import json

from flask import Blueprint, render_template, request, session

from access import verifyUserDecorator
from requests.tableClasses import createResultPage, ItemTableCustomerOrders, ItemTableOrder, \
    ItemTableProductsWithLesserQuantity
from sql.SqlMaster import SqlMaster

requestsApp = Blueprint('requests', __name__, template_folder='templates')

SqlMaster = SqlMaster(json.load(open('config/dataBaseConfig.json', 'r', encoding="utf-8")), r'./requests/requests')

LevelToName = {
    '0': 'Разработчик',
    '1': 'Администратор',
    '2': 'Директор',
    '3': 'Работник склада',
    '4': 'Покупатель'
}
NameToLevel = {
    'Разработчик': '0',
    'Администратор': '1',
    'Директор': '2',
    'Работник склада': '3',
    'Покупатель': '4'
}
NumberStatusToName = {
    0: 'Создан',
    1: 'Сборка',
    2: 'Отправлен',
    3: 'Завершен'
}


# region General
@requestsApp.route('/')
@verifyUserDecorator
def requestsIndex():
    return render_template('requestIndex.html', name=session.get('groupName'))


# endregion

# region Director
@requestsApp.route('/CustomersOrders', methods=['GET', 'POST'])
@verifyUserDecorator
def requestsCustomersOrders():
    customerNames = SqlMaster.MakeRequest('CustomerNames.sql')
    if request.method == 'GET':
        file = open(r'.\requests\templates\requestCustomersOrdersChild.html', 'w', encoding='utf-8')

        file.write(
            '{% extends \'requestCustomersOrdersBase.html\' %}{% block child %}<div class="article_3"><select name="customerName">')
        for name in customerNames:
            temp = name['Name']
            file.write(f'<option>{temp}</option>')
        file.write('</select></div>{% endblock %}')
        file.close()

        return render_template('requestCustomersOrdersChild.html')
    else:
        customerName = request.form.get('customerName')
        title = f'Заказы заказчика {customerName}'
        for name in customerNames:
            if name['Name'] == customerName:
                customerName = int(name['idCustomer'])
                break
        result = SqlMaster.MakeRequest('CustomerOrders.sql',
                                       customerName=customerName, allOrders=0)
        for i in range(len(result)):
            result[i]['idOrder'] = i + 1
            result[i]['OrderStatus'] = NumberStatusToName[result[i]['OrderStatus']]
        table = ItemTableCustomerOrders(result)
        createResultPage(table)
        return render_template('requestResultChild.html', url_back='./CustomersOrders',
                               title=title)


# endregion

# region Customer
@requestsApp.route('/Order', methods=['GET', 'POST'])
@verifyUserDecorator
def requestsOrder():
    if request.method == 'GET':
        result = SqlMaster.MakeRequest('CustomerOrders.sql',
                                       customerName='0', allOrders=1)

        file = open(r'.\requests\templates\requestOrderChild.html', 'w', encoding='utf-8')
        file.write(
            '{% extends \'requestOrderBase.html\' %}{% block child %}<div class="article_3"><select name="idOrder">')
        for id in result:
            idOrder = id['idOrder']
            file.write(f'<option>{idOrder}</option>')
        file.write('</select></div>{% endblock %}')
        file.close()

        return render_template('requestOrderChild.html')
    else:
        idOrder = request.form.get('idOrder')
        title = f'Товары заказа №{idOrder}'
        result = SqlMaster.MakeRequest('OrderProducts.sql',
                                       idOrder=int(idOrder))
        for i in range(len(result)):
            result[i]['idOrderProducts'] = i + 1

        table = ItemTableOrder(result)
        createResultPage(table)
        return render_template('requestResultChild.html', url_back='./Order',
                               title=title)


# endregion

# region Worker

@requestsApp.route('/ProductsWithLesserQuantity', methods=['GET', 'POST'])
@verifyUserDecorator
def requests_ProductsWithLesserQuantity():
    if request.method == 'GET':
        return render_template('requestProductsWithLesserQuantity.html')
    else:
        quantityProduct = request.form.get('quantityProduct')
        result = SqlMaster.MakeRequest('ProductsWithLesserQuantity.sql', quantityProduct=quantityProduct)

        table = ItemTableProductsWithLesserQuantity(result)
        createResultPage(table)
        return render_template('requestResultChild.html', url_back='./ProductsWithLesserQuantity',
                               title=f"Все продукты, количество которых меньше чем {quantityProduct}")
# endregion
