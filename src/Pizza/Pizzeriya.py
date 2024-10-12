from src.Pizza.controller import Controller


def main(controller):
    print('Вас вітає наша Піццерія')
    while True:
        print('1. Меню')
        print('2. Замовити піццу')
        print('3. Створити свою піццу')
        print('4. Фільтр за ціною піцц')
        print('5. Закрити програму')
        choice = input('Виберіть пункт меню: ')

        if choice == '1':
            controller.display_menu()
        elif choice == '2':
            controller.new_order()
        elif choice == '3':
            controller.create_custom_pizza()
        elif choice == '4':
            controller.filter_pizzas_by_price()
        elif choice == '5':
            break
        else:
            print('Неправильний вибір!')

if __name__ == '__main__':
    controller = Controller()
    main(controller)