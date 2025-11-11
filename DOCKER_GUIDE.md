# 🐳 Docker Guide для AWS App Platform

## Огляд

Цей документ пояснює ключові моменти Dockerfile та як правильно задеплоїти додаток на AWS App Platform.

---

## 📋 Ключові моменти Dockerfile

### 1. **Multi-stage Build** (Багатостадійна збірка)

```dockerfile
FROM python:3.11-slim as builder
# ... встановлення залежностей ...
FROM python:3.11-slim
# ... фінальний образ ...
```

**Чому це важливо:**
- **Зменшення розміру образу**: компілятори (gcc, g++) залишаються тільки в builder stage
- **Безпека**: фінальний образ містить тільки runtime залежності
- **Швидкість**: менший образ = швидше завантаження та розгортання

**Розмір оптимізації:**
- Builder stage: ~500-700 MB (з компіляторами)
- Runtime stage: ~200-300 MB (без компіляторів)
- **Економія: ~50% розміру образу**

---

### 2. **Безпека: Non-root User**

```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

**Чому це важливо:**
- Запуск від імені root користувача = критична вразливість безпеки
- Якщо контейнер зламають, зловмисник отримає root доступ
- Best practice: завжди використовувати нерoot користувача

**Як це працює:**
- Створюється системний користувач `appuser` без домашньої директорії (`-r`)
- Всі файли додатку належать `appuser`
- Контейнер запускається від імені `appuser`

---

### 3. **Кешування Docker Layers**

```dockerfile
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
# ...
COPY --chown=appuser:appuser . .
```

**Чому порядок важливий:**
- Docker кешує кожен layer (шар)
- Якщо `requirements.txt` не змінився, Docker використовує кешований layer
- Код копіюється останнім, тому зміни в коді не перебудовують залежності

**Результат:**
- Зміна коду → швидка перебудова (тільки останній layer)
- Зміна залежностей → повна перебудова (очікувано)

---

### 4. **Змінні середовища для Python**

```dockerfile
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
```

**Пояснення:**
- `PYTHONUNBUFFERED=1`: вимикає буферизацію виводу (логи відображаються миттєво)
- `PYTHONDONTWRITEBYTECODE=1`: не створює `.pyc` файли (менший образ)

---

### 5. **Healthcheck**

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://localhost:{port}/health')" || exit 1
```

**Що це робить:**
- Кожні 30 секунд перевіряє endpoint `/health`
- Якщо 3 спроби неуспішні → контейнер позначається як unhealthy
- `--start-period=40s`: дає час на старт додатку перед перевірками

**Чому це важливо:**
- AWS App Platform використовує healthcheck для моніторингу
- Автоматичний перезапуск нездорових контейнерів
- Load balancer не направляє трафік на unhealthy контейнери

---

### 6. **Gunicorn Configuration**

```dockerfile
CMD exec gunicorn \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-4} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout ${GUNICORN_TIMEOUT:-120} \
    --max-requests ${GUNICORN_MAX_REQUESTS:-1000} \
    --max-requests-jitter ${GUNICORN_MAX_REQUESTS_JITTER:-50} \
    --preload \
    wsgi:app
```

**Ключові параметри:**

