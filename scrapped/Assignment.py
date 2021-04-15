from flask import Flask, render_template, request, session, redirect, url_for
from Forms import CreateUserForm, CreateFurnitureForm, LoginForm
import shelve, User, Furniture

app = Flask(__name__)
app.secret_key = "autismo's gallery"

@app.route('/')
def home():
    usersDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        usersDict = db['Users'] #assign Users storage into usersDict
    except:
        print("Error in retrieving Users from storage.db.")
    db.close() #always close your database

    print(usersDict)
    if session.get("USERID") != None:
        username = usersDict[session["USERID"]].get_username()
        return render_template('home.html', username=username)
    return render_template('home.html')

@app.route('/ourProducts')
def ourProducts():
    return render_template('ourProducts.html')

@app.route('/ourProducts/1/', methods=['GET', 'POST'])
def ourProductsProduct():
    return render_template('ourProductsProduct.html')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html')

@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm(request.form)
    if request.method == 'POST' and loginForm.validate(): #only runs if post button clicked
        usersDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            usersDict = db['Users'] #assign Users storage into usersDict
        except:
            print("Error in retrieving Users from storage.db.")
        db.close() #always close your database

        for i in usersDict:
            if loginForm.username.data == usersDict[i].get_username():
                if loginForm.password.data == usersDict[i].get_password():
                    session["USERID"] = usersDict[i].get_userID()
                    return redirect(url_for('home'))

        return render_template('login.html', form=loginForm, invalid=True)
    return render_template('login.html', form=loginForm)

@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    createUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and createUserForm.validate(): #only runs if post button clicked
        usersDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            usersDict = db['Users'] #assign Users storage into usersDict
        except:
            print("Error in retrieving Users from storage.db.")

        for i in usersDict:
            if usersDict[i].get_username() == createUserForm.username.data:
                return render_template('createUser.html', form=createUserForm, exist=True)

        User.User.countID = len(usersDict) + 1
        #create list of data into 'user' variable
        user = User.User(createUserForm.username.data,
                         createUserForm.password.data,
                         createUserForm.gender.data,)
        usersDict[user.get_userID()] = user #put 'user' variable into usersDict

        db['Users'] = usersDict #update new 'Users' in database
        db.close() #always close your databaseu

        #test codes, left here for fun#############
        #usersDict = db['Users'] #update 'usersDict' with new users, same as line 22

        #user = usersDict[user.get_userID()] #from variable in line 27, get user id, refresh 'user' variable from updated dictionary, idk why honestly
        #print(user.get_username(), "was stored in shelve successfully with userID =", user.get_userID()) #console output to confirm success
        ###########################################

        return redirect(url_for('home')) #go back to this page on successful post/creation
    return render_template('createUser.html', form=createUserForm) #refresh page, createUserForm variable created in line 16, for form get and post

@app.route('/logout')
def logout():
    session["USERID"] = None
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if session.get("USERID") != None:
        usersDict = {}
        db = shelve.open('storage.db', 'c') #open for read only
        try:
            usersDict = db['Users'] #assign Users storage into usersDict
        except:
            print("There are no users.")
        db.close()
        user = usersDict[session["USERID"]]
        return render_template('profile.html', user=user)
    return redirect(url_for('login'))

#Administrator Functions
@app.route("/createFurniture", methods=["GET", "POST"])
def upload_image():
    createFurnitureForm = CreateFurnitureForm(request.form)
    if request.method == 'POST' and createFurnitureForm.validate(): #only runs if post button clicked
        furnitureDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            furnitureDict = db['Furniture'] #assign Users storage into usersDict
        except:
            print("Error in retrieving Users from storage.db.")

        Furniture.Furniture.countID = len(furnitureDict) + 1
        #create list of data into 'user' variable
        furniture = Furniture.Furniture(createFurnitureForm.image.data)
        furnitureDict[furniture.get_furnitureID()] = furniture #put 'user' variable into usersDict

        db['Furniture'] = furnitureDict #update new 'Users' in database
        db.close()
        return redirect(url_for('retrieveFurniture')) #go back to this page on successful post/creation
    return render_template('createFurniture.html', form=createFurnitureForm)

@app.route('/retrieveFurniture')
def retrieveFurniture():
    furnitureDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Users storage into usersDict
    except:
        print("Error in retrieving Users from storage.db.")
    db.close()

    furnitureList = []

    #Insert every dictionary into usersList list
    for key in furnitureDict:
        furniture = furnitureDict.get(key)
        furnitureList.append(furniture)
    #return sends the variable back to person
    return render_template('retrieveFurniture.html', furnitureList=furnitureList, count=len(furnitureList))

@app.route('/retrieveUsers')
def retrieveUsers():
    usersDict = {}
    db = shelve.open('storage.db', 'c') #open for read only
    try:
        usersDict = db['Users'] #assign Users storage into usersDict
    except:
        print("There are no users.")
    db.close()

    usersList = []

    #Insert every dictionary into usersList list
    for key in usersDict:
        user = usersDict.get(key)
        usersList.append(user)
    #return sends the variable back to person
    return render_template('retrieveUsers.html', usersList=usersList, count=len(usersList))

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        userDict = {}
        db = shelve.open('storage.db', 'w')
        userDict = db['Users']
        user = userDict.get(id)
        user.set_username(updateUserForm.username.data)
        user.set_password(updateUserForm.password.data)
        user.set_membership(updateUserForm.membership.data)
        user.set_gender(updateUserForm.gender.data)
        db['Users'] = userDict
        db.close()
        return redirect(url_for('retrieveUsers'))
    else:
        userDict = {}
        db = shelve.open('storage.db', 'r')
        userDict = db['Users']
        db.close()

        user = userDict.get(id) #retrieve user data of specific id into user variable
        updateUserForm.username.data = user.get_username()
        updateUserForm.password.data = user.get_password()
        updateUserForm.membership.data = user.get_membership()
        updateUserForm.gender.data = user.get_gender()
        return render_template('updateUser.html', form=updateUserForm)

if __name__ == '__main__':
    app.run()
