@echo off
chcp 65001 >nul
REM Склеивает видео из частей обратно в целые файлы. Двойной щелчок по этому файлу.
cd /d "%~dp0"
for /r %%f in (*.part01) do (
  copy /b "%%~dpnf.part*" "%%~dpnf" >nul
  echo Готово: %%~nf
)
echo Все видео собраны. Части .partXX можно удалить.
pause
