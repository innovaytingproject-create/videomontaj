---
workflow: general-video
flow: automation
storyboard: no
message: "Биомассажёр FOHERB — 5 функций в одном компактном приборе, заменяет 10 ручных массажей"
destination: instagram-reels
aspect: "9:16"
language: ru (subtitles; speech is Uzbek with Russian words)
audience: потенциальные покупатели, реклама
length: по основным смысловым блокам (~99 s)
---

## Intent
Реклама продукта из одного дубля распаковки: вырезать черновые куски, паузы и оговорки; естественный монтаж,
плавный звук, субтитры, заголовки/плашки/цифры/логотип в бренде (чёрный + оранжевый), фоновая музыка.
Хук в начале и призыв в конце — из речи героини.

## Assets
- Исходник: Google Drive 1IlKJKx5IP0x1dSm8QT8AOH2aP2QOrZ7V (media/source.mp4, не в git)
- Референс стиля: Google Drive 1SzBkreT3oVEZWs6E_Yhre75RIQKM4b6n — кинетическая типографика, нумерованные карточки
- Музыка: "Advertime" (FreePD, CC0) — assets/music-advertime.mp3

## Pipeline
edit/pauses.py → edit/edl.py → edit/cut.py → edit/build.py → `npx hyperframes render --output out/picture.mp4` → edit/mix.sh
