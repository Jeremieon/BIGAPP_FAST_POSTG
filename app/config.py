import os
#database variables
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME','postgres')
DATABASE_PASSWORD= os.getenv('DATABASE_PASSWORD','1990')
DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'BigAPI')
SECRET_KEY = os.getenv('SECRET_KEY','31df8a9d99142f097c48946d30dc87684acc9f06852517ddf7b2f77ba36d9eb4')
ALGORITHM = os.getenv("ALGORITHM","HS256")
#openssl rand -hex 32