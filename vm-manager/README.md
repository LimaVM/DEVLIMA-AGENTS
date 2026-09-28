# VM Manager — implementação na Fase 5

Serviço systemd interno no host, isolado do Core, com API autenticada e allowlist de operações. Usará o template existente e a chave pública dedicada sem alterar ambos.

Interface planejada: WorkerProvider → LinuxWorkerProvider/WindowsWorkerProvider. Linux implementará create/start/stop/status/delete/reset/snapshot/restore; Windows só terá contrato reservado inicialmente.

Pré-requisitos confirmados em CURRENT_STATE.md. Não instalar unidade systemd vazia ou container privilegiado nesta fase.
