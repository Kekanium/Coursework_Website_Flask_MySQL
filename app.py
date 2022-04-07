import json

from flask import Flask, render_template, session

from access import verifyUserDecorator
from auth.routes import authApp
from basket.routes import basketApp
from edit.routes import editApp
from requests.routes import requestsApp

mainApp = Flask(__name__)

mainApp.config['ACCESS_CONFIG_MODULE'] = json.load(open('config/accessConfigModules.json', 'r', encoding="utf-8"))
mainApp.config['ACCESS_CONFIG_PAGE'] = json.load(open('config/accessConfigPage.json', 'r', encoding="utf-8"))
mainApp.config['SECRET_KEY'] = 'Secret'
mainApp.config['TEMPLATES_AUTO_RELOAD'] = True

mainApp.register_blueprint(authApp, url_prefix='/auth')
mainApp.register_blueprint(requestsApp, url_prefix='/requests')
mainApp.register_blueprint(editApp, url_prefix='/edit')
mainApp.register_blueprint(basketApp, url_prefix='/basket')
@mainApp.route('/')
@verifyUserDecorator
def Index():
    return render_template('index.html', name=session.get('groupName', 'Посетитель'))


@mainApp.route('/exit')
@verifyUserDecorator
def Exit():
    return render_template('exit.html')


@mainApp.errorhandler(404)
@verifyUserDecorator
def Error404(error):
    return render_template('error404.html'), 404


@mainApp.errorhandler(500)
@verifyUserDecorator
def Error500(error):
    return render_template('error500.html'), 500


if __name__ == '__main__':
    mainApp.run(host='127.0.0.1', port=5001)
