import json
from contextlib import contextmanager

import httpx2 as httpx
import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.config import Settings, get_settings
from app.llm.base import LLMError, LLMMessage
from app.llm.groq import GroqProvider
from app.llm.llama_cpp import LlamaCppProvider
from app.llm.router import LLMRouter
from app.llm.service import DatabaseAuditRecorder
from app.models import AuditLog, LLMRequest
from app.security import create_token

MESSAGES = [LLMMessage(role="user", content="contexto privado para teste")]


def response(content="resposta local"):
    return httpx.Response(
        200,
        json={
            "id": "completion-test",
            "choices": [{"message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": 12, "completion_tokens": 3},
        },
    )


def make_router(local_handler, cloud_handler=None, *, enabled=True, recorder=None):
    cloud_calls = []

    def cloud(request):
        cloud_calls.append(request)
        return cloud_handler(request) if cloud_handler else response("resposta cloud")

    attempts = []
    router = LLMRouter(
        LlamaCppProvider(
            "http://100.102.91.22:8080/v1",
            "local-model",
            timeout=1,
            health_timeout=1,
            client=httpx.Client(transport=httpx.MockTransport(local_handler)),
        ),
        GroqProvider(
            "test-cloud-model",
            api_key="test-key-not-a-real-credential",
            timeout=1,
            health_timeout=1,
            client=httpx.Client(transport=httpx.MockTransport(cloud)),
        ),
        allow_cloud_fallback=enabled,
        record_attempt=recorder if recorder is not None else attempts.append,
    )
    return router, cloud_calls, attempts


def test_local_chat_does_not_contact_cloud():
    def local(request):
        body = json.loads(request.content)
        assert body["model"] == "local-model"
        assert body["messages"][0]["content"] == MESSAGES[0].content
        assert "authorization" not in request.headers
        return response()

    router, cloud, attempts = make_router(local)
    result = router.chat(MESSAGES)
    assert result.completion.content == "resposta local"
    assert result.completion.provider == "llama_cpp"
    assert not result.fallback_used
    assert len(attempts) == 1 and attempts[0].success
    assert not cloud
    router.close()


@pytest.mark.parametrize("status", [500, 502, 503, 504])
def test_technical_http_failure_falls_back_once(status):
    router, cloud, attempts = make_router(lambda request: httpx.Response(status))
    result = router.chat(MESSAGES)
    assert result.completion.provider == "groq"
    assert result.fallback_used
    assert len(cloud) == 1
    assert cloud[0].headers["authorization"] == "Bearer test-key-not-a-real-credential"
    assert [item.provider for item in attempts] == ["llama_cpp", "groq"]
    assert attempts[0].error_code == "server_error"
    assert attempts[0].request_id == attempts[1].request_id == result.request_id
    router.close()


@pytest.mark.parametrize("error_type", [httpx.ReadTimeout, httpx.ConnectError])
def test_transport_failure_falls_back(error_type):
    def fail(request):
        raise error_type("secret upstream text that must not be recorded", request=request)

    router, cloud, attempts = make_router(fail)
    assert router.chat(MESSAGES).fallback_used
    assert len(cloud) == 1
    assert "secret" not in attempts[0].error_code
    router.close()


@pytest.mark.parametrize("status", [400, 401, 403, 404, 422, 429])
def test_non_technical_failures_never_send_context_to_cloud(status):
    router, cloud, attempts = make_router(
        lambda request: httpx.Response(status, json={"error": {"message": "private"}})
    )
    with pytest.raises(LLMError):
        router.chat(MESSAGES)
    assert not cloud
    assert len(attempts) == 1 and not attempts[0].success
    router.close()


def test_explicit_model_unavailable_allows_fallback():
    router, cloud, attempts = make_router(
        lambda request: httpx.Response(404, json={"error": {"code": "model_not_found"}})
    )
    assert router.chat(MESSAGES).fallback_used
    assert attempts[0].error_code == "model_unavailable"
    assert len(cloud) == 1
    router.close()


@pytest.mark.parametrize("failure", [500, 503])
def test_fallback_disabled_makes_zero_cloud_requests(failure):
    router, cloud, attempts = make_router(lambda request: httpx.Response(failure), enabled=False)
    with pytest.raises(LLMError):
        router.chat(MESSAGES)
    assert not cloud
    assert len(attempts) == 1
    router.close()


def test_fallback_disabled_also_skips_cloud_health_check():
    router, cloud, _ = make_router(
        lambda request: httpx.Response(200, json={"data": [{"id": "local-model"}]}), enabled=False
    )
    health = router.health_check()
    assert health["local"]["healthy"]
    assert health["cloud"]["error_code"] == "disabled"
    assert not cloud
    router.close()


def test_cloud_failure_is_audited_and_not_retried():
    router, cloud, attempts = make_router(
        lambda request: httpx.Response(503), lambda request: httpx.Response(401)
    )
    with pytest.raises(LLMError, match="auth_error"):
        router.chat(MESSAGES)
    assert len(cloud) == 1
    assert len(attempts) == 2
    assert attempts[1].fallback and attempts[1].error_code == "auth_error"
    router.close()


@pytest.mark.parametrize(
    "content", ["Não posso ajudar com isso.", "Resposta curta que o usuário pode não gostar."]
)
def test_valid_local_reply_is_not_judged_to_force_cloud(content):
    router, cloud, _ = make_router(lambda request: response(content))
    assert router.chat(MESSAGES).completion.content == content
    assert not cloud
    router.close()


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"choices": []},
        {"choices": [{"message": {"content": None}}]},
        {"choices": [{"message": {"content": ""}}]},
    ],
)
def test_invalid_response_does_not_trigger_cloud(body):
    router, cloud, attempts = make_router(lambda request: httpx.Response(200, json=body))
    with pytest.raises(LLMError, match="invalid_response"):
        router.chat(MESSAGES)
    assert not cloud
    assert attempts[0].error_code == "invalid_response"
    router.close()


def test_redirect_does_not_forward_key_or_context():
    router, cloud, _ = make_router(
        lambda request: httpx.Response(307, headers={"Location": "https://public.invalid"})
    )
    with pytest.raises(LLMError, match="http_error"):
        router.chat(MESSAGES)
    assert not cloud
    router.close()


def test_health_checks_configured_model_presence():
    router, cloud, _ = make_router(
        lambda request: httpx.Response(200, json={"data": [{"id": "local-model"}]}),
        lambda request: httpx.Response(200, json={"data": [{"id": "test-cloud-model"}]}),
    )
    health = router.health_check()
    assert health["local"]["healthy"] and health["cloud"]["healthy"]
    assert len(cloud) == 1 and cloud[0].method == "GET"
    router.close()


def test_missing_model_reported_unavailable():
    router, _, _ = make_router(lambda request: httpx.Response(200, json={"data": []}))
    assert router.health_check()["local"]["error_code"] == "model_unavailable"
    router.close()


def test_missing_key_never_issues_request():
    requests = []
    with httpx.Client(
        transport=httpx.MockTransport(lambda request: requests.append(request))
    ) as client:
        provider = GroqProvider("model", api_key="", timeout=1, health_timeout=1, client=client)
        with pytest.raises(LLMError, match="not_configured"):
            provider.chat(MESSAGES)
        assert not provider.health_check().healthy
        assert not requests


def test_json_mode_is_structured_request_option():
    def local(request):
        assert json.loads(request.content)["response_format"] == {"type": "json_object"}
        return response('{"reply":"ok","actions":[]}')

    router, cloud, _ = make_router(local)
    assert json.loads(router.chat(MESSAGES, json_mode=True).completion.content)["reply"] == "ok"
    assert not cloud
    router.close()


def test_thinking_disabled_only_for_local_structured_requests():
    captured = []

    def handle(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200, json={"choices": [{"message": {"content": '{"reply":"ok"}'}}]})

    local = LlamaCppProvider(
        "http://127.0.0.1:9/v1",
        "test",
        timeout=1,
        health_timeout=1,
        client=httpx.Client(transport=httpx.MockTransport(handle)),
    )
    local.chat(MESSAGES, json_mode=True)
    local.chat(MESSAGES)
    cloud = GroqProvider(
        "test",
        api_key="test-key",
        timeout=1,
        health_timeout=1,
        client=httpx.Client(transport=httpx.MockTransport(handle)),
    )
    cloud.chat(MESSAGES, json_mode=True)
    assert captured[0]["reasoning_effort"] == "none"
    assert captured[0]["chat_template_kwargs"] == {"enable_thinking": False}
    assert "reasoning_effort" not in captured[1] and "reasoning_effort" not in captured[2]
    assert "chat_template_kwargs" not in captured[2]
    local.close()
    cloud.close()


