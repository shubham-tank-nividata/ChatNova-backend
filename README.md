# ChatNova-backend

## setup

to setup virtual environment and installing dependencies run following command in root directory :

```
pipenv install
```

in case you don't have pipenv install it using pip

```
pip install pipenv
```

activate virtual environment using

```
pipenv shell
```

then run migrations :

```
python manage.py migrate
```

after that run server :

```
python manage.py runserver
```
