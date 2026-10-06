# Videomontaj — монтаж Reels и YouTube

## Структура
- `media/` — исходники (в git не попадают, слишком большие). Скачивать сюда из Google Drive.
- `remotion-studio/` — проект Remotion (React). Композиции в `src/Composition.tsx`: `TestReel` 1080×1920, `TestYouTube` 1920×1080.
- `hyperframes-studio/reels/` — проект HyperFrames (HTML + GSAP). GSAP подключён локально из `vendor/`, CDN в песочнице недоступен.
- `scripts/transcribe.py` — расшифровка речи по словам (faster-whisper) → `.words.json` + `.srt`.
- `scripts/setup.sh` — восстанавливает зависимости в новом контейнере (запускается SessionStart-хуком).
- `.claude/skills/` — скиллы: Remotion, HyperFrames, Taste Skill, Impeccable, Эмиль Ковальски.

## Окружение (облачная песочница)
- Браузер для рендера — локальный Chromium headless shell; путь задан в `remotion.config.ts` и в `HYPERFRAMES_BROWSER_PATH`.
- Внешние CDN, Hugging Face, remotion.media заблокированы сетевой политикой: все библиотеки и шрифты держать локально.
- Шрифт Inter с кириллицей установлен в системе.

## Рендер
- Remotion: `cd remotion-studio && npx remotion render <CompId> out/<name>.mp4`
- HyperFrames: `cd hyperframes-studio/reels && npx hyperframes check && npx hyperframes render --quality draft --output out/<name>.mp4`
- Проверка: `ffprobe -v error -show_entries format=duration:stream=width,height -of csv=p=0 <file>`, затем смотреть кадры через `ffmpeg -ss <t> -frames:v 1`.

## Форматы
- Reels/Shorts/TikTok: 1080×1920, 30 fps, текст и субтитры вне нижних ~20% и верхних ~12% кадра (интерфейс платформы).
- YouTube: 1920×1080, 30 fps (или как в исходнике).
