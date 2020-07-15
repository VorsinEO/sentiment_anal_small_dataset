class Config:
    DEBUG = True
    SECRET_KEY= "secret_key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///reviews.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False