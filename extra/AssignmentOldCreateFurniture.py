from flask import Flask, render_template, request, session, redirect, url_for
from Forms import CreateUserForm, LoginForm, ChangeProfileForm, ChangePasswordForm, CreateFurnitureForm
import shelve, User, Furniture
import os
from werkzeug.utils import secure_filename

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
    furnitureDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Furniture storage into furnitureDict
    except:
        print("Error in retrieving Furniture from storage.db.")
    db.close()

    furnitureList = []
    #Insert every dictionary into furnitureList list
    for key in furnitureDict:
        furniture = furnitureDict.get(key)
        furnitureList.append(furniture)

    #cart items
    if session.get("USERID") != None:
        usersDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            usersDict = db['Users'] #assign Users storage into usersDict
        except:
            print("Error in retrieving Users from storage.db.")
        db.close() #always close your database

        cart = usersDict[session["USERID"]].get_cart()
    else:
        cart = []
    return render_template('ourProducts.html', furnitureDict=furnitureDict, furnitureList=furnitureList, count=len(furnitureList), cart=cart, cartcount=len(cart))

@app.route('/deleteCart/<int:id>')
def deleteCart(id):
    db = shelve.open('storage.db', 'c')
    usersDict = db['Users']

    cart = usersDict[session["USERID"]].get_cart()
    cart.pop(id)
    usersDict[session["USERID"]].set_cart(cart)
    db['Users'] = usersDict
    db.close()

    return redirect(url_for('ourProducts'))

@app.route('/ourProducts/<int:id>/', methods=['GET', 'POST'])
def ourProductsProduct(id):
    furnitureDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Furniture storage into usersDict
    except:
        print("Error in retrieving Furniture from storage.db.")
    db.close()

    if id not in furnitureDict:
        return redirect(url_for('ourProducts'))

    item = furnitureDict[id]
    return render_template('ourProductsProduct.html', item=item)

@app.route('/addToCart/<int:id>/')
def addToCart(id):
    if session.get("USERID") != None:
        usersDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            usersDict = db['Users'] #assign Users storage into usersDict
        except:
            print("Error in retrieving Users from storage.db.")

        print(usersDict[session["USERID"]].get_cart())
        usersDict[session["USERID"]].add_To_Cart(id, id)
        print(usersDict[session["USERID"]].get_cart())

        db['Users'] = usersDict #update new 'Users' in database
        db.close() #always close your database
        return redirect(url_for('ourProducts'))
    return redirect(url_for('login'))

@app.route('/addToOrder')
def addToOrder():
    if session.get("USERID") != None:
        usersDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            usersDict = db['Users'] #assign Users storage into usersDict
        except:
            print("Error in retrieving Users from storage.db.")

        cart = usersDict[session["USERID"]].get_cart()
        if len(cart) != 0:
            User.User.orderID += 1
            orderList = usersDict[session["USERID"]].get_orderList()
            orderList[User.User.orderID] = cart
            usersDict[session["USERID"]].set_orderList(orderList)
            db['Users'] = usersDict
            db.close()
            return redirect(url_for('delivery'))
        db.close()
        return redirect(url_for('ourProducts'))
    return redirect(url_for('login'))

@app.route('/delivery')
def delivery():
    usersDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        usersDict = db['Users'] #assign Users storage into usersDict
    except:
        print("Error in retrieving Users from storage.db.")
    db.close()

    orderList = usersDict[session["USERID"]].get_orderList()
    count = len(orderList)

    return render_template('delivery.html', orderList=orderList, count=count)

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    return render_template('question.html')

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
                    if usersDict[i].get_membership() == 'Admin':
                        session["ADMIN"] = True
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

        if len(usersDict) != 0:
            usersDictKeys = list(usersDict)
            User.User.countID = usersDictKeys[-1] + 1 #new countID is the key of last item in usersDict, + 1
        else:
            User.User.countID = 1

        #create list of data into 'user' variable
        user = User.User(createUserForm.username.data,
                         createUserForm.firstName.data,
                         createUserForm.lastName.data,
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

        return redirect(url_for('login')) #go back to this page on successful post/creation
    return render_template('createUser.html', form=createUserForm) #refresh page, createUserForm variable created in line 16, for form get and post

@app.route('/logout')
def logout():
    session["USERID"] = None
    if session["ADMIN"] != None:
        session["ADMIN"] = None
    return redirect(url_for('home'))

@app.route('/profile')
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

@app.route('/changeProfile', methods=['GET', 'POST'])
def changeProfile():
    changeProfileForm = ChangeProfileForm(request.form)
    if request.method == 'POST' and changeProfileForm.validate():
        userDict = {}
        db = shelve.open('storage.db', 'w')
        userDict = db['Users']
        user = userDict.get(session["USERID"])

        user.set_firstName(changeProfileForm.firstName.data)
        user.set_lastName(changeProfileForm.lastName.data)
        user.set_gender(changeProfileForm.gender.data)
        db['Users'] = userDict
        db.close()
        return redirect(url_for('profile'))
    else:
        userDict = {}
        db = shelve.open('storage.db', 'r')
        userDict = db['Users']
        db.close()

        user = userDict.get(session["USERID"]) #retrieve user data of specific id into user variable
        changeProfileForm.firstName.data = user.get_firstName()
        changeProfileForm.lastName.data = user.get_lastName()
        changeProfileForm.gender.data = user.get_gender()
        return render_template('changeProfile.html', form=changeProfileForm)

@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    changePasswordForm = ChangePasswordForm(request.form)
    if request.method == 'POST' and changePasswordForm.validate():
        userDict = {}
        db = shelve.open('storage.db', 'w')
        userDict = db['Users']
        user = userDict.get(session["USERID"])

        if user.get_password() != changePasswordForm.oldPassword.data:
            return redirect(url_for('changePassword'))
        if changePasswordForm.newPassword.data != changePasswordForm.newPasswordConfirm.data:
            return redirect(url_for('changePassword'))

        user.set_password(changePasswordForm.newPassword.data)
        db['Users'] = userDict
        db.close()
        return redirect(url_for('profile'))
    else:
        return render_template('changePassword.html', form=changePasswordForm)
#Administrator Functions
app.config["IMAGE_UPLOADS"] = "C:/Users/trill/Desktop/1966 - App Development/Assignment/static/img/uploads" #set path, change this yourself
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG"]

def allowed_image(filename):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1] #get extension
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False
@app.route("/createFurniture", methods=["GET", "POST"])
def createFurniture():
    if request.method == "POST":
        if request.files: #if theres a file in the file input
            #------------MAKE FURNITURE DICTIONARY-------------#
            furnitureDict = {}
            db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
            try:
                furnitureDict = db['Furniture'] #assign Furniture storage into usersDict
            except:
                print("Error in retrieving Furniture from storage.db.")

            Furniture.Furniture.countID = len(furnitureDict) + 1
            furniture = Furniture.Furniture(request.form["furnitureName"], request.form["furnitureCost"], request.form["furnitureDescription"], request.form["furnitureDimensions"])
            #---------SAVING THE IMAGE--------------#
            image = request.files["image"] #assign picture into 'image'

            if image.filename == "":
                print("Image must have a filename")
                return redirect(request.url)

            if not allowed_image(image.filename):
                print("that image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(image.filename)
                ext = filename.rsplit(".", 1)[1] #get extension
                print(furniture.get_countID())
                filename = str(furniture.get_countID()) + '.' + ext #change new filename based on furniture id
                print(filename)

                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename)) #save image into this place

            print("Image saved")
            #---------------------------------------------#
            #create list of data into 'furniture' variable
            furniture.set_filename(filename) #set filename of furniture object

            furnitureDict[furniture.get_furnitureID()] = furniture #put 'furniture' object into furnitureDict
            db['Furniture'] = furnitureDict #update new 'Furniture' in database
            db.close()

            return redirect(url_for('retrieveFurniture'))
    return render_template('createFurniture.html')

@app.route('/retrieveFurniture')
def retrieveFurniture():
    furnitureDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Users storage into usersDict
    except:
        print("Error in retrieving Furniture from storage.db.")
    db.close()

    furnitureList = []
    #Insert every dictionary into usersList list
    for key in furnitureDict:
        furniture = furnitureDict.get(key)
        furnitureList.append(furniture)
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

    if session["USERID"] not in usersDict:
        session["USERID"] = None
        session["ADMIN"] = None
        return redirect(url_for('home'))

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
        user.set_firstName(updateUserForm.firstName.data)
        user.set_lastName(updateUserForm.lastName.data)
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
        updateUserForm.firstName.data = user.get_firstName()
        updateUserForm.lastName.data = user.get_lastName()
        updateUserForm.password.data = user.get_password()
        updateUserForm.membership.data = user.get_membership()
        updateUserForm.gender.data = user.get_gender()
        return render_template('updateUser.html', form=updateUserForm)

@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
    usersDict = {}
    db = shelve.open('storage.db', 'w')
    usersDict = db['Users']
    usersDict.pop(id) #remove selected id

    db['Users'] = usersDict
    db.close()

    return redirect(url_for('retrieveUsers'))

if __name__ == '__main__':
    app.run()
