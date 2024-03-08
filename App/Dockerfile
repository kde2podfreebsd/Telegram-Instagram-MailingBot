# Указываем базовый образ
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл requirements.txt из корневой папки внутрь контейнера
COPY ./requirements.txt  .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем все файлы из текущей директории внутрь контейнера
COPY . .

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH=$PYTHONPATH:/app

# Запускаем ваше приложение
CMD ["python3", "App/Bot/main.py"]
