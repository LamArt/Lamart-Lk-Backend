# Lamart-performance-review
Личный кабинет для ООО "Ламарт" и платформа для performance review
## Deploy
create virtual enviroment from requirements.txt

powershell: 
`cd lamart_lk`
`python manage.py makemingrations`
`python manage.py migrate`
`python manage.py createsuperuser`
`python manage.py runserver`
done!

## Docs
After depoying watch API doc here -> http://127.0.0.1:8000/redoc/ or http://127.0.0.1:8000/swagger/

## Authentication
API uses bearer JWT authentication, read docs for more info.
1) For login or sign up: exchange provider oauth token* to refresh and acess jwt /auth/exchange_token/
2) Refresh the access token if it's no longer valid by using /auth/refresh/
3) Revresh token expires after 12 hours, do step 1 to get new.

* Yandex is the only provider available now.
dev token: https://oauth.yandex.ru/authorize?response_type=token&client_id=c120ba35adaf4278a8277e542b1a0cbd
"acess_token" param in response url is what you looking for