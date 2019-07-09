class Item:
    name = ""
    price = ""
    author = ""
    place = ""
    def __init__(self, input_id, input_author, input_place, input_price):
        self.name = input_id
        self.author = input_author
        self.place = input_place
        self.price = input_price
    def toJSON(self):
        printStr = {
            'name': self.name,
            'price': self.name,
            'author':self.author,
            'place': self.name
        }
        return printStr
