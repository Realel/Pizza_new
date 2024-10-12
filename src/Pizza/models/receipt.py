import datetime
from src.Pizza.models.client import Client


class Receipt:
    def __init__(self, uuid: str, client: Client, row_list: list):
        self.uuid = uuid
        self.client = client
        self.row_list = row_list
        self.order_time = datetime.datetime.now()  # Время заказа
        self.total_price = sum(row.get_total_price() for row in self.row_list)  # Общая сумма заказа
        self.cooking_time = len(row_list) * 10  # Время готовки в минутах (по 10 минут на пиццу)

    def __str__(self):
        # Формируем чек
        receipt_str = f"Клієнт: {self.client.first_name} {self.client.last_name}\n"
        receipt_str += f"Телефон: {self.client.phone_number}\n"
        receipt_str += f"Адреса: {self.client.address}\n"
        receipt_str += f"Час замовлення: {self.order_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt_str += "Замовлені піцци:\n"

        # Перебираем все пиццы в заказе
        for row in self.row_list:
            receipt_str += f"{row.pizza.title} x {row.quantity} = {row.get_total_price()} грн.\n"

        # Общая сумма и время готовности
        receipt_str += f"\nЗагальна сума: {self.total_price} грн.\n"
        ready_time = self.order_time + datetime.timedelta(minutes=self.cooking_time)
        receipt_str += f"Час готовності: {ready_time.strftime('%Y-%m-%d %H:%M:%S')} (+{self.cooking_time} хв.)\n"

        return receipt_str
