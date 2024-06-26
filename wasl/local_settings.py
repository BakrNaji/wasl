# local_settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_local_db_name',
        'USER': 'your_local_db_user',
        'PASSWORD': 'your_local_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
