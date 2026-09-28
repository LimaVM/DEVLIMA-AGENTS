from uuid import UUID

import httpx2 as httpx


class ManagerError(Exception):
    def __init__(self, code, uncertain=False):
        self.code, self.uncertain = code, uncertain
        super().__init__(code)


class ManagerClient:
    def __init__(self, settings):
        transport = httpx.HTTPTransport(uds=settings.vm_manager_socket)
        self.client = httpx.Client(
            transport=transport,
            base_url="http://vm-manager",
            headers={"Authorization": "Bearer " + settings.vm_manager_token.get_secret_value()},
            timeout=httpx.Timeout(350, connect=5),
            trust_env=False,
            follow_redirects=False,
        )

    def close(self):
        self.client.close()

    def request(self, method, path, **kwargs):
        try:
            response = self.client.request(method, path, **kwargs)
            if response.status_code == 404:
                raise ManagerError("not_found")
            if response.status_code >= 400:
                detail = response.json().get("detail", "manager_error")
                raise ManagerError(detail if isinstance(detail, str) else "manager_invalid_request")
            return response.json()
        except (httpx.RequestError, ValueError):
            raise ManagerError("manager_unreachable", uncertain=True) from None

    def operation(self, identifier, owner):
        return self.request(
            "GET", f"/v1/operations/{UUID(str(identifier))}", params={"owner": str(owner)}
        )

    def perform(self, command):
        return self.request(
            "POST",
            "/v1/operations",
            json={
                "request_id": str(command.id),
                "worker_id": str(command.worker_id),
                "owner": str(command.user_id),
                "kind": command.kind,
                **command.arguments,
            },
        )

    def status(self, identifier, owner):
        return self.request(
            "GET", f"/v1/workers/{UUID(str(identifier))}", params={"owner": str(owner)}
        )
