import shelve

db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
del db['Tags']
del db['Furniture']
db.close()
