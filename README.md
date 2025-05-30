Mana siz so‘ragan professional va to‘liq `README.md` faylining chiroyli va markdown formatida yozilgan varianti:

---

````markdown
# 🎓 kindergarten_org

**`kindergarten_org`** — bu Django asosidagi bolalar bog'chasi boshqaruv tizimi bo‘lib, inventarizatsiya, ovqatlanish, foydalanuvchi va hisobot modullarini o‘z ichiga oladi. Loyihada asinxron ishlarni bajarish uchun **Celery** va **Redis** ishlatilgan.

---

## 📦 Talablar (Requirements)

- Python 3.10+
- Django 4.x
- Redis-server
- Celery
- Eventlet
- Docker (ixtiyoriy)

---

## 🚀 Loyihani ishga tushirish

### 1. Redis-serverni ishga tushirish

Agar sizda Redis o‘rnatilgan bo‘lsa, quyidagi buyruq orqali uni ishga tushiring:

```bash
redis-server
````

> ℹ️ Bu Celery uchun **broker** sifatida ishlaydi.

---

### 2. Celery Beat va Worker ishga tushirish

Ikkita terminal oynasida quyidagi buyruqlarni bajaring:

#### ➤ Beat:

```bash
celery -A kindergarten_org beat --loglevel=info
```

#### ➤ Worker:

```bash
celery -A kindergarten_org worker --pool=eventlet --loglevel=info
```

---

### 3. Django serverini ishga tushirish

Uchinchi terminalda:

```bash
python manage.py runserver
```

---

### 4. Brauzerda ochish

Brauzeringizda quyidagi manzilga kiring:

```
http://127.0.0.1:8000
```

---

## ⚙️ Docker orqali ishga tushirish (ixtiyoriy)

```bash
docker-compose build
docker-compose up
```

---

## 🔧 Loyihaning asosiy imkoniyatlari

* ✅ Inventarizatsiyani boshqarish
* ✅ Ovqatlanish rejalari va kuzatuvi
* ✅ Har oy uchun PDF hisobotlar
* ✅ Foydalanuvchilar va rollarni boshqarish
* ✅ Asinxron vazifalar uchun Celery integratsiyasi

---

## 📁 Loyihaning tuzilmasi

```bash
kindergarten_org/
├── app/
├── custom_celery_beat/
├── inventory/
├── kindergarten_org/       # Django settings
├── logs/
├── meals/
├── media/
├── reports/
├── static/
├── staticfiles/
├── templates/
├── tests/
├── users/
├── db.sqlite3
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
└── manage.py
```

---

## 📜 Litsenziya

Bu loyiha ochiq manbali va istalgan maqsadda foydalanish uchun mo‘ljallangan.

```

---

Agar logotip, badge yoki havolalar kerak bo‘lsa, ular ham qo‘shib beraman. Yana nima kerak bo‘lsa, bemalol so‘rashingiz mumkin.
```
