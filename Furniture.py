class Furniture:
    countID = 0
    def __init__(self, name, cost, description, length, width, height):
        self.__furnitureID = self.countID
        self.__filename = ''
        self.__name = name
        self.__cost = cost
        self.__tags = []
        self.__description = description
        self.__length = length
        self.__width = width
        self.__height = height
        self.__stars = 0
        self.__reviews = {'lastId':0}

    def get_countID(self):
        return self.__class__.countID

    def get_furnitureID(self):
        return self.__furnitureID
    def get_filename(self):
        return self.__filename
    def get_name(self):
        return self.__name
    def get_cost(self):
        return self.__cost
    def get_tags(self):
        return self.__tags
    def get_description(self):
        return self.__description
    def get_length(self):
        return self.__length
    def get_width(self):
        return self.__width
    def get_height(self):
        return self.__height
    def get_reviews(self):
        return self.__reviews
    def get_stars(self):
        return self.__stars

    def set_furnitureID(self, furnitureID):
        self.__furnitureID = furnitureID
    def set_filename(self, filename):
        self.__filename = filename
    def set_name(self, name):
        self.__name = name
    def set_cost(self, cost):
        self.__cost = cost
    def set_tags(self, tags):
        self.__tags = tags
    def set_description(self, description):
        self.__description = description
    def set_dimensions(self, length, width, height):
        self.__length = length
        self.__width = width
        self.__height = height
    def set_reviews(self, reviews):
        self.__reviews = reviews
        print(self.__reviews)
        stars = 0
        for id in self.__reviews:
            if id == 'lastId':
                continue
            reviewObject = self.__reviews[id]
            stars += reviewObject.get_stars()
        if len(self.__reviews) == 1:
            avgStars = 0
        else:
            avgStars = round(stars/(len(self.__reviews)-1), 1)
        self.__stars = avgStars

class CartFurniture(Furniture):
    def __init__(self, name, cost, description, length, width, height,filename ,quantity, furnitureID):
        super().__init__(name, cost, description, length, width, height)
        self.__cartfilename = filename
        self.__furnitureID = furnitureID
        self.__quantity = quantity
        self.__totalprice = float(cost) * quantity
    def get_totalprice(self):
        return self.__totalprice
    def get_quantity(self):
        return self.__quantity
    def get_cartfurnitureID(self):
        return self.__furnitureID
    def get_cartfilename(self):
        return self.__cartfilename

    def set_quantity(self,quantity):
        self.__quantity = quantity
    def set_totalprice(self,totalprice):
        self.__totalprice = totalprice
    def set_cartfurnitureID(self,cartfurnitureid):
        self.__furnitureID = cartfurnitureid
    def set_cartfilename(self,cartfilename):
        self.__cartfilename = cartfilename


