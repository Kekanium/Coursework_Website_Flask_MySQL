from functools import wraps

from flask import session, current_app, request, render_template


def verifyUserAccess():
    accessConfigModule = current_app.config['ACCESS_CONFIG_MODULE']
    accessConfigPage = current_app.config['ACCESS_CONFIG_PAGE']
    groupName = session.get('groupName', 'Посетитель')

    targetPage = request.endpoint
    targetModule = targetPage.split('.')

    if len(targetModule) == 1:
        targetModule = ""
    else:
        targetModule = targetModule[0]

    if groupName == 'Разработчик':
        return True

    # Check module access
    if groupName in accessConfigModule \
            and targetModule in accessConfigModule[groupName]:
        return True

    # Check page access
    if groupName in accessConfigPage \
            and targetPage in accessConfigPage[groupName]:
        return True
    else:
        return False


def verifyUserDecorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if verifyUserAccess():
            return f(*args, **kwargs)
        return render_template('permissionDenied.html')

    return wrapper
