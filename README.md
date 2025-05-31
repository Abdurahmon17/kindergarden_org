# 🎓 kindergarten_org

**`kindergarten_org`** — bu Django asosidagi bolalar bog'chasi boshqaruv tizimi bo‘lib, inventarizatsiya, ovqatlanish, foydalanuvchilar va hisobot modullarini o‘z ichiga oladi. Asinxron jarayonlar uchun **Celery** va **Redis**, konteynerlash uchun esa **Docker** texnologiyalaridan foydalanilgan.

---

## 📦 Talablar (Requirements)

- Python 3.10+
- Django 4.x
- Redis
- Celery
- Eventlet
- Docker (ixtiyoriy)

---

## 🚀 Ishga tushirish usullari

### 🖥 1. Mahalliy ishga tushirish (Local Run)

#### 1.1. Redis serverni ishga tushiring (Admin CMD orqali)

```bash
redis-server
```

> ℹ️ Redis — Celery uchun broker vazifasini bajaradi.

#### 1.2. Celery Beat va Worker’ni alohida terminallarda ishga tushiring

```bash
# Beat (davriy vazifalar uchun)
celery -A kindergarten_org beat --loglevel=info

# Worker (fon vazifalar uchun)
celery -A kindergarten_org worker --pool=eventlet --loglevel=info
```

#### 1.3. Django serverni ishga tushiring

```bash
python manage.py runserver
```

#### 1.4. Web ilovaga kirish

Brauzeringizda oching: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

### 🐳 2. Docker orqali ishga tushirish

Agar siz Docker’dan foydalanmoqchi bo‘lsangiz:

```bash
docker-compose build
docker-compose up
```

> `docker-compose.yml` va `Dockerfile` fayllari to‘g‘ri sozlangan bo‘lishi kerak.

---

## 🔧 Asosiy funksiyalar

- ✅ Inventarizatsiya boshqaruvi
- ✅ Ovqatlanish rejasi va statistikasi
- ✅ Foydalanuvchilar va rollarni boshqarish
- ✅ Oy yakunlari bo‘yicha PDF hisobotlar
- ✅ Celery yordamida fon vazifalar

---

## 📁 Loyihaning tuzilmasi

```bash
kindergarten_org/
├── app/
├── custom_celery_beat/
├── inventory/
├── kindergarten_org/       # Django konfiguratsiyasi
├── logs/
├── meals/
├── media/
├── reports/
├── static/
├── staticfiles/
├── templates/
├── users/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── entrypoint.sh
```

---

## 👨‍💻 Muallif

Abdurahmon17  
🔗 [GitHub profilingiz](https://github.com/Abdurahmon17)

---

## 📜 Litsenziya

Bu loyiha ochiq manbali bo‘lib, istalgan maqsadlarda foydalanish uchun ruxsat beriladi.

