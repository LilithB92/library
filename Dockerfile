FROM python:3.13

WORKDIR /library

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt ./

# Устанавливаем зависимости через pip
RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

RUN mkdir -p library/staticfiles && chmod -R 755 library/staticfiles

# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
