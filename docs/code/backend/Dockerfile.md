# backend/Dockerfile

Constrói etapas de dependências, execução de produção e testes; estabelece usuário, diretório e comando do container de backend.

[Arquivo fonte](../../../backend/Dockerfile) · 22 linhas físicas.

Referência gerada por `scripts/document_code.py`. O contexto editorial vem de `scripts/code_reference_catalog.json`; descrições por linha usam AST/análise lexical. O guia descreve a instrução e não comprova sua execução ou homologação.

## Linha a linha

| Linha | Código original | Explicação |
| --- | --- | --- |
| <a id="L1"></a>1 | <code>FROM python:3.12-slim@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f AS base</code> | Diretiva Dockerfile FROM para configurar a etapa da imagem. |
| <a id="L2"></a>2 | <code>ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1</code> | Diretiva Dockerfile ENV para configurar a etapa da imagem. |
| <a id="L3"></a>3 | <code>WORKDIR /app</code> | Diretiva Dockerfile WORKDIR para configurar a etapa da imagem. |
| <a id="L4"></a>4 | <code>COPY requirements.txt .</code> | Diretiva Dockerfile COPY para configurar a etapa da imagem. |
| <a id="L5"></a>5 | <code>RUN pip install --disable-pip-version-check -r requirements.txt</code> | Diretiva Dockerfile RUN para configurar a etapa da imagem. |
| <a id="L6"></a>6 | <code>RUN groupadd --gid 10001 agent &amp;&amp; useradd --uid 10001 --gid agent --no-create-home agent</code> | Diretiva Dockerfile RUN para configurar a etapa da imagem. |
| <a id="L7"></a>7 | <code>COPY app ./app</code> | Diretiva Dockerfile COPY para configurar a etapa da imagem. |
| <a id="L8"></a>8 | <code>COPY alembic.ini .</code> | Diretiva Dockerfile COPY para configurar a etapa da imagem. |
| <a id="L9"></a>9 | <code>COPY migrations ./migrations</code> | Diretiva Dockerfile COPY para configurar a etapa da imagem. |
| <a id="L10"></a>10 | <code>USER 10001:10001</code> | Diretiva Dockerfile USER para configurar a etapa da imagem. |
| <a id="L11"></a>11 | <code>EXPOSE 8000</code> | Diretiva Dockerfile EXPOSE para configurar a etapa da imagem. |
| <a id="L12"></a>12 | <code>CMD [&quot;uvicorn&quot;, &quot;app.main:app&quot;, &quot;--host&quot;, &quot;0.0.0.0&quot;, &quot;--port&quot;, &quot;8000&quot;, &quot;--ws&quot;, &quot;websockets-sansio&quot;, &quot;--ws-max-size&quot;, &quot;65536&quot;, &quot;--limit-concurrency&quot;, &quot;128&quot;, &quot;--proxy-headers&quot;, &quot;--forwarded-allow-ips&quot;, &quot;*&quot;]</code> | Diretiva Dockerfile CMD para configurar a etapa da imagem. |
| <a id="L13"></a>13 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L14"></a>14 | <code>FROM base AS test</code> | Diretiva Dockerfile FROM para configurar a etapa da imagem. |
| <a id="L15"></a>15 | <code>USER root</code> | Diretiva Dockerfile USER para configurar a etapa da imagem. |
| <a id="L16"></a>16 | <code>COPY requirements-dev.txt pyproject.toml ./</code> | Diretiva Dockerfile COPY para configurar a etapa da imagem. |
| <a id="L17"></a>17 | <code>RUN pip install --disable-pip-version-check -r requirements-dev.txt</code> | Diretiva Dockerfile RUN para configurar a etapa da imagem. |
| <a id="L18"></a>18 | <code>COPY tests ./tests</code> | Diretiva Dockerfile COPY para configurar a etapa da imagem. |
| <a id="L19"></a>19 | <code>USER 10001:10001</code> | Diretiva Dockerfile USER para configurar a etapa da imagem. |
| <a id="L20"></a>20 | <code>CMD [&quot;pytest&quot;, &quot;-q&quot;, &quot;-p&quot;, &quot;no:cacheprovider&quot;]</code> | Diretiva Dockerfile CMD para configurar a etapa da imagem. |
| <a id="L21"></a>21 | <code>∅</code> | Linha em branco que separa entradas de configuração. |
| <a id="L22"></a>22 | <code>FROM base AS production</code> | Diretiva Dockerfile FROM para configurar a etapa da imagem. |
