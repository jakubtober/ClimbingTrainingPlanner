# It's local settings definition, please don't change this file

# 1. Copy file and rename as 'settings_local.py'
# 2. Set all options
# 3. Go to a project path, with '.git' directory
# 4. Type command in terminal to avoid adding local setting to repository:
#    echo "lend_n_borrow/settings_local.py" >> .git/info/exclude

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4%^_+c8o%o$pg@729ipph-qvso753p9r4d*(lh*#9!3j)r_hei'

DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
    '.ngrok.io',
]

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'NAME': 'climbing_training',
        'PASSWORD': 'coderslab',
        'OPTIONS': {
            'autocommit': True,
        }
    }
}
