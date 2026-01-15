release : python manage.py migrate 
web : waitress-serve --port=$PORT storefront.wsgi:application
worker : celery -A <nama-project> worker 
