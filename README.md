# Lamart-performance-review

Личный кабинет для ООО "Ламарт" и платформа для performance review

## Deploy

1) clone from git
2) switch to dev
3) create, active venv
4) create .env and local_settings.py
5) в .env поменять POSTGRES_HOST="db" на "localhost"
6) open docker dekctop
7) in terminal: `docker-compose up --build -d`
7) `cd lamart_lk` `python manage.py makemigrations` `python manage.py migrate`
8) создать админа, если надо
9) вернуть db в шаге 5
10) `docker-compose up --build`

## Docs

After deploying watch API doc here -> http://127.0.0.1:8000/redoc/ or http://127.0.0.1:8000/swagger/

## Authentication

API uses bearer JWT authentication, read docs for more info.

1) For login or sign up: exchange provider oauth token* to refresh and acess jwt /auth/exchange_token/
2) Refresh the access token if it's no longer valid by using /auth/refresh/
3) Refresh token expires after 12 hours, do step 1 to get new.

* Yandex is the only provider available now.
  dev token: https://oauth.yandex.ru/authorize?response_type=token&client_id=c120ba35adaf4278a8277e542b1a0cbd
  "access_token" param in response url is what you looking for

## Atlassian Provider

To connect Jira as provider you need:

1) Create a new app in [Developer Console](https://developer.atlassian.com/console/myapps/)
2) Add all permissions with Jira API like read and etc, but no more 50 scopes.
3) Open "Authorization" in left menu, configure OAuth 2.0
4) You need to take URL from "Classic Jira platform REST API authorization URL"
5) Add in your URL new param "offline_access" to the scope parameter, it will be looks like: '
   %3Ajira-data-provider%20offline_access&redirect_uri'. You can past it to the right place, all the difference is in
   the offline access parameter.
6) After accepting all accesses "code=" param is what you need.
7) Exchange your authorization code to JWT token by auth/exchange_token/

* Only for developer url to take JIRA authorization code:

  https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=OFe6NSNJiBJypHiGeEMinCsohVPFfXAV&scope=read%3Ajira-work%20manage%3Ajira-project%20manage%3Ajira-configuration%20read%3Ajira-user%20write%3Ajira-work%20manage%3Ajira-webhook%20manage%3Ajira-data-provider%20offline_access&redirect_uri=http%3A%2F%2Flocalhost%3A5004%2Fsalary&state=${YOUR_USER_BOUND_VALUE}&response_type=code&prompt=consent
