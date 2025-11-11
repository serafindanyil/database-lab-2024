# 🚀 Docker Quick Start

## Локальне тестування

### 1. Збірка образу

```bash
docker build -t database-lab-2024 .
```

### 2. Запуск контейнера

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="mysql+mysqlconnector://user:password@host:port/dbname" \
  -e SECRET_KEY="your-secret-key" \
  -e PORT=8000 \
  database-lab-2024
```

### 3. Перевірка роботи

```bash
# Healthcheck
curl http://localhost:8000/health

# Або відкрийте в браузері
open http://localhost:8000/health
```

## Тестування з .env файлом

```bash
docker run -p 8000:8000 \
  --env-file .env \
  database-lab-2024
```

## Перевірка розміру образу

```bash
docker images database-lab-2024
```

Очікуваний розмір: ~200-300 MB

## Перевірка логів

```bash
docker logs <container_id>
```

## Вхід в контейнер

```bash
docker exec -it <container_id> /bin/bash
```

## Очищення

```bash
# Зупинити контейнер
docker stop <container_id>

# Видалити контейнер
docker rm <container_id>

# Видалити образ
docker rmi database-lab-2024
```

---

## AWS App Platform Deployment

1. Пуште код у репозиторій (GitHub/GitLab/Bitbucket)
2. Створіть App в AWS App Platform
3. Підключіть репозиторій
4. Налаштуйте змінні середовища
5. Деплой!

Детальні інструкції див. в `DOCKER_GUIDE.md`

