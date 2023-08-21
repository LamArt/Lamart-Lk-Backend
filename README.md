# Lamart-performance-review
Личный кабинет для ООО "Ламарт" и платформа для performance review
## Deploy
use powershell: cd lamart_lk
then create virtual enviroment from requirements.txt

powershell: `python manage.py makemingrations`
`python manage.py migrate`
`python manage.py createsuperuser`
`python manage.py runserver`
done!

## Docs
After depoying watch API doc here -> http://127.0.0.1:8000/redoc/
