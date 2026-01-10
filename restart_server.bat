@echo off
REM Script para reiniciar o servidor Hit Predictor
echo ================================================
echo Reiniciando Hit Predictor Server
echo ================================================
echo.

REM Para processos Python rodando na porta 5002
echo [1/3] Parando servidor anterior...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5002 ^| findstr LISTENING') do (
    echo Matando processo %%a
    taskkill /F /PID %%a 2>nul
)

REM Aguarda 2 segundos
timeout /t 2 /nobreak >nul

REM Inicia novo servidor
echo.
echo [2/3] Iniciando servidor com mudancas aplicadas...
cd /d "%~dp0"
start "Hit Predictor Server" python backend\api.py

REM Aguarda servidor iniciar
timeout /t 3 /nobreak >nul

echo.
echo [3/3] Servidor reiniciado!
echo ================================================
echo Servidor disponivel em: http://localhost:5002
echo ================================================
echo.
echo Pressione qualquer tecla para fechar...
pause >nul
