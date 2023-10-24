import os
#database variables
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME','postgres')
DATABASE_PASSWORD= os.getenv('DATABASE_PASSWORD','1990')
DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'BigAPI')
