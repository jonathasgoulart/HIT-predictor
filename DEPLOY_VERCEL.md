# 🚀 Guia de Deploy no Vercel - Hit Predictor

Siga estes passos para colocar sua aplicação online:

## 1. Preparação Local
Verifique se você tem os novos arquivos de configuração:
- `vercel.json`: Define como o Vercel deve tratar o frontend e a API.
- `requirements.txt`: Lista as bibliotecas Python necessárias.
- `api/index.py`: O ponto de entrada para o servidor no Vercel.
- `.vercelignore`: Garante que arquivos pesados de dados brutos não sejam enviados.

## 2. Deploy via CLI (Recomendado)
Se você tem o Vercel CLI instalado:
1. Abra o terminal na pasta raiz do projeto.
2. Digite `vercel`.
3. Siga as instruções no terminal (pode dar Enter em tudo para as opções padrão).

## 3. Deploy via GitHub (Automático)
1. Crie um repositório no seu GitHub.
2. Faça o push de todos os arquivos do projeto.
3. No site da Vercel, clique em **"Add New"** -> **"Project"**.
4. Importe o repositório do GitHub.
5. Em **"Build & Development Settings"**, o Vercel deve detectar automaticamente que é um projeto Flask/Python.
6. Clique em **"Deploy"**.

## ⚠️ Observações Importantes para o Vercel

### Limitação de MP3/M4A
Como o Vercel é um ambiente "serverless", ele não possui o sistema operacional completo com codecs de áudio. 
- **Suporte Nativo**: Arquivos **.WAV** e **.FLAC** funcionarão perfeitamente.
- **Suporte MP3**: Para funcionar MP3, teríamos que incluir um binário estático do FFmpeg no repositório. Como isso aumenta muito o tamanho do projeto, recomendo testar com **.WAV** inicialmente na nuvem.

### Tempo de Processamento
O Vercel tem um limite de tempo (timeout) de 10 a 60 segundos por requisição.
- Análises de músicas longas (> 5 min) podem falhar se o processamento demorar demais.
- Nossos modelos de IA são leves (~4MB), então o carregamento deve ser rápido.

---
**Status**: Configurações geradas com sucesso! Agora é só subir para a nuvem. 🎵
