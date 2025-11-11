# ============================================================================
# Multi-stage Dockerfile для Flask додатку на AWS App Platform
# Використано найкращі практики для production середовища
# ============================================================================

# ----------------------------------------------------------------------------
# Stage 1: Builder - встановлення залежностей та компіляція
# ----------------------------------------------------------------------------
FROM python:3.11-slim as builder

# Встановлюємо змінні середовища для Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Встановлюємо системні залежності, необхідні для компіляції
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію
WORKDIR /build

# Копіюємо файл залежностей (для кешування Docker)
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --user --no-cache-dir -r requirements.txt

# ----------------------------------------------------------------------------
# Stage 2: Runtime - фінальний образ
# ----------------------------------------------------------------------------
FROM python:3.11-slim

# Встановлюємо змінні середовища
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:$PATH" \
    PORT=8000

# Створюємо нерoot користувача для безпеки
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Встановлюємо тільки runtime залежності (без компіляторів)
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо встановлені залежності з builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Копіюємо код додатку
COPY . .

# Змінюємо власника всіх файлів на appuser
RUN chown -R appuser:appuser /app /home/appuser/.local

# Переходимо на нерoot користувача
USER appuser

# Відкриваємо порт (AWS App Platform використовує PORT зі змінної середовища)
# Примітка: EXPOSE приймає тільки число, але AWS App Platform ігнорує це і використовує PORT
EXPOSE 8000

# Healthcheck для моніторингу здоров'я контейнера
# Перевіряємо endpoint /health (який є в вашому додатку)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://localhost:{port}/health')" || exit 1

# Команда запуску - використовуємо gunicorn з підтримкою PORT
# Опції:
# --workers 4: кількість worker процесів (налаштуйте залежно від ресурсів)
# --threads 2: кількість потоків на worker
# --timeout 120: таймаут для обробки запиту (секунди)
# --max-requests 1000: максимум запитів на worker перед перезапуском (запобігає memory leaks)
# --max-requests-jitter 50: випадковий додаток до max-requests
# --preload: завантажує додаток до fork workers (швидший старт, менше пам'яті)
# --access-logfile -: логування до stdout
# --error-logfile -: помилки до stderr
# --log-level info: рівень логування
CMD exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-4} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-50} \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level ${LOG_LEVEL:-info} \
    wsgi:app

