from uuid import UUID

import httpx2 as httpx


# Documentação: Define o tipo ManagerError e reúne o estado/contrato descrito para este módulo.
class ManagerError(Exception):
    # Documentação: Inicializa ManagerError com as dependências e estado declarados.
    def __init__(self, code, uncertain=False):
        self.code, self.uncertain = code, uncertain
        super().__init__(code)


# Documentação: Define o tipo ManagerClient e reúne o estado/contrato descrito para este módulo.
class ManagerClient:
    # Documentação: Inicializa ManagerClient com as dependências e estado declarados.
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

    # Documentação: Libera ManagerClient.close, segundo o contrato e as verificações deste módulo.
    def close(self):
        self.client.close()

    # Documentação: Executa a requisição de ManagerClient.request, segundo o contrato e as
    # verificações deste módulo.
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

    # Documentação: Implementa ManagerClient.operation como parte do fluxo descrito para este
    # arquivo.
    def operation(self, identifier, owner):
        return self.request(
            "GET", f"/v1/operations/{UUID(str(identifier))}", params={"owner": str(owner)}
        )

    # Documentação: Implementa ManagerClient.perform como parte do fluxo descrito para este
    # arquivo.
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

    # Documentação: Implementa ManagerClient.status como parte do fluxo descrito para este
    # arquivo.
    def status(self, identifier, owner):
        return self.request(
            "GET", f"/v1/workers/{UUID(str(identifier))}", params={"owner": str(owner)}
        )
