import shelve
usersDict = {}
db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
try:
    usersDict = db['Users'] #assign Users storage into usersDict
except:
    print("Error in retrieving Users from storage.db.")
usersDict[1].set_membership("Admin")
print(usersDict[1].get_membership())
db['Users'] = usersDict

db.close()

