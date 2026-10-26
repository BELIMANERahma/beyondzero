# ما وراء الصفر | Beyond Zero
لعبة مغامرات تعليمية (السنة الثانية متوسط) مبنية على قصة «ما وراء الصفر».
An educational adventure for 2ème année moyenne: open doors by solving lessons, avoid enemies, reach the gate.

## التشغيل | Run
```
python -m venv venv
venv\Scripts\activate          (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python main.py
```

## التحكم | Controls
- الأسهم أو WASD: الحركة | 1-4 أو الفأرة: الإجابة | Esc: إيقاف مؤقت | F11: ملء الشاشة | M: كتم الصوت
- النافذة قابلة لتغيير الحجم بالسحب.

## المراحل والدروس | Levels & lessons
1. الأرشيف: سلاسل الجمع والطرح، أولويات العمليات، الأقواس
2. النفق: الأقواس العشرية وحاصل القسمة، خاصية توزيع الضرب على الجمع والطرح
3. المكتبة: لغة عربية + مقارنة الكسور وجمعها وطرحها
4. قاعة الحاسوب: معالج النصوص (إدراج الجداول، الأسطر والأعمدة، دمج الخلايا، الحدود)
5. المخبر: علوم + القسمة الإقليدية والقسمة العشرية
6. البوابة: أسئلة من كل المواد
7. ذكرى أول نوفمبر 1954: مرحلة خاصة بأسئلة التاريخ والحساب (من القائمة الرئيسية)

## إضافة أسئلة | Add questions
افتح questions.py وأضف سؤالًا إلى القائمة المناسبة بالشكل:
("النص", ["خيار1","خيار2","خيار3","خيار4"], رقم_الإجابة_الصحيحة, "الشرح")
استعمل {…} حول العمليات الحسابية والكلمات اللاتينية لتظهر بالاتجاه الصحيح، مثل {3/4 + 1/4}.

## إنشاء ملف تنفيذي | Build a standalone app
```
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "assets;assets" main.py      (Windows)
pyinstaller --noconsole --onefile --add-data "assets:assets" main.py      (Mac / Linux)
```
## الملفات | Files
main.py (اللعبة) | gfx.py (الرسوم والشخصيات) | cutscene.py (المشاهد المتحركة) | questions.py (الأسئلة) | assets/ (الخط)
يُحفظ التقدّم تلقائيًا في ملف .beyond_zero_save.json داخل مجلد المستخدم.

## جعل اللعبة قابلة للتثبيت | Make it installable
1. Windows: انقر مرتين على build_windows.bat ← ينتج dist\BeyondZero\BeyondZero.exe (يعمل دون Python).
2. لإنشاء ملف تثبيت BeyondZero_Setup.exe: ثبّت Inno Setup ثم افتح installer.iss واضغط Compile.
3. Mac/Linux: شغّل build_mac_linux.sh.

## الحصول على ملف .exe و .apk تلقائيًا | Get .exe and .apk automatically (GitHub)
1. أنشئ حسابًا مجانيًا على github.com ثم مستودعًا جديدًا (New repository) وارفع كل ملفات هذا المجلد.
2. افتح تبويب Actions ← Build installers ← Run workflow.
3. بعد دقائق (الـ exe) أو ~30 دقيقة (الـ apk) نزّل الملفات من Artifacts:
   BeyondZero-Windows (فيه BeyondZero_Setup.exe) و BeyondZero-Android (فيه ملف apk).
4. على الهاتف: انقل الـ apk وفعّل «التثبيت من مصادر غير معروفة». للتجربة على الحاسوب بأزرار اللمس: python main.py --touch
