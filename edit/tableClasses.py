from flask_table import Col, Table
from flask_table.html import element


def createResultPage(table) -> None:
    """
    Create result page for input data in file editChild.html

    :param table: Table for creation. Inherited  from flask_table.Table
    :return: None
    """
    htmlTable = table.__html__()
    file = open(r'.\edit\templates\editChild.html', 'w', encoding='utf-8')

    file.write('{% extends \'editBase.html\' %}{% block child %}<div class="article_3">')
    if htmlTable == "<p>No Items</p>":
        file.write('<p class="article_2">Нечего редактировать</p>')
    else:
        file.write(htmlTable)
    file.write('</div>{% endblock %}')
    file.close()
    return None


class ExternalURLCol(Col):
    """
    Class for use External links
    """

    def __init__(self, name, url_attr, class_attr, **kwargs):
        """
        Init External table for Col
        :param name: name of Col
        :param url_attr: url for link
        :param class_attr: css class name
        """
        self.url_attr = url_attr
        self.class_attr = class_attr
        super(ExternalURLCol, self).__init__(name, **kwargs)

    def td_contents(self, item, attr_list):
        """
        Let generator table to know what put inside cell
        :param item: std parametr for Col
        :param attr_list: std parametr for Col
        :return: element in table column
        """
        text = self.from_attr_list(item, attr_list)
        url = self.from_attr_list(item, [self.url_attr])
        classURL = self.from_attr_list(item, [self.class_attr])
        return element('a', {'href': url, 'class': classURL}, content=text)


class ItemTableEditUsers(Table):
    idLogin = Col('id')
    Login = Col('Логин')
    PasswordL = Col('Пароль')
    AccessLevel = Col('Уровень доступа')
    UpdateLink = ExternalURLCol(' ', url_attr='urlUpdate', attr='nameUpdate', class_attr="classUpdate")
    DeleteLink = ExternalURLCol(' ', url_attr='urlDelete', attr='nameDelete', class_attr="classDelete")


class ItemTableEditProducts(Table):
    idProduct = Col('Артикул')
    Name = Col('Продукт')
    Material = Col('Материал')
    UnitOfMeasurement = Col('Единица измерения')
    PricePerUnit = Col('Цена')
    ActualQuantity = Col('Актуальное количество')
    FixationDate = Col('Дата фиксации')
    ReservedProduct = Col('Зарезервировано продукта')
    ReservationDate = Col('Дата резервации')
    UpdateLink = ExternalURLCol(' ', url_attr='urlUpdate', attr='nameUpdate', class_attr="classUpdate")
    DeleteLink = ExternalURLCol(' ', url_attr='urlDelete', attr='nameDelete', class_attr="classDelete")
