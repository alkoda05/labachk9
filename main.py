#Импорт нужных библиотек
from flask import Flask, render_template, request, redirect, url_for
#для работы с базой данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Первичный ключ
    text = db.Column(db.String(200), nullable=False) #Строковое поле для хранения текста отзыва
    rate = db.Column(db.Integer, nullable=False) #Целоч. поле для хранения оценки отзыва

#Функция отображающая данные из index.html
@app.route('/')
def index():
    return render_template('index.html')

#
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    #Если POST то мы отправили новый отзыв
    if request.method == 'POST':
        text = request.form['text']
        rate = int(request.form['rate'])
        review = Review(text=text, rate=rate)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('reviews'))
    #Если GET то отображаются все отзывы
    else:
        reviews = Review.query.all()
        return render_template('reviews.html', reviews=reviews)

#Запуск сервера
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)