# Указываем базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt из корневой папки внутрь контейнера
COPY ../requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все файлы из текущей директории внутрь контейнера
COPY . .

# Запускаем ваше приложение
CMD ["python", "App/main.py"]
