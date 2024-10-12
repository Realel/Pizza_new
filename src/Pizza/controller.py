import uuid
from faker import Faker
import sqlite3

from src.Pizza.models.pizza import Pizza
from src.Pizza.models.client import Client
from src.Pizza.models.receipt import Receipt
from src.Pizza.models.receipt_row import Row
from src.database import create_client_table, add_new_client, find_client_by_phone

my_faker = Faker(locale='uk_UA')
Faker.seed()

class SingletonMeta(type):
    _instances = {}


    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Controller(metaclass=SingletonMeta):
    def __init__(self):
        self.order_list = []
        self.pizza_list = [
            Pizza(1, 'Проста', 'Томатный соус, сыр, орегано', "85"),
            Pizza(2, 'Вегетарианская', 'Томатный соус, сыр, болгарский перец, шампиньоны, маслины', "95"),
            Pizza(3, 'Сырная классика', 'Томатный соус, моцарелла, пармезан, орегано', "80"),
            Pizza(4, 'Грибная', 'Томатный соус, грибы, сыр, чеснок', "90"),
            Pizza(5, 'Маргарита', 'Томатный соус, сыр моцарелла, базилик', "120"),
            Pizza(6, 'Пеперони', 'Томатный соус, сыр, колбаса пеперони, оливковое масло', "150"),
            Pizza(7, 'Четыре сыра', 'Томатный соус, моцарелла, горгонзола, пармезан, чеддер', "180"),
            Pizza(8, 'Гавайская', 'Томатный соус, сыр, курица, ананас', "140"),
            Pizza(9, 'Мясная', 'Томатный соус, ветчина, бекон, колбаски, сыр', "200"),
            Pizza(10, 'С морепродуктами', 'Томатный соус, кальмары, креветки, мидии, сыр', "220")
            ]

        self.ingredients_menu = [
            ("Томатный соус", 10),
            ("Сыр моцарелла", 25),
            ("Пармезан", 30),
            ("Чеддер", 25),
            ("Колбаса пеперони", 40),
            ("Ветчина", 35),
            ("Курица", 30),
            ("Ананас", 20),
            ("Оливки", 15),
            ("Маслины", 15),
            ("Грибы", 20),
            ("Болгарский перец", 15),
            ("Креветки", 50),
            ("Мидии", 45),
            ("Кальмары", 50),
            ("Бекон", 35),
            ("Томаты", 10),
            ("Лук", 10),
            ("Чеснок", 5)
        ]
        self.client_list = []
        create_client_table()


    def display_menu(self):
        for pizza in(self.pizza_list):
            print(f"{pizza.id}. {pizza.title} - {pizza.descr} - {pizza.price} грн.")

    def new_order(self):
        s = str(uuid.uuid4())  # Уникальный идентификатор заказа
        row_list = []

        # Запрашиваем номер телефона клиента
        phone = input("Введите номер телефона: ")

        # Ищем клиента по номеру телефона
        client_data = find_client_by_phone(phone)

        if client_data:
            print(f"Клиент найден: {client_data[1]} {client_data[2]}, адрес: {client_data[4]}")
            client = Client(client_data[1], client_data[2], client_data[3],
                            client_data[4])  # Создаем объект Client на основе данных из БД
        else:
            print("Новый клиент.")
            first_name = input("Введите имя: ")
            last_name = input("Введите фамилию: ")
            address = input("Введите адрес: ")

            # Добавляем нового клиента в базу данных
            add_new_client(first_name, last_name, phone, address)

            # Создаем клиента для чека
            client = Client(first_name, last_name, phone, address)

        # Процесс выбора пиццы
        while True:
            try:
                pizza_idx = int(input("Введите индекс пиццы или -1 для завершения: "))
                if pizza_idx == -1:
                    break
                if pizza_idx < 1 or pizza_idx > len(self.pizza_list):
                    print("Неправильный индекс пиццы. Попробуйте снова.")
                    continue
                quantity = int(input("Введите количество пицц: "))
                pizza = self.pizza_list[pizza_idx - 1]
                row_list.append(Row(pizza, quantity))
            except ValueError:
                print("Некорректное значение. Попробуйте снова.")

        if row_list:
            # Создаем чек
            receipt = Receipt(s, client, row_list)
            print(receipt)  # Выводим чек
        else:
            print("Заказ не создан.")


    def filter_pizzas_by_price(self):
        choice = input("Введіть '1', щоб показати піцци дешевше 100 грн, або '2' для піцц дорожче 100 грн: ")
        if choice == '1':
            filtered_pizzas = [pizza for pizza in self.pizza_list if int(pizza.price) < 100]
            if filtered_pizzas:
                print("Піци, ціна яких менше 100 грн.:")
                for pizza in filtered_pizzas:
                    print(f"{pizza.id}. {pizza.title} - {pizza.descr} - {pizza.price} грн.")
            else:
                print("Немає піц з ціною менше 100 грн.")

        elif choice == '2':
            filtered_pizzas = [pizza for pizza in self.pizza_list if int(pizza.price) > 100]
            if filtered_pizzas:
                print("Піци, ціна яких більше 100 грн.:")
                for pizza in filtered_pizzas:
                    print(f"{pizza.id}. {pizza.title} - {pizza.descr} - {pizza.price} грн.")
            else:
                print("Немає піц з ціною більше 100 грн.")


    def create_custom_pizza(self):
        base_price = 20  # Стоимость основы
        chosen_ingredients = []
        total_price = base_price  # Начальная стоимость равна цене основы

        print("Создайте свою пиццу! Цена основы: 20 грн.")
        print("Меню ингредиентов:")

        # Выводим список ингредиентов с ценами
        for idx, (ingredient, price) in enumerate(self.ingredients_menu, start=1):
            print(f"{idx}. {ingredient} - {price} грн.")

        while True:
            try:
                ingredient_idx = int(input("Введите номер ингредиента или -1 для завершения: "))
                if ingredient_idx == -1:
                    break
                if ingredient_idx < 1 or ingredient_idx > len(self.ingredients_menu):
                    print("Неправильный выбор. Попробуйте снова.")
                    continue

                # Добавляем выбранный ингредиент в список
                chosen_ingredient = self.ingredients_menu[ingredient_idx - 1]
                chosen_ingredients.append(chosen_ingredient)
                total_price += chosen_ingredient[1]  # Добавляем цену ингредиента к общей стоимости
                print(f"Добавлено: {chosen_ingredient[0]} - {chosen_ingredient[1]} грн.")
            except ValueError:
                print("Некорректное значение. Попробуйте снова.")

        # Пользователь может назвать свою пиццу
        pizza_name = input("Введите название для вашей пиццы: ")

        # Описание пиццы составляем из ингредиентов
        description = ', '.join([ingredient[0] for ingredient in chosen_ingredients])

        # Создаем пиццу
        custom_pizza = Pizza(len(self.pizza_list) + 1, pizza_name, description, str(total_price))
        self.pizza_list.append(custom_pizza)

        print(f"Ваша пицца '{pizza_name}' создана! Состав: {description}. Цена: {total_price} грн.")
        return custom_pizza