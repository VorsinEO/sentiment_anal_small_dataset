from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Модель для хранения заказов
class Review(db.Model):
    #Таблица
    __tablename__='reviews'

    id = db.Column(db.Integer, primary_key=True)
    origin_text = db.Column(db.String(2000), nullable=False)
    sentiment = db.Column(db.Integer, nullable=False)
    sentiment_proba_neg = db.Column(db.Float, nullable=False)
    sentiment_proba_pos = db.Column(db.Float, nullable=False)
    check_answer = db.Column(db.Boolean, nullable=True)

class Review_rus(db.Model):
    #Таблица
    __tablename__='reviews_rus'

    id = db.Column(db.Integer, primary_key=True)
    origin_text = db.Column(db.String(2000), nullable=False)
    sentiment = db.Column(db.Integer, nullable=False)
    sentiment_proba_neg = db.Column(db.Float, nullable=False)
    sentiment_proba_pos = db.Column(db.Float, nullable=False)
    check_answer = db.Column(db.Boolean, nullable=True)