from flask import Flask, render_template, url_for, request, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'beaberaberfgbrtgbrfgbfg'

menu = [{'name': 'Главная', 'url': 'index'},
        {'name': 'О сайте', 'url': 'about'},
        {'name': 'Обратная связь', 'url': 'write_us'},
        ]


@app.route('/index')
@app.route('/')
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route('/about')
def about():
    print(url_for('about'))
    return render_template('about.html', menu=menu)


@app.route('/write_us', methods=['POST', 'GET'])
def write_us():
    if request.method == 'POST':
        if len(request.form["username"]) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки формы', category='error')
        print(request.form)
    return render_template('write_us.html', menu=menu, title='Обратная связь')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'Bastos' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title='Авторизация', menu=menu)


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя {username}"


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu), 404


@app.errorhandler(401)
def pageNotFound(error):
    return render_template('page401.html', title='Данные недоступны', menu=menu), 404


if __name__ == '__main__':
    app.run()
