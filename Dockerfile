# Используем официальный Python-образ как базовый
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Указываем команду для запуска сервера Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "D.Z.30.1.wsgi:application"]
