import pickle
from flask import render_template, session, redirect, request

from app import app, db
from models import Review, Review_rus
from forms import ReviewForm
from preprocess import preprocess_text, preprocess_text_rus

#Загрузим модель и векторизацию
vectorizer = pickle.load(open('bow_vectorizer.pickle','rb'))
model = pickle.load(open('model.pickle','rb'))
vectorizer_rus = pickle.load(open('bow_vectorizer_rus.pickle','rb'))
model_rus = pickle.load(open('model_rus.pickle','rb'))

#получить класс по тексту 0 - не понравилось, 1 - понравилось
def get_sentiment(text):
    result = dict()
    result['origin_text']=text

    #получить вектор из предобработанного текста
    proc_text = preprocess_text(text)
    result['proc_text']=proc_text

    vector = vectorizer.transform([proc_text])

    sentiment = model.predict(vector)
    result['sentiment']=int(sentiment[0])

    sentiment_proba = model.predict_proba(vector)
    result['sentiment_proba_neg']=sentiment_proba[0][0].round(2)
    result['sentiment_proba_pos']=sentiment_proba[0][1].round(2)

    return result

#получить класс по тексту 0 - не понравилось, 1 - понравилось
def get_sentiment_rus(text):
    result = dict()
    result['origin_text']=text

    #получить вектор из предобработанного текста
    proc_text = preprocess_text_rus(text)
    result['proc_text']=proc_text

    vector = vectorizer_rus.transform([proc_text])

    sentiment = model_rus.predict(vector)
    result['sentiment']=int(sentiment[0])

    sentiment_proba = model_rus.predict_proba(vector)
    result['sentiment_proba_neg']=sentiment_proba[0][0].round(2)
    result['sentiment_proba_pos']=sentiment_proba[0][1].round(2)

    return result
# Главная страница выбора анализа
@app.route('/')
def home():
    return render_template('index.html')

# #Главная страница английского анализа
@app.route('/english_anal/',  methods=["GET", "POST"])
def english_anal():

    form = ReviewForm()
    if form.validate_on_submit() and (request.method == "POST"):
        review = (form.review.data)
        reviews = session.get('reviews', [])
        reviews.append(review)
        session['reviews'] = reviews

        sent_an = get_sentiment(review)
        new_review = Review(
            origin_text=review,
            sentiment=sent_an['sentiment'],
            sentiment_proba_neg = sent_an['sentiment_proba_neg'],
            sentiment_proba_pos = sent_an['sentiment_proba_pos'])
        db.session.add(new_review)
        db.session.commit()


        return redirect(f'/result/{new_review.id}/')

    output = render_template('main.html', form=form)
    return output

#Страница результата анализа
@app.route('/result/<int:id>/')
def get_result(id):
    db_review = db.session.query(Review).get_or_404(id)
    
    #просить ли валидировать ответ модели
    answer_exist = False
    if db_review.check_answer is not None:
        answer_exist = True
    
    #благодарить ли за валидацию или уже благодарили
    show_thanks = False
    review_thanks = session.get('review_thanks',[])
    if answer_exist and len(review_thanks)>0:
        _ = session['review_thanks'].pop()
        show_thanks = True

    output = render_template('result.html',  res=db_review, answer_exist=answer_exist, show_thanks=show_thanks)
    return output

@app.route('/answer/<int:id>/<int:answer>/')
def get_answer(id, answer):
    db_review = db.session.query(Review).get_or_404(id)
    db_review.check_answer = bool(answer)
    db.session.commit()

    review_thanks = session.get('review_thanks',[])
    review_thanks.append('thanks')
    session['review_thanks'] = review_thanks

    return redirect(f'/result/{id}/')

@app.route('/previous_analysis/')
def get_previous():
    all_reviews = db.session.query(Review).filter(Review.check_answer!=None)
    true_count = 0
    count = 0
    for rev in all_reviews:
        if rev.check_answer == True:
            true_count += 1
        count += 1
    if count == 0:
        return 'No previous analysis in the database. Sorry'
    accuracy = round((true_count/count),2)
    results = all_reviews = db.session.query(Review).filter(Review.check_answer!=None).order_by(Review.id.desc()).limit(5)

    output = render_template('previous.html', results=results, accuracy=accuracy)
    return output

@app.route('/about/')
def get_about():
    my_dict={'Rus':'rus','Eng':'eng'}
    return render_template('about.html', my_dict=my_dict)

#Главная для русского анализа
@app.route('/russian_anal/',  methods=["GET", "POST"])
def russian_anal():

    form = ReviewForm()
    if form.validate_on_submit() and (request.method == "POST"):
        review = (form.review.data)
        reviews = session.get('reviews', [])
        reviews.append(review)
        session['reviews'] = reviews

        sent_an = get_sentiment_rus(review)
        new_review = Review_rus(
            origin_text=review,
            sentiment=sent_an['sentiment'],
            sentiment_proba_neg = sent_an['sentiment_proba_neg'],
            sentiment_proba_pos = sent_an['sentiment_proba_pos'])
        db.session.add(new_review)
        db.session.commit()


        return redirect(f'/result_rus/{new_review.id}/')

    output = render_template('main_rus.html', form=form)
    return output

#Страница результата анализа на русском
@app.route('/result_rus/<int:id>/')
def get_result_rus(id):
    db_review = db.session.query(Review_rus).get_or_404(id)
    
    #просить ли валидировать ответ модели
    answer_exist = False
    if db_review.check_answer is not None:
        answer_exist = True
    
    #благодарить ли за валидацию или уже благодарили
    show_thanks = False
    review_thanks = session.get('review_thanks',[])
    if answer_exist and len(review_thanks)>0:
        _ = session['review_thanks'].pop()
        show_thanks = True

    output = render_template('result_rus.html',  res=db_review, answer_exist=answer_exist, show_thanks=show_thanks)
    return output

#ендпойнт обработки клика на фидбэк по результату для русского анализа
@app.route('/answer_rus/<int:id>/<int:answer>/')
def get_answer_rus(id, answer):
    db_review = db.session.query(Review_rus).get_or_404(id)
    db_review.check_answer = bool(answer)
    db.session.commit()

    review_thanks = session.get('review_thanks',[])
    review_thanks.append('thanks')
    session['review_thanks'] = review_thanks

    return redirect(f'/result_rus/{id}/')

@app.route('/previous_analysis_rus/')
def get_previous_rus():
    all_reviews = db.session.query(Review_rus).filter(Review_rus.check_answer!=None)
    true_count = 0
    count = 0
    for rev in all_reviews:
        if rev.check_answer == True:
            true_count += 1
        count += 1
    if count == 0:
        return 'No previous analysis in the database. Sorry'
    accuracy = round((true_count/count),2)
    results = all_reviews = db.session.query(Review_rus).filter(Review_rus.check_answer!=None).order_by(Review_rus.id.desc()).limit(5)

    output = render_template('previous_rus.html', results=results, accuracy=accuracy)
    return output