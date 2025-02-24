# Используем легковесный образ на основе Debian
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем только необходимые файлы
COPY convert-bot.py /app/
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Указываем, что токен будет передаваться через переменные окружения
ENV TOKEN=""

# Запускаем бота
CMD ["python", "convert-bot.py"]
