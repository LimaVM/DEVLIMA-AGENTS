from time import perf_counter

import httpx2 as httpx
from pydantic import ValidationError

from app.llm.base import LLMCompletion, LLMError, LLMMessage, LLMProvider, ProviderHealth

MODEL_UNAVAILABLE_CODES = {
    "model_not_found",
    "model_not_available",
    "model_unavailable",
    "model_not_loaded",
    "model_not_ready",
    "model_decommissioned",
}


class OpenAICompatibleProvider(LLMProvider):
    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        timeout: float,
        health_timeout: float,
        api_key: str = "",
        requires_key: bool = False,
        client: httpx.Client | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.health_timeout = health_timeout
        self.configured = bool(base_url and model and (api_key or not requires_key))
        self.client = client or httpx.Client(
            timeout=httpx.Timeout(timeout, connect=min(timeout, 5), pool=5),
            follow_redirects=False,
            trust_env=False,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        if not self.configured:
            raise LLMError("not_configured")
        try:
            response = self.client.request(
                method, f"{self.base_url}/{path}", headers=self.headers, **kwargs
            )
        except httpx.TimeoutException:
            raise LLMError("timeout") from None
        except (httpx.NetworkError, httpx.RemoteProtocolError):
            raise LLMError("connection_error") from None
        except httpx.RequestError:
            raise LLMError("transport_error") from None
        if 500 <= response.status_code <= 599:
            raise LLMError("server_error", status_code=response.status_code)
        if not 200 <= response.status_code <= 299:
            code = "http_error"
            if response.status_code in {401, 403}:
                code = "auth_error"
            elif response.status_code == 429:
                code = "rate_limited"
            elif response.status_code in {400, 404, 422}:
                try:
                    error = response.json().get("error", {})
                    if isinstance(error, dict) and error.get("code") in MODEL_UNAVAILABLE_CODES:
                        code = "model_unavailable"
                except (ValueError, AttributeError, TypeError):
                    pass
            raise LLMError(code, status_code=response.status_code)
        return response

    def chat(
        self, messages: list[LLMMessage], *, max_tokens: int = 512, json_mode: bool = False
    ) -> LLMCompletion:
        body = {
            "model": self.model,
            "messages": [message.model_dump() for message in messages],
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "stream": False,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
            body.update(self.structured_options())
        response = self._request("POST", "chat/completions", json=body)
        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise ValueError("Missing text")
            upstream_id = data.get("id")
            if not isinstance(upstream_id, str) or len(upstream_id) > 255:
                upstream_id = None
            usage = data.get("usage") or {}
            return LLMCompletion(
                content=content,
                provider=self.name,
                model=self.model,
                upstream_request_id=upstream_id,
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
            )
        except (ValueError, KeyError, IndexError, TypeError, AttributeError, ValidationError):
            raise LLMError("invalid_response") from None

    def structured_options(self) -> dict:
        return {}

    def health_check(self) -> ProviderHealth:
        started = perf_counter()
        code = None
        try:
            response = self._request("GET", "models", timeout=self.health_timeout)
            data = response.json()["data"]
            available = any(
                item.get("id") == self.model or self.model in (item.get("aliases") or [])
                for item in data
                if isinstance(item, dict) and item.get("active", True)
            )
            if not available:
                code = "model_unavailable"
        except LLMError as error:
            code = error.code
        except (ValueError, KeyError, TypeError):
            code = "invalid_response"
        return ProviderHealth(
            provider=self.name,
            configured=self.configured,
            healthy=code is None,
            model=self.model,
            latency_ms=max(0, round((perf_counter() - started) * 1000)),
            error_code=code,
        )

    def close(self) -> None:
        self.client.close()
