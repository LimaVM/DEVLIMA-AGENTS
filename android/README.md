# Android V1 — desenvolvido na VPS

Aplicativo Kotlin/Compose/Material 3: login HTTPS, sessão Android Keystore, chat/histórico/fila offline, rotina e memórias propostas, conexão WSS com ACK/heartbeat/backoff, chamadas internas e SpeechRecognizer/TextToSpeech com alternativa por texto. Sem Firebase/WebRTC nesta V1.

Package release `br.com.vegasolucoes.agent`, debug `.debug`; versão 1.0.0/code 100, Android 8.0/API 26 ou superior, target/compile 36. Servidor padrão `https://agent.vegasolucoes.com.br`; Groq/API keys ficam somente no backend. A senha de login não é persistida.

## Build na VPS

Workspace `/srv/devlima-agent/android`, JDK 17, SDK `/srv/devlima-android-sdk`, Gradle wrapper 8.13, AGP 8.13.2 e Kotlin 2.3.10. SDK/build-tools 36.0.0 e imagem de emulador Google APIs 36 instalados fora do Git. Gradle usa até dois workers e heap de 3 GiB.

```sh
cd /srv/devlima-agent/android
export ANDROID_HOME=/srv/devlima-android-sdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
./gradlew --no-daemon assembleRelease testDebugUnitTest lintDebug
/srv/devlima-android-sdk/build-tools/36.0.0/apksigner verify --verbose --print-certs app/build/outputs/apk/release/app-release.apk
sha256sum app/build/outputs/apk/release/app-release.apk
```

Keystore `/srv/devlima-build-tools/agent-release.jks` e `signing.properties`, modo 0600, fora do Git. Ausência desses arquivos produz release sem assinatura de produção; não distribua esse arquivo. Preserve o certificado para futuras atualizações. [Release privada v1.0.0](https://github.com/LimaVM/DEVLIMA-AGENTS/releases/tag/v1.0.0) contém APK e checksum.

## Testes

Três testes unitários e lint sem erros passaram na build final. Três instrumentados básicos, um relatório de capacidades de voz e um E2E temporizado passaram no emulador API 36 da VPS. E2E confirmou café 5 min, chamada 2 min, WSS/contexto/ACK, rotina e transcrição enviada por texto; não capturou voz de microfone físico. Evidências em [PHASE_9.md](../docs/PHASE_9.md).

Com emulador iniciado pelo usuário do build e ADB/console restritos ao loopback, execute `connectedDebugAndroidTest` com `-Pandroid.testInstrumentationRunnerArguments.class=<classe>` para filtrar as classes básicas em `app/src/androidTest`. Sem configuração privada, o E2E é ignorado.

`EndToEndTest` é opt-in: exige `no_backup/e2e-private.json`, conta sintética cujo nome começa com `devlima-v1-validation`, credencial externa privada e servidor real. Injete o arquivo via `adb shell run-as` apenas no build debug, com permissões privadas; nunca versione nem imprima seu conteúdo. O teste o apaga após login. Revogue a conta/dispositivo e limpe o app depois; ele cria eventos reais e usa o provider configurado, podendo gerar custo.

## Usar o APK

Instale a release, permita instalação dessa origem conforme o Android, entre com a credencial entregue separadamente e toque Conectar em Conta. Permita notificações para lembretes/chamadas. Microfone é solicitado ao atender/ativar áudio com o aplicativo visível. Negando a permissão, a chamada ainda permite texto. Atender pela notificação abre a interface; ela confirma o atendimento. Chamadas são internas ao app.

Mute interrompe escuta/TTS; saída alterna speaker/auricular conforme recursos do aparelho. Encerrar confirma no Core e fecha áudio/serviço. Com conexão interrompida, mensagens mantêm UUID para replay; confira seu estado antes de tentar envio novo.

## Homologação física pendente

- Registrar modelo, versão Android e engine de reconhecimento/TTS pt-BR.
- Login, histórico e lembrete café 5 min com app visível e em background/tela bloqueada.
- Chamada 2 min: notificação, atender/recusar, permissão concedida/negada.
- Duas falas capturadas por microfone, respostas com contexto e TTS audível; mute/unmute, speaker/auricular e encerramento sem áudio residual.
- Wi-Fi → rede móvel → offline → reconexão; ausência de mensagens/avisos duplicados.
- Bateria/Doze/restrições do fabricante; force stop, reabertura/conexão explícita, renovação/expiração de sessão.

Foreground Service usa notificação persistente e início pelo usuário. Android pode suspender serviços/rede em Doze, restringir bateria e impedir entrega após force stop. Sem Firebase e sem receiver de boot, não há promessa de chamada/aviso após o usuário forçar parada ou bloquear o app. Não há contorno dessas políticas nem solicitação automática de isenção de bateria. A VPS realiza o desenvolvimento/build; não substitui essa homologação no telefone.
