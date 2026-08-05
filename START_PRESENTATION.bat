@echo off
setlocal
title Immersive Exhibition Presentation
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve-presentation.ps1"
endlocal
