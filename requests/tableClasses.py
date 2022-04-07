from flask_table import Table, Col


def createResultPage(table) -> None:
    """
    Create result page for input data in file requestResultChild.html

    :param table: Table for creation. Inherited  from flask_table.Table
    :return: None
    """
    htmlTable = table.__html__()
    file = open(r'.\requests\templates\requestResultChild.html', 'w', encoding='utf-8')

    file.write('{% extends \'requestResultBase.html\' %}{% block child %}<div class="article_3">')
    if htmlTable == "<p>No Items</p>":
        file.write('<p class="article_2">По данному запросу результатов не найдено</p>')
    else:
        file.write(htmlTable)
    file.write('</div>{% endblock %}')
    file.close()
    return None


class ItemTableCustomerOrders(Table):
    idOrder = Col('Номер заказа')
    OrderSum = Col('Сумма заказа')
    OrderDate = Col('Дата заказа')
    OrderStatus = Col('Статус')
    OrderStatusDate = Col('Дата последнего изменения статуса')


class ItemTableOrder(Table):
    idOrderProducts = Col('Позиция')
    idProduct = Col('Артикул')
    Name = Col('Наименование')
    Quantity = Col('Количество')
    Sum = Col('Сумма')


class ItemTableProductsWithLesserQuantity(Table):
    idProduct = Col('Артикул')
    Name = Col('Продукт')
    ActualQuantity = Col('Актуальное количество')
    FixationDate = Col('Дата фиксации')
    ReservedProduct = Col('Зарезервировано продукта')
    ReservationDate = Col('Дата резервации')
