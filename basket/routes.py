import datetime
import json

from flask import Blueprint, render_template, request, session, redirect, url_for

from sql.SqlMaster import SqlMaster

basketApp = Blueprint('basket', __name__, template_folder='templates')
SqlMaster = SqlMaster(json.load(open('config/dataBaseConfig.json', 'r')), r'./basket/requests')


@basketApp.route('/', methods=['GET', 'POST'])
# @verifyUserAccess
def basketIndex():
    if request.method == 'GET':
        customerNames = SqlMaster.MakeRequest('CustomerNames.sql')

        return render_template("basketIndex.html", customerNames=customerNames)
    else:
        idCustomer = int(request.form.get('customerId'))
        session['idCustomer'] = idCustomer
        print(url_for("basket.basketMain"))
        return redirect(url_for("basket.basketMain"))


@basketApp.route('/Main', methods=['GET', 'POST'])
# @verifyUserAccess
def basketMain():
    if request.method == 'GET':
        products = SqlMaster.MakeRequest('AllProducts.sql')
        basketId = session.get('basket', [])
        CustomerName = SqlMaster.MakeRequest("CustomerName.sql", idCustomer=session.get('idCustomer'))[0]['Name']
        totalSum = 0
        for product in products:
            product['curQuantity'] = product['ActualQuantity']
            for basketProduct in basketId:
                if product['idProduct'] == basketProduct[0]:
                    product['curQuantity'] = product['ActualQuantity'] - basketProduct[1]
                    totalSum += product['PricePerUnit'] * basketProduct[1]
                    break

        return render_template('basketMain.html',
                               CustomerName=CustomerName,
                               totalSum=totalSum,
                               basket=basketId,
                               products=products,
                               allProducts=SqlMaster.MakeRequest('AllProducts.sql'),
                               cleared_basket=-1,
                               bought=-1)
    else:
        basketId = session.get('basket', [])
        products = SqlMaster.MakeRequest('AllProducts.sql')

        # Add
        itemIdAdd = int(request.form.get('itemIdAdd', -1))
        itemQuantityAdd = int(request.form.get('itemQuantityAdd', -1))
        isInBasket = False
        if itemIdAdd != -1:
            for currentProduct in basketId:
                if currentProduct[0] == itemIdAdd:
                    currentProduct[1] += itemQuantityAdd
                    isInBasket = True

            if not isInBasket:
                basketId.append([itemIdAdd, itemQuantityAdd])

        # Remove
        itemIdDelete = int(request.form.get('itemIdDelete', -1))
        itemQuantityDelete = int(request.form.get('itemQuantityDelete', -1))
        if itemIdDelete != -1:
            for currentProduct in basketId:
                if currentProduct[0] == itemIdDelete:
                    currentProduct[1] -= itemQuantityDelete
                    if currentProduct[1] == 0:
                        basketId.remove(currentProduct)

        # Clear basket
        clearBasket = int(request.form.get('clearBasket', -1))
        if clearBasket != -1:
            basketId = []

        # Buy
        buy = int(request.form.get('buy', -1))
        if buy != -1:
            allSum = 0
            for basketItem in basketId:
                for currentProduct in products:
                    if int(currentProduct['idProduct']) == basketItem[0]:
                        allSum = int(currentProduct['PricePerUnit']) * basketItem[1]

            SqlMaster.MakeUpdateInsert('AddOrder.sql', idCustomer=session.get('idCustomer'),
                                       OrderDate=datetime.date.today(), OrderSum=allSum,
                                       OrderStatus=0, OrderStatusDate=datetime.date.today())

            lastOrder = int(SqlMaster.MakeRequest('GetLastOrder.sql')[0]['idOrder'])
            for basketItem in basketId:
                for currentProduct in products:
                    if int(currentProduct['idProduct']) == basketItem[0]:
                        SqlMaster.MakeUpdateInsert('AddProductToOrder.sql', idOrder=lastOrder,
                                                   idProduct=basketItem[0], Quantity=basketItem[1],
                                                   Sum=int(currentProduct['PricePerUnit']) * basketItem[1])
                        SqlMaster.MakeUpdateInsert('UpdateProduct.sql', idProduct=basketItem[0],
                                                   ActualQuantity=int(currentProduct['ActualQuantity']) - basketItem[1],
                                                   ReservedProduct=int(currentProduct['ReservedProduct']) + basketItem[
                                                       1])
            basketId = []
            return render_template("basketResult.html")

        session['basket'] = basketId
        return redirect(url_for('basket.basketMain'))
