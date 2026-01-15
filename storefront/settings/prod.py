from .common import *
import os 
from dotenv import load_dotenv
import dj_database_url

load_dotenv()
DEBUG = False 
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        dj_database_url.config()
    }
}
