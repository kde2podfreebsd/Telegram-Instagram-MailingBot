# Указываем базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt из корневой папки внутрь контейнера
COPY ../requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем файл, который мы запускаем в CMD
COPY App/UserAgent/UserAgentSpamPlugin.py .

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH=$PYTHONPATH:/app

# Запускаем ваше приложение
CMD ["python3", "UserAgentSpamPlugin.py"]
