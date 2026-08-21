@echo off
chcp 65001 > nul
title Telegram Garant Bot
cd /d "%~dp0"
echo ==============================================
echo  Запуск Telegram Garant Bot...
echo ==============================================
python main.py
pause
