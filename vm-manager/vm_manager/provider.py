from typing import Protocol


# Documentação: Define o tipo WorkerProvider e reúne o estado/contrato descrito para este módulo.
class WorkerProvider(Protocol):
    """Host-side lifecycle contract. Implementations never accept host shell commands."""

    # Documentação: Libera WorkerProvider.close, segundo o contrato e as verificações deste
    # módulo.
    def close(self) -> None: ...
    # Documentação: Confere WorkerProvider.check_resources, segundo o contrato e as verificações
    # deste módulo.
    def check_resources(self, rows: list[dict], desired: dict) -> None: ...
    # Documentação: Cria WorkerProvider.create, segundo o contrato e as verificações deste módulo.
    def create(self, row: dict) -> dict: ...
    # Documentação: Implementa WorkerProvider.status como parte do fluxo descrito para este
    # arquivo.
    def status(self, row: dict) -> dict: ...
    # Documentação: Inicia WorkerProvider.start, segundo o contrato e as verificações deste
    # módulo.
    def start(self, row: dict) -> dict: ...
    # Documentação: Interrompe WorkerProvider.stop, segundo o contrato e as verificações deste
    # módulo.
    def stop(self, row: dict) -> bool: ...
    # Documentação: Implementa WorkerProvider.destroy como parte do fluxo descrito para este
    # arquivo.
    def destroy(self, row: dict) -> dict: ...
    # Documentação: Implementa WorkerProvider.reset como parte do fluxo descrito para este
    # arquivo.
    def reset(self, row: dict, generation: str) -> dict: ...
    # Documentação: Implementa WorkerProvider.snapshot como parte do fluxo descrito para este
    # arquivo.
    def snapshot(self, row: dict, identifier: str) -> tuple[dict, dict]: ...
    # Documentação: Implementa WorkerProvider.restore como parte do fluxo descrito para este
    # arquivo.
    def restore(self, row: dict, snapshot: dict) -> dict: ...
    # Documentação: Implementa WorkerProvider.execute como parte do fluxo descrito para este
    # arquivo.
    def execute(self, row: dict, identifier: str, script: str, timeout: int) -> dict: ...
