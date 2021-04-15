class User:
    countID = 0
    orderID = 0 #use for orderList key
    def __init__(self, username, email, firstName, lastName, password, gender):
        self.__userID = self.countID
        self.__membership = 'Default'
        self.__cart = {} #{id:quantity}
        self.__orderDict = {} #Dictionary {Key=Order ID: Value= Cart dictionary}
        self.__username = username
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email
        self.__password = password
        self.__gender = gender
        self.__reset_Password = None
        self.__email_verified = False

        #Trillium
        self.__boughtItems = []
        self.__reviewsDict = {} #Furniture id to [review id] made
        #Daniel
        self.__creditcardID = 0
        self.__creditcard = {}
        #Zion
        self.__wishlist = []
        #Sean
        self.__totalSpent = 0

    #Trillium
    def get_boughtItems(self):
        return self.__boughtItems
    def set_boughtItems(self, boughtItems):
        self.__boughtItems = boughtItems

    #Daniel
    def get_creditcard(self):
        return self.__creditcard
    def set_creditcard(self, creditcard):
        self.__creditcard = creditcard
    def get_creditcardID(self):
        return self.__creditcardID
    def set_creditcardID(self, creditcardID):
        self.__creditcardID = creditcardID
    #Zion
    def set_wishlist(self, wishlist):
        self.__wishlist = wishlist
    def get_wishlist(self):
        return self.__wishlist
    #Sean
    def set_totalSpent(self, totalSpent):
        self.__totalSpent = totalSpent
    def get_totalSpent(self):
        return self.__totalSpent

    ###
    def add_To_Cart(self, itemID, quantity):
        print('Adding to cart')
        if itemID in self.__cart:
            oldQuantity = self.__cart[itemID]
            self.__cart[itemID] = oldQuantity + quantity
            print('Added to cart add')
        else:
            self.__cart[itemID] = quantity
            print('Added to cart else')
    def get_cart(self):
        return self.__cart
    def set_cart(self, cart):
        self.__cart = cart

    def get_orderDict(self):
        return self.__orderDict
    def set_orderDict(self, orderDict):
        self.__orderDict = orderDict

    def get_resetPassword(self):
        return self.__reset_Password
    def set_resetPassword(self, reset_Password):
        self.__reset_Password = reset_Password

    def get_reviewsDict(self):
        return self.__reviewsDict
    def set_reviewsDict(self, reviewsDict):
        self.__reviewsDict = reviewsDict

    def get_userID(self):
        return self.__userID
    def get_username(self):
        return self.__username
    def get_firstName(self):
        return self.__firstName
    def get_lastName(self):
        return self.__lastName
    def get_password(self):
        return self.__password
    def get_membership(self):
        return self.__membership
    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email
    def get_emailVerified(self):
        return self.__email_verified

    def set_userID(self, userID):
        self.__userID = userID
    def set_firstName(self, firstName):
        self.__firstName = firstName
    def set_lastName(self, lastName):
        self.__lastName = lastName
    def set_username(self, username):
        self.__username = username
    def set_password(self, password):
        self.__password = password
    def set_membership(self, membership):
        self.__membership = membership
    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email
    def set_emailVerified(self, verified):
        self.__email_verified = verified

class Creditcard:
    def __init__(self, cctype, ccnumber, ccscode, expirationdate, billinginformationname, city, billingaddress, postalcode, country, phonenumber, usersCreditCardCount):
        self.__creditcardtype = cctype
        self.__creditcardnumber = ccnumber
        self.__securitycode = ccscode
        self.__expdate = expirationdate
        self.__fullname = billinginformationname
        self.__city = city
        self.__billing = billingaddress
        self.__postalcode = postalcode
        self.__country = country
        self.__phonenumber = phonenumber

        self.__usersCreditCardCount = usersCreditCardCount

    def get_creditcardtype(self):
        return self.__creditcardtype
    def get_creditcardnumber(self):
        return self.__creditcardnumber
    def get_securitycode(self):
        return self.__securitycode
    def get_expdate(self):
        return self.__expdate
    def get_fullname(self):
        return self.__fullname
    def get_city(self):
        return self.__city
    def get_billing(self):
        return self.__billing
    def get_postalcode(self):
        return self.__postalcode
    def get_country(self):
        return self.__country
    def get_phonenumber(self):
        return self.__phonenumber

    def set_creditcardtype(self,creditcardtype):
        self.__creditcardtype = creditcardtype
    def set_creditcardnumber(self,ccnumber):
        self.__creditcardnumber = ccnumber
    def set_securitycode(self,securitycode):
        self.__securitycode = securitycode
    def set_expdate(self,date):
        self.__expdate = date
    def set_fullname(self,fullname):
        self.__fullname = fullname
    def set_city(self,city):
        self.__city = city
    def set_billing(self,billing):
        self.__billing = billing
    def set_postalcode(self,postalcode):
        self.__postalcode = postalcode
    def set_country(self,country):
        self.__country = country
    def set_phonenumber(self,phonenumber):
        self.__phonenumber = phonenumber

    def get_creditCardCount(self):
        return self.__usersCreditCardCount

class Orders:
    def __init__(self, userID, orderID, orderDate, deliveryDate, totalCost, orderlist, phoneNumber, postalcode, country,deliveryaddress, ccId,cctype):
        self.__userID = userID
        self.__orderID = orderID
        self.__orderdate = orderDate
        self.__deliverydate = deliveryDate
        self.__totalcost = totalCost
        self.__deliverystatus = 'Processing'
        self.__orderlist = orderlist #[object,object,object]
        self.__deliveryaddress = deliveryaddress
        self.__postalcode = postalcode
        self.__country = country
        self.__phonenumber = phoneNumber
        self.__ccId = ccId
        self.__cctype = cctype
        self.__completionstatus = "Incomplete"
    def get_userID(self):
        return self.__userID

    def get_orderID(self):
        return self.__orderID
    def set_orderID(self,orderID):
        self.__orderID = orderID
    def get_orderdate(self):
        return self.__orderdate
    def set_orderdate(self,orderdate):
        self.__orderdate = orderdate
    def get_deliverydate(self):
        return self.__deliverydate
    def set_deliverydate(self,deliverydate):
        self.__deliverydate = deliverydate
    def get_totalcost(self):
        return self.__totalcost
    def set_totalcost(self,totalcost):
        self.__totalcost = totalcost
    def get_deliverystatus(self):
        return self.__deliverystatus
    def set_deliverystatus(self,deliverystatus):
        self.__deliverystatus = deliverystatus
    def get_orderlist(self):
        return self.__orderlist
    def set_orderlist(self,orderlist):
        self.__orderlist = orderlist
    def get_deliveryaddress(self):
        return self.__deliveryaddress
    def set_deliveryaddress(self,deliveryaddress):
        self.__deliveryaddress = deliveryaddress
    def get_postalcode(self):
        return self.__postalcode
    def set_postalcode(self,postalcode):
        self.__postalcode = postalcode
    def get_country(self):
        return self.__country
    def set_country(self,country):
        self.__country = country
    def get_phonenumber(self):
        return self.__phonenumber
    def set_phonenumber(self,phonenumber):
        self.__phonenumber = phonenumber
    def get_ccnumber(self):
        return self.__ccId
    def set_ccnumber(self,ccnumber):
        self.__ccId = ccnumber
    def get_completionstatus(self):
        return self.__completionstatus
    def set_completionstatus(self,completionstatus):
        self.__completionstatus = completionstatus
    def get_cctype(self):
        return self.__cctype
    def set_cctype(self,cctype):
        self.__cctype = cctype
