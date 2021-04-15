from datetime import date, timedelta, datetime
import shelve, User, Furniture, Question, Review

db = shelve.open("storage.db","c")
userdict = db["Users"]
currentuser = userdict[2]
ordersuser = currentuser.get_orderDict()
specificorder = ordersuser[14]
deliverydate = specificorder.get_deliverydate()
currentdate = date.today()
eta5 = 5
currentdate5 = currentdate - timedelta(days=eta5)
eta = 3
deliverydate5 = currentdate5 + timedelta(days=eta)
deliverydatenow = currentdate + timedelta(days=eta)
print(specificorder.get_deliverydate())
specificorder.set_orderdate(currentdate5)
specificorder.set_deliverydate(deliverydate5)
print(specificorder.get_deliverydate())
ordersuser[14] = specificorder
print(ordersuser[14].get_deliverydate())
currentuser.set_orderDict(ordersuser)
print(currentuser.get_orderDict())
userdict[2] = currentuser
db["Users"] = userdict

db.close()
