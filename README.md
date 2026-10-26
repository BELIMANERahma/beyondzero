# ما وراء الصفر | Beyond Zero
لعبة مغامرات تعليمية مبنية على قصة «ما وراء الصفر». تحلّ مسائل الأرقام والصفر لفتح الأبواب، وتهرب من حراس الملك زيركان.
An educational adventure game: solve number/zero puzzles to open doors, dodge guards, reach the gate.

## التشغيل | Run
1. ثبّت Python 3.9+ من python.org (ضع علامة Add to PATH)
2. في هذا المجلد افتح الطرفية (Terminal / CMD) ونفّذ:
```
pip install -r requirements.txt
python main.py
```

## التحكم | Controls
- الأسهم أو WASD: الحركة | P: إيقاف مؤقت | 1-4 أو الفأرة: الإجابة | Esc: القائمة

## إنشاء ملف تنفيذي (exe) | Build a standalone app
```
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "assets;assets" main.py      (Windows)
pyinstaller --noconsole --onefile --add-data "assets:assets" main.py      (Mac / Linux)
```
ستجد اللعبة في مجلد dist.  (ملاحظة: questions.py يتم تضمينه تلقائيًا)

## الملفات | Files
- main.py: كود اللعبة | questions.py: بنك الأسئلة (أضف أسئلتك بسهولة!) | assets/: الخط
