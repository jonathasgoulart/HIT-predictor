# 🚀 Guia de Deploy no Render (Suporte Total a MP3)

O Render é a melhor alternativa gratuita para o seu caso, pois ele permite usar **Docker**, o que nos possibilita instalar o **FFmpeg** e processar MP3, M4A e qualquer outro formato sem problemas.

## 1. Preparação
Certifique-se de que os seguintes arquivos estão na raiz:
- `Dockerfile`: Configura o Linux, FFmpeg e Python.
- `requirements.txt`: Inclui `gunicorn` para o servidor de produção.
- `.vercelignore` ou `.gitignore`: Para não subir arquivos desnecessários.

## 2. Passo a Passo no Render
1. Crie uma conta em [render.com](https://render.com).
2. Clique em **"New +"** e selecione **"Web Service"**.
3. Conecte seu repositório do GitHub.
4. Nas configurações do serviço:
   - **Runtime**: Selecione `Docker`. (Isso é crucial!)
   - **Instance Type**: Escolha `Free`.
5. Clique em **"Deploy Web Service"**.

## 3. Vantagens do Render + Docker
- ✅ **Suporte a MP3/M4A**: O Docker já instala o FFmpeg automaticamente.
- ✅ **Timeout Longo**: Diferente do Vercel, o Render permite que a análise demore um pouco mais (até 120 segundos no nosso config).
- ✅ **Servidor Real**: Não é "serverless", então o código que funciona no seu computador funcionará exatamente igual lá.

---
**Nota**: Na versão gratuita do Render, o servidor "dorme" após 15 minutos de inatividade. O primeiro acesso após um tempo pode demorar uns 30 segundos para "acordar".

🎵 **Tudo pronto! Seu Dockerfile está configurado para o sucesso.**