| Параметр | Значення | Пояснення |
|----------|----------|-----------|
| `--bind 0.0.0.0:$PORT` | 0.0.0.0:8000 | Слухає на всіх інтерфейсах, порт зі змінної середовища |
| `--workers 4` | 4 | Кількість worker процесів (налаштуйте за ресурсами) |
| `--threads 2` | 2 | Кількість потоків на worker |
| `--timeout 120` | 120 сек | Максимальний час обробки запиту |
| `--max-requests 1000` | 1000 | Перезапуск worker після N запитів (запобігає memory leaks) |
| `--max-requests-jitter 50` | 50 | Випадковий додаток до max-requests (уникає одночасних перезапусків) |
| `--preload` | - | Завантажує додаток до fork (швидший старт, менше пам'яті) |

**Формула для workers:**
```
workers = (2 × CPU cores) + 1
```
Наприклад, для 2 CPU cores: `(2 × 2) + 1 = 5 workers`

---

### 7. **Порт для AWS App Platform**

```dockerfile
ENV PORT=8000
EXPOSE 8000
CMD exec gunicorn --bind 0.0.0.0:${PORT:-8000} ...
```

**Важливо:**
- AWS App Platform автоматично встановлює змінну `PORT`
- Додаток **обов'язково** повинен слухати на `0.0.0.0` (не `127.0.0.1`)
- `EXPOSE` - це тільки документація, AWS ігнорує це і використовує `PORT`

---

## 🚀 Деплой на AWS App Platform

### Крок 1: Підготовка

1. **Переконайтеся, що у вас є:**
   - Dockerfile в корені проекту
   - `.dockerignore` файл
   - Всі залежності в `requirements.txt`

2. **Налаштуйте змінні середовища в AWS App Platform:**
   ```
   DATABASE_URL=mysql+mysqlconnector://user:password@host:port/dbname
   SECRET_KEY=your-secret-key-here
   FLASK_APP=app:create_app
   ```

### Крок 2: Створення App на AWS

1. Відкрийте AWS App Platform консоль
2. Створіть новий App
3. Виберіть "Docker" як платформу
4. Підключіть репозиторій (GitHub/GitLab/Bitbucket)
5. Вкажіть Dockerfile шлях (зазвичай `/Dockerfile`)

### Крок 3: Налаштування Environment Variables

Додайте наступні змінні середовища:

```
# Database
DATABASE_URL=mysql+mysqlconnector://user:password@host:port/dbname
# або окремо:
DB_USER=your_db_user
DB_PASS=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
DB_NAME=your_db_name

# Flask
SECRET_KEY=your-very-secret-key-here
FLASK_APP=app:create_app
FLASK_ENV=production

# Gunicorn (опціонально)
GUNICORN_WORKERS=4
GUNICORN_THREADS=2
GUNICORN_TIMEOUT=120
LOG_LEVEL=info
```

### Крок 4: Налаштування ресурсів

- **CPU**: мінімум 1 vCPU (рекомендовано 2+)
- **RAM**: мінімум 512 MB (рекомендовано 1 GB+)
- **Workers**: налаштуйте `GUNICORN_WORKERS` залежно від CPU

### Крок 5: Деплой

1. Зробіть commit і push у ваш репозиторій
2. AWS App Platform автоматично почне збірку
3. Після успішної збірки додаток буде розгорнуто

---

## 🔧 Налаштування для Production

### 1. База даних

Переконайтеся, що:
- База даних доступна з AWS App Platform
- Використовується SSL/TLS з'єднання (якщо можливо)
- Налаштовані connection pooling параметри:
  ```python
  DB_POOL_SIZE=5
  DB_MAX_OVERFLOW=10
  DB_POOL_RECYCLE=280
  ```

### 2. Міграції бази даних

Додайте команду для міграцій у AWS App Platform (Build Command):
```bash
flask db upgrade
```

Або створіть окремий job для міграцій.

### 3. Логування

- Всі логи (stdout/stderr) автоматично збираються AWS CloudWatch
- Використовуйте структуроване логування для кращого моніторингу

### 4. Моніторинг

- Використовуйте CloudWatch для моніторингу метрик
- Налаштуйте алерти на помилки та високе навантаження
- Перевіряйте healthcheck endpoint регулярно

---

## 🐛 Troubleshooting

### Проблема: Додаток не запускається

**Можливі причини:**
1. Неправильний порт: переконайтеся, що використовується `0.0.0.0:$PORT`
2. Помилки в базі даних: перевірте `DATABASE_URL`
3. Відсутні залежності: перевірте `requirements.txt`

**Рішення:**
```bash
# Перевірте логи в AWS CloudWatch
# Перевірте змінні середовища
# Тестуйте локально: docker build -t myapp . && docker run -p 8000:8000 myapp
```

### Проблема: Healthcheck fails

**Можливі причини:**
1. Endpoint `/health` не існує або повертає помилку
2. Додаток не встиг запуститися

**Рішення:**
- Перевірте, що endpoint `/health` повертає `200 OK`
- Збільште `--start-period` в HEALTHCHECK

### Проблема: Високе використання пам'яті

**Рішення:**
- Зменште кількість workers: `GUNICORN_WORKERS=2`
- Зменште `--max-requests` для частіших перезапусків
- Додайте більше RAM в AWS App Platform

---

## 📚 Додаткові ресурси

- [AWS App Platform Documentation](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/latest/deploying/)

---

## ✅ Чеклист перед деплоєм

- [ ] Dockerfile створено і протестовано локально
- [ ] `.dockerignore` налаштовано правильно
- [ ] Всі змінні середовища налаштовані в AWS
- [ ] База даних доступна з AWS App Platform
- [ ] Healthcheck endpoint працює
- [ ] Логи налаштовані правильно
- [ ] Міграції бази даних виконані
- [ ] SSL/TLS налаштовано (якщо потрібно)
- [ ] Моніторинг налаштовано

---

**Створено з ❤️ для production-ready деплою на AWS App Platform**

