class Client:
    def __init__(self,first_name,last_name,phone_number,address):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
    def __str__(self):
        return f'Client: {self.first_name} {self.last_name}, Phone: {self.phone_number}, Address: {self.address}'