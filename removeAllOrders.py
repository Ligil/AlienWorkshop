import shelve
db = shelve.open('storage.db', 'c')

db['CompletedOrders'] = {}

db.close()
