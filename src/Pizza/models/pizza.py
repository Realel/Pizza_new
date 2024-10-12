class Pizza:
    def __init__(self, id , title, descr ,price ):
        self.id = id
        self.title = title
        self.descr = descr
        self.price = price
    def __str__(self):
        return f"[{self.id}] {self.title} - {self.descr[:30]}... (Price: {self.price})"