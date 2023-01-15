# Исходный код для дипломной работы: Менеджер задач


## Описание проекта


## Используемый стэк:

  python3.10, Django, Postgresql

### Клонировать репозиторий

```sh
git clone https://github.com/Specially4/todolist.git
```

### Установка зависимостей
```shell
pip install -r requirements.txt
```

### Start DB

```sh
docker-compose up --build -d
```

### Roll up migrations

```sh
python manage.py migrate
```

### Create superuser

```sh
python manage.py createsuperuser
```

### Run app


```sh
python manage.py runserver
```
