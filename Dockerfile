# 1. Python image
FROM python:3.11-slim

# 2. Zaruriy paketlarni o‘rnatish
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Ishchi katalog
WORKDIR /app

# 4. requirements.txt faylini nusxalash
COPY requirements.txt .

# 5. Paketlarni o‘rnatish
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Loyihani konteynerga nusxalash
COPY . .

# 7. Static fayllarni yig‘ish
RUN python manage.py collectstatic --noinput

# 8. Port (agar ishlatayotgan bo‘lsangiz)
EXPOSE 8000

# 9. Django serverni ishga tushirish
CMD ["gunicorn", "kindergarten_org.wsgi:application", "--bind", "0.0.0.0:8000"]

