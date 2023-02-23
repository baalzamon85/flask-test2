from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # отключаем т.к. этот мод не поддерживается
db = SQLAlchemy(app)


class Article(db.Model): # Создаем класс который представляет собой табл. БД где мы будем хранить записи(класс Article наследует все от объекта "db")
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # nullable=False - не позволяет создавать пустое поле title
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow) # default - по умолчанию добавляет настоящее время если оно не указано вручную

    def __repr__(self):  # эта функция указывает на то что когда мы выбираем какой-либо обьект класса Article нам будет выдаваться сам обьект и + его id
        return '<Article %r>' % self.id

# после создания класса Article создаем БД в терминале "python" --> "from app import db" --> "db.create_all()"--> "exit()"

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()  # создаем обьект articles в который отбираем данные из таблицы Article  и сортируем их по дате  и при помощи desc в начало выводим более новые
    return render_template("posts.html", articles=articles) # передаем в шаблон articles список articles для дальнейшей его обработки далее см. "создание шаблона"


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/del')   # создаем обработку удаления статей
def posts_delete(id):
    article = Article.query.get_or_404(id)
    
    try:
        db.session.delete(article)  #обращаемся к БД  и методу "delete" для удаления записи "article" из таблицы
        db.session.commit()  # обращаемся к БД и методу commit  для обновления БД
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])  #  # создаем обработку редактирования статей
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)



@app.route('/create-article', methods=['POST', 'GET'])
def create_articale():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":  # запуск приложения
    app.run(debug=False)