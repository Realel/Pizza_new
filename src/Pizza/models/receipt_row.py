from.pizza import Pizza


class Row:
    def __init__(self, pizza: Pizza, quantity: int):
        self.pizza = pizza
        self.quantity = quantity
        self.__total_price = float(self.pizza.price) * self.quantity

    def get_total_price(self):
        return self.__total_price

    def __str__(self):
        return f'{self.pizza.title} x {self.quantity} = {self.__total_price} грн.'