@pytest.mark.parametrize(
    "url",
    [
        "http://8.8.8.8/v1",
        "http://100.102.91.22:abc/v1",
        "http://name.invalid/v1",
        "http://key@100.102.91.22/v1",
        "http://100.102.91.22/v1?key=secret",
        "ftp://100.102.91.22/v1",
    ],
)
def test_primary_url_must_be_private_and_without_credentials(url):
    with pytest.raises(ValidationError):
        Settings(local_llm_base_url=url)


def test_audit_contains_metadata_only(session, user):
    router, _, _ = make_router(
        lambda request: httpx.Response(503), recorder=DatabaseAuditRecorder(session)
    )
    result = router.chat(MESSAGES, user_id=user.id)
    rows = list(
        session.scalars(select(LLMRequest).where(LLMRequest.request_id == result.request_id))
    )
    assert len(rows) == 2
    assert rows[0].created_at.tzinfo is not None
    assert all(row.user_id == user.id for row in rows)
    assert {row.provider for row in rows} == {"llama_cpp", "groq"}
    assert sum(row.fallback for row in rows) == 1
    assert sum(row.success for row in rows) == 1
    events = list(session.scalars(select(AuditLog).where(AuditLog.event == "llm.request")))
    assert len(events) == 2
    assert MESSAGES[0].content not in str([event.details for event in events])
    assert "test-key" not in str([event.details for event in events])
    router.close()


def test_llm_api_requires_authentication(client):
    assert client.get("/llm/health").status_code == 401
    assert (
        client.post("/llm/chat", json={"messages": [{"role": "user", "content": "oi"}]}).status_code
        == 401
    )


def test_llm_api_bounds_context_before_provider(client, user):
    token = create_token(user, get_settings())
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/llm/chat", headers=headers, json={"messages": [{"role": "user", "content": "x" * 8001}]}
    )
    assert response.status_code == 422
    assert "x" * 100 not in response.text
    assert (
        client.post(
            "/llm/chat",
            headers=headers,
            json={"messages": [{"role": "system", "content": "system"}]},
        ).status_code
        == 422
    )


def test_llm_api_response_is_correlated_and_audited(client, user, session, monkeypatch):
    @contextmanager
    def fake_build(settings, db):
        router, _, _ = make_router(lambda request: response(), recorder=DatabaseAuditRecorder(db))
        try:
            yield router
        finally:
            router.close()

    monkeypatch.setattr("app.api.llm.build_router", fake_build)
    token = create_token(user, get_settings())
    reply = client.post(
        "/llm/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"messages": [{"role": "user", "content": "oi"}]},
    )
    assert reply.status_code == 200
    assert reply.json()["request_id"] == reply.headers["X-Request-ID"]
    assert reply.json()["provider"] == "llama_cpp"
    assert not reply.json()["fallback_used"]
    row = session.scalar(select(LLMRequest))
    assert row.user_id == user.id


def test_llm_api_error_hides_upstream_body(client, user, monkeypatch):
    @contextmanager
    def fake_build(settings, db):
        router, _, _ = make_router(
            lambda request: httpx.Response(401, json={"error": {"message": "upstream secret"}}),
            recorder=DatabaseAuditRecorder(db),
        )
        try:
            yield router
        finally:
            router.close()

    monkeypatch.setattr("app.api.llm.build_router", fake_build)
    token = create_token(user, get_settings())
    reply = client.post(
        "/llm/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"messages": [{"role": "user", "content": "oi"}]},
    )
    assert reply.status_code == 503
    assert reply.json()["detail"]["code"] == "auth_error"
    assert "upstream secret" not in reply.text
