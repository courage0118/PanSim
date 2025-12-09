class car:
    price_dic = {"bmw": 1000, "vw": 2000}
    def __init__(self, brand, plate):
        self.brand = brand
        self.plate = plate

    def get_price(self):
        return self.price_dic(brand)

mycar = car(brand="bmw", plate="110")
print(mycar.get_price())