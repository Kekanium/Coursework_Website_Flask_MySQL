import json

from flask import Blueprint, render_template, url_for, request, session

from access import verifyUserDecorator
from edit.tableClasses import ItemTableEditUsers, ItemTableEditProducts, createResultPage
from sql.SqlMaster import SqlMaster

editApp = Blueprint('edit', __name__, template_folder='templates')
SqlMaster = SqlMaster(json.load(open('config/dataBaseConfig.json', 'r')), r'./edit/requests')


# region General
@editApp.route('/')
@verifyUserDecorator
def editIndex():
    return render_template('editIndex.html', name=session.get('groupName'))


# endregion

# region Admin
@editApp.route('/users')
@verifyUserDecorator
def editUsers():
    result = SqlMaster.MakeRequest('UserGetAll.sql')
    for user in result:
        idLogin = user['idLogin']
        user['urlUpdate'] = url_for('edit.editUsers') + f'/{idLogin}'
        user['nameUpdate'] = f'Редактировать'
        user['classUpdate'] = f""
        user['urlDelete'] = url_for('edit.editUsers') + f'/delete' + f'/{idLogin}'
        user['nameDelete'] = f'Удалить'
        user['classDelete'] = f"confirmable"

    table = ItemTableEditUsers(result)

    createResultPage(table)

    return render_template('editChild.html', title="Все пользователи", url_for_insert=url_for('edit.editUserInsert'),
                           insertWhat="Добавить пользователя")


@editApp.route('/users/<user>', methods=['GET', 'POST'])
@verifyUserDecorator
def editUserEdit(user):
    if request.method == 'GET':
        result = SqlMaster.MakeRequest('UserGetOne.sql', id=user)[0]
        return render_template('editUserEdit.html', idLogin=result['idLogin'], Login=result['Login'],
                               PasswordL=result['PasswordL'], AccessLevel=result['AccessLevel'])
    else:
        idLogin = int(user)
        Login = request.form.get('Login')
        PasswordL = request.form.get('PasswordL')
        AccessLevel = int(request.form.get('AccessLevel'))
        SqlMaster.MakeUpdateInsert('UserUpdate.sql', idLogin=idLogin, Login=Login, PasswordL=PasswordL,
                                   AccessLevel=AccessLevel)
        return render_template('editUserResult.html')


@editApp.route('/users/add', methods=['GET', 'POST'])
@verifyUserDecorator
def editUserInsert():
    if request.method == 'GET':
        return render_template('editUserInsert.html')
    else:
        Login = request.form.get('Login')
        PasswordL = request.form.get('PasswordL')
        AccessLevel = int(request.form.get('AccessLevel'))
        SqlMaster.MakeUpdateInsert('UserInsert.sql', Login=Login, PasswordL=PasswordL,
                                   AccessLevel=AccessLevel)
        return render_template('editUserResult.html')


@editApp.route('/users/delete/<user>')
@verifyUserDecorator
def editUserDelete(user):
    SqlMaster.MakeUpdateInsert('UserDelete.sql', idLogin=int(user))
    return render_template('editUserDelete.html', idLogin=int(user))


# endregion

# region Worker

@editApp.route('/products')
@verifyUserDecorator
def editProducts():
    result = SqlMaster.MakeRequest('ProductGetAll.sql')
    for product in result:
        idProduct = product['idProduct']
        product['urlUpdate'] = url_for('edit.editProducts') + f'/{idProduct}'
        product['nameUpdate'] = f'Редактировать'
        product['classUpdate'] = f""
        product['urlDelete'] = url_for('edit.editProducts') + f'/delete' + f'/{idProduct}'
        product['nameDelete'] = f'Удалить'
        product['classDelete'] = f"confirmable"
    table = ItemTableEditProducts(result)

    createResultPage(table)

    return render_template('editChild.html', title="Все продукты", url_for_insert=url_for('edit.editProductInsert'),
                           insertWhat="Добавить продукт")


@editApp.route('/products/<product>', methods=['GET', 'POST'])
@verifyUserDecorator
def editProductEdit(product):
    if request.method == 'GET':
        result = SqlMaster.MakeRequest('ProductGetOne.sql', id=product)[0]
        return render_template('editProductEdit.html',
                               idProduct=result['idProduct'],
                               Name=result['Name'],
                               Material=result['Material'],
                               UnitOfMeasurement=result['UnitOfMeasurement'],
                               PricePerUnit=result['PricePerUnit'],
                               ActualQuantity=result['ActualQuantity'],
                               FixationDate=result['FixationDate'],
                               ReservedProduct=result['ReservedProduct'],
                               ReservationDate=result['ReservationDate'])
    else:
        idProduct = int(product)
        Name = request.form.get('Name')
        Material = request.form.get('Material')
        UnitOfMeasurement = request.form.get('UnitOfMeasurement')
        PricePerUnit = request.form.get('PricePerUnit')
        ActualQuantity = request.form.get('ActualQuantity')
        FixationDate = request.form.get('FixationDate')
        ReservedProduct = request.form.get('ReservedProduct')
        ReservationDate = request.form.get('ReservationDate')
        SqlMaster.MakeUpdateInsert('ProductUpdate.sql',
                                   idProduct=idProduct,
                                   Name=Name,
                                   Material=Material,
                                   UnitOfMeasurement=UnitOfMeasurement,
                                   PricePerUnit=PricePerUnit,
                                   ActualQuantity=ActualQuantity,
                                   FixationDate=FixationDate,
                                   ReservedProduct=ReservedProduct,
                                   ReservationDate=ReservationDate)
        return render_template('editProductResult.html')


@editApp.route('/products/add', methods=['GET', 'POST'])
@verifyUserDecorator
def editProductInsert():
    if request.method == 'GET':
        return render_template('editProductInsert.html')
    else:
        Name = request.form.get('Name')
        Material = request.form.get('Material')
        UnitOfMeasurement = request.form.get('UnitOfMeasurement')
        PricePerUnit = request.form.get('PricePerUnit')
        ActualQuantity = request.form.get('ActualQuantity')
        FixationDate = request.form.get('FixationDate')
        ReservedProduct = request.form.get('ReservedProduct')
        ReservationDate = request.form.get('ReservationDate')
        SqlMaster.MakeUpdateInsert('ProductInsert.sql',
                                   Name=Name,
                                   Material=Material,
                                   UnitOfMeasurement=UnitOfMeasurement,
                                   PricePerUnit=PricePerUnit,
                                   ActualQuantity=ActualQuantity,
                                   FixationDate=FixationDate,
                                   ReservedProduct=ReservedProduct,
                                   ReservationDate=ReservationDate)
        return render_template('editProductResult.html')


@editApp.route('/products/delete/<product>')
@verifyUserDecorator
def editProductDelete(product):
    SqlMaster.MakeUpdateInsert('ProductDelete.sql', idProduct=int(product))
    return render_template('editProductDelete.html', idProduct=int(product))

# endregion
