# Lamart-performance-review
Личный кабинет для ООО "Ламарт" и платформа для performance review
## Deploy
create virtual enviroment from requirements.txt

powershell: 
`cd lamart_lk`
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py createsuperuser`
`python manage.py runserver`
done!

## Docs
After deploying watch API doc here -> http://127.0.0.1:8000/redoc/ or http://127.0.0.1:8000/swagger/

## Authentication
API uses bearer JWT authentication, read docs for more info.
1) For login or sign up: exchange provider oauth token* to refresh and acess jwt /auth/exchange_token/
2) Refresh the access token if it's no longer valid by using /auth/refresh/
3) Revresh token expires after 12 hours, do step 1 to get new.

* Yandex is the only provider available now.
dev token: https://oauth.yandex.ru/authorize?response_type=token&client_id=c120ba35adaf4278a8277e542b1a0cbd
"acess_token" param in response url is what you looking for

## Atlassian Provider
To connect Jira as provider you need:
1) Create a new app in [Developer Console](https://developer.atlassian.com/console/myapps/)
2) Add all permissions with Jira API like read and etc, but no more 50 scopes.
3) Open "Authorization" in left menu, configure OAuth 2.0
4) You need to take URL from "Classic Jira platform REST API authorization URL"
5) Add in your URL new param: 'Ajira-data-provider%20offline_access&
redirect_uri='. You can past it to the right place, all the difference is in the offline access parameter.
6) After accepting all accesses "code=" param is what you need
7) Exchange your authorization code to JWT token by auth/exchange_token/