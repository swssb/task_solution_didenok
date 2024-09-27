# Password Manager API

## Описание
API для управления паролями с методами POST и GET.

### Как запустить проект

1. Склонируйте репозиторий

2. Запустите docker-compose
   ```bash
   docker-compose up --build
3. Используйте коллекции Postman(password_manager.postman_collection.yaml) или Swagger для проверки API 127.0.0.1:8000/swagger
4. Для запуска тестов используйте 
   ```bash
   docker-compose run --rm api sh -c "python manage.py migrate && pytest"
