# Android — desenvolvimento na VPS

Projeto Kotlin/Compose/Material 3 em `/srv/devlima-agent/android` na VPS Ubuntu. SDK em `/srv/devlima-android-sdk`, JDK 17 e Gradle 8.13; wrapper tem checksum oficial. Fontes são espelhadas no Git, compilação e emulador ficam na VPS por preferência do proprietário.

```sh
cd /srv/devlima-agent/android
ANDROID_HOME=/srv/devlima-android-sdk ./gradlew --no-daemon assembleDebug testDebugUnitTest lintDebug
ANDROID_HOME=/srv/devlima-android-sdk ./gradlew --no-daemon connectedDebugAndroidTest
```

Build limitado a dois workers e heap 3 GiB. Emulador API 36 usa KVM, dois cores e 3 GiB; não executar builds pesados junto de todos os workers de produção. SDK, caches e APKs não são versionados.

Login HTTPS, tokens/eventos AES-GCM/Android Keystore, WSS/ACK após persistência, heartbeat, refresh rotativo e reconexão com backoff. Senha não é persistida; nenhuma chave do backend/provider é embutida. Foreground Service specialUse inicia pela ação do usuário e oferece desconectar. Permissão de notificações é necessária para avisos. Force stop e restrições de bateria seguem as políticas do Android; reconexão não promete contorná-las.

Chat/rotina chegam na Fase 7, chamadas internas/SpeechRecognizer/TextToSpeech na Fase 8. Sem Firebase/WebRTC. Assinatura release usa arquivo privado externo `/srv/devlima-build-tools/signing.properties`; manter keystore e senhas fora do Git.
