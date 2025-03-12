

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:J!strM3str@localhost/mechanic_shop_db'
    DEBUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass