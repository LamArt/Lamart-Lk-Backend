# Lamart-performance-review

Личный кабинет для ООО "Ламарт" и платформа для performance review

## Deploy

1) Create [.env](.env.example)
2) Run docker
3) In terminal: `docker-compose up --build`

## Api Docs

After deploying you can find API docs here -> [Redoc](http://127.0.0.1:8000/redoc/) or [Swagger](http://127.0.0.1:8000/swagger/)

## Development

1. Create virtualenv
```
python -m venv [path to venv folder]
```
2. Activate virtualenv
```
source [path to venv folder]/Scripts/activate
```
3. Install requirements.
```
pip install -r requirements/local.txt
```
4. Set POSTGRES_HOST="localhost" in .env
5. Run db
```
docker-compose up db --build -d
```
6. Make migrations, migrate and run server
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
``` 

## Authentication

API uses bearer JWT authentication, read API docs for more info.

1) For login or sign up: exchange provider [oauth token](https://yandex.ru/dev/id/doc/en/access)* to refresh and acess jwt /auth/exchange_token/
2) Refresh the access token if it's no longer valid by using /auth/refresh/
3) Refresh token expires after 12 hours, do step 1 to get new.
* Yandex is the only provider available now.
  
## Atlassian Provider

To connect Jira you need:

1) Create a new app in [Developer Console](https://developer.atlassian.com/console/myapps/)
2) Add all permissions with Jira API like read and etc, but no more 50 scopes.
3) Open "Authorization" in left menu, configure OAuth 2.0
4) You need to take URL from "Classic Jira platform REST API authorization URL"
5) Add in your URL new param "offline_access" to the scope parameter, it will be looks like: '
   %3Ajira-data-provider%20offline_access&redirect_uri'. You can past it to the right place, all the difference is in
   the offline access parameter.
6) After accepting all accesses "code=" param is what you need.
7) Exchange your authorization code to JWT token by auth/get_token_jira/
