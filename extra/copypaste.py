usersDict = {}
db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
try:
    usersDict = db['Users'] #assign Users storage into usersDict
except:
    print("Error in retrieving Users from storage.db.")
db.close() #always close your database
