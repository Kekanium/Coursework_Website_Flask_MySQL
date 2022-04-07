import json

from flask import Blueprint, request, render_template, session

from access import verifyUserDecorator
from sql.SqlMaster import SqlMaster

authApp = Blueprint('auth', __name__, template_folder='templates')
SqlMaster = SqlMaster(json.load(open('config/dataBaseConfig.json', 'r', encoding="utf-8")), r'./auth/requests')

LevelToName = {
    '0': 'Разработчик',
    '1': 'Администратор',
    '2': 'Директор',
    '3': 'Работник склада',
    '4': 'Заказчик'
}


@authApp.route('/', methods=['GET', 'POST'])
@verifyUserDecorator
def authIndex():
    if request.method == 'GET':
        return render_template('authIndex.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        result = SqlMaster.MakeRequest('CheckForLoginAndPassword.sql', Login=login, PasswordL=password)

        if len(result) == 0:
            return render_template('authFailed.html')
        else:
            session['groupName'] = LevelToName[f"{result[0]['AccessLevel']}"]
            return render_template('authSuccessfully.html', name=session['groupName'])


@authApp.route('/unauth')
@verifyUserDecorator
def authDeauthorize():
    session.clear()
    return render_template('authDeauthorize.html', name='Посетитель')
