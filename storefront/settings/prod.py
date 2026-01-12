from .common import *
import os 
from dotenv import load_dotenv

load_dotenv()
DEBUG = False 
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = []
