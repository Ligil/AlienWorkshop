from flask import Flask, flash, render_template, request, session, redirect, url_for, jsonify, make_response
from flask_mail import Mail, Message
from Forms import CreateUserForm, UpdateUserForm, LoginForm, ChangeProfileForm, ChangePasswordForm, FurnitureForm, ForgotPasswordForm, NewPasswordForm, CreateOrderForm, QuestionForm, QuestionReplyForm, CreateCreditCardForm, ReviewForm, UpdateFurnitureForm
import random, decimal, collections
import shelve, User, Furniture, Question, Review
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta, datetime

app = Flask(__name__)
app.secret_key = "autismo's gallery"

app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'AlienatedWorkshop@gmail.com',  # enter your email here
    MAIL_DEFAULT_SENDER = 'AlienatedWorkshop@gmail.com', # enter your email here
    MAIL_PASSWORD = 'AlienatedWorkingshop' # enter your password here
))
#https://myaccount.google.com/security#signin
mail = Mail(app)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

########################################################

@app.route('/')
def home():
    furnitureDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Furniture storage into furnitureDict
    except:
        print("Error in displaying home page carousel")

    homeDisplayList = []
    try:
        homeDisplayList = db['HomeDisplay']
    except:
        pass
    db.close()

    homeDisplayObjectList = []
    for id in homeDisplayList:
        homeDisplayObjectList.append(furnitureDict[id])

    sortedList = []
    if len(homeDisplayObjectList) == 0:
        count = 0
    else:
        loops = (len(homeDisplayObjectList) - 1) // 3 #(0-2, 3-5,
        for i in range(loops):
            base = i * 3
            miniList = [homeDisplayObjectList[base], homeDisplayObjectList[base+1], homeDisplayObjectList[base+2]]
            sortedList.append(miniList)

        miniList = []
        extra = len(homeDisplayObjectList) - loops * 3
        for j in range(extra):
            base = 3 * loops
            miniList.append(homeDisplayObjectList[base + j])
        sortedList.append(miniList)

    count = len(homeDisplayObjectList)
    return render_template('home.html', display=sortedList, count=count)

@app.route('/tags_click', methods=["POST"])
def tagclick():
    req = request.get_json() #convert json object into python dict

    tagsDict = {'allTags':[]}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        tagsDict = db['Tags']
    except:
        print("Error in retrieving Tags from storage.db.")
    db.close()

    tagsDict.pop('allTags')
    res = make_response(jsonify(tagsDict), 200)
    return res

@app.route('/unload_tag', methods=["POST"])
def unloadTag():
    session['SELECTTAG'] = None
    res = make_response(jsonify('Hello!'), 200)
    return res

@app.route('/ourProducts', methods=['GET', 'POST'])
def ourProducts():
    furnitureDict = {}
    tagsDict = {'allTags':[]}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Furniture storage into furnitureDict
    except:
        print("Error in ourproducts page")
    try:
        tagsDict = db['Tags']
    except:
        print("Error in retrieving Tags from storage.db.")
    db.close()

    furnitureList = []
    #Insert every dictionary into furnitureList list
    for key in furnitureDict:
        furniture = furnitureDict.get(key)
        furnitureList.append(furniture)

    tagsList = tagsDict['allTags']
    tagsList.sort()
    converter = tagsDict.pop('allTags')

    searchValue = None
    if request.method == 'POST':
        searchValue = request.form.get('search')

    return render_template('ourProducts.html', furnitureDict=furnitureDict, furnitureList=furnitureList,
                           count=len(furnitureList),
                           tagsList=tagsList, tagsToId=converter, searchValue=searchValue)

@app.route('/deleteCart/<int:id>', methods=['GET', 'POST'])
def deleteCart(id):
    db = shelve.open('storage.db', 'c')
    usersDict = db['Users']

    cart = usersDict[session["USERID"]].get_cart()
    cart.pop(id)
    usersDict[session["USERID"]].set_cart(cart)
    db['Users'] = usersDict
    db.close()

    return redirect(url_for('cart'))

@app.route('/ourProducts/<int:id>/', methods=['GET', 'POST'])
def ourProductsProduct(id):
    #-----------------------------------------------#
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    #-----------------------------------------------#
    furnitureDict = {}
    try:
        furnitureDict = db['Furniture'] #assign Furniture storage into usersDict
    except:
        print("error in product itself")
    #-----------------------------------------------#
    usersDict = {}
    try:
        usersDict = db['Users']
    except:
        pass
    #-----------------------------------------------#

    #check if valid id in url
    if id not in furnitureDict:
        return redirect(url_for('ourProducts'))

    #Add review
    bought = None
    usersDict = db['Users']
    form = ReviewForm()
    if session.get('USERID') != None:
        userId = session['USERID']
        currentUserObject = usersDict[userId]
        boughtList = currentUserObject.get_boughtItems()
        if id in boughtList:
            bought = True
        if request.method == 'POST':
            #---------- Retrieve Reviews from furnitureObject--------#
            furnitureObject = furnitureDict[id]
            reviewsDict = furnitureObject.get_reviews()
            #Set review id
            try:
                reviewsDict['lastId'] += 1
            except:
                reviewsDict['lastId'] = 1
            reviewId = reviewsDict['lastId'] #For saving into furnitureObject Reviews

            #------------Creating Object------------#
            reviewText = form.review.data
            stars = int(request.form.get('star'))
            now = datetime.now()
            timePosted = now.strftime("%d/%m/%Y %H:%M")
            print(timePosted)
            print(reviewText, stars, userId, timePosted)

            gender = currentUserObject.get_gender()
            if gender == 'M':
                imgFilename = 'male.png'
            else:
                imgFilename = 'female.png'
            reviewObject = Review.Review(reviewId, reviewText, stars, userId, timePosted, imgFilename)
            #---------SAVING THE IMAGE, IF IMAGE HAS DATA--------------#
            f = form.image.data
            print(f)
            if f != None: #if there is data, save it
                print('Saving image')
                if f.filename == "":
                    print("Image must have a filename")
                    return redirect(request.url)
                if not allowed_image(f.filename):
                    print("that image extension is not allowed")
                    return redirect(request.url)
                else:
                    filename = secure_filename(f.filename)
                    ext = filename.rsplit(".", 1)[1] #get extension
                    filename = str(furnitureObject.get_furnitureID()) + 'review' + str(reviewId) + '.' + ext
                    f.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    reviewObject.set_filename(filename)
            #--------------Saving Reviews in FurnitureObject ReviewsDict----------------#
            reviewsDict[reviewId] = reviewObject
            furnitureObject.set_reviews(reviewsDict) #Furniture object is now updated
            print('Reviews in furnitureObject:', furnitureObject.get_reviews())
            #---------Making user object record reviews made --------#
            reviewsDict = currentUserObject.get_reviewsDict()
            if id not in reviewsDict:
                reviewsDict[id] = [reviewId]
            else:
                reviewsForFurniture = reviewsDict[id]
                reviewsForFurniture.append(reviewId)
                reviewsDict[id] = reviewsForFurniture
            print('Reviews:', reviewsDict)
            currentUserObject.set_reviewsDict(reviewsDict)
            #--------Saving Users and Furniture--------#
            usersDict[userId] = currentUserObject
            db['Users'] = usersDict
            furnitureDict[id] = furnitureObject
            db['Furniture'] = furnitureDict
            db.close()                               #SHELVE CLOSE
            return redirect(request.url)

    #--------------Continue here if not form submit-------------#
    #-------------------Retrieve more data----------------------#
    tagsDict = {'allTags':[]}
    try:
        tagsDict = db['Tags']
    except:
        print("Error in retrieving Tags from storage.db")
    #-----------------------------------------------#
    db.close()
    #-------------Start Code-------------#
    item = furnitureDict[id]
    #------------------------------------Review List --------------------------------------#
    #------Part 1 - List of review objects----#
    reviewsDict = item.get_reviews()
    reviewObjectList = []
    for reviewsKey in reviewsDict:
        if reviewsKey == 'lastId' or reviewsKey == 'stars':
            continue
        reviewObject = reviewsDict[reviewsKey]
        reviewObjectList.append(reviewObject)
    starCount = round(item.get_stars())
    starCount1dp = item.get_stars()
    reviewCount = len(reviewsDict) - 1
    #------Part 2 - User's Review Id List----#
    userReviewList = []
    if session.get('USERID') != None:
        currentUserObject = usersDict[session['USERID']]
        currentUserReviewsDict = currentUserObject.get_reviewsDict()
        if id in currentUserReviewsDict:
            userReviewList = currentUserReviewsDict[id]
    #---------------------------------Review List Done-------------------------------------#
    #--------------------------------Recommended Points------------------------------------#
    itemTagList = item.get_tags()

    recoPointDict = {} #score counter for most similar items
    tags = item.get_tags()
    for tag in tags:
        for idTag in tagsDict[tag]:
            if idTag not in recoPointDict:
                recoPointDict[idTag] = 1
            else:
                recoPointDict[idTag] = recoPointDict[idTag] + 1

    if id in recoPointDict:
        recoPointDict.pop(id)
        print(recoPointDict)

    #If not other same tags,
    if len(recoPointDict) == 0:
        return render_template('ourProductsProduct.html', form=form, item=item, itemTagList=itemTagList, bought=bought, reviewObjectList=reviewObjectList, userReviewList=userReviewList, starCount=starCount, starCount1dp=starCount1dp, reviewCount=reviewCount, usersDict=usersDict)
    ###############################################################
    #Recommend Point Dict completed, now sort
    def by_value(id):
        return recoPointDict[id]
    sortedList = sorted(recoPointDict, key=by_value, reverse=True)
    recoListID = []
    for i in range(3):
        try:
            recoListID.append(sortedList[i])
        except:
            pass

    recoListObject = []
    for id2 in recoListID:
        recoListObject.append(furnitureDict[id2])
    #-------------------------------Recommended Points Done ------------------------------#
    return render_template('ourProductsProduct.html', form=form, item=item, itemTagList=itemTagList, bought=bought, reviewObjectList=reviewObjectList, userReviewList=userReviewList, starCount=starCount, starCount1dp=starCount1dp, reviewCount=reviewCount, usersDict=usersDict, recoList=recoListObject)

@app.route('/deleteReview/<int:reviewId>/<int:furnitureId>', methods=['GET', 'POST'])
def deleteReview(reviewId, furnitureId):
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    furnitureDict = db['Furniture'] #assign Furniture storage into usersDict
    usersDict = db['Users']

    furnitureReviewList = furnitureDict[furnitureId].get_reviews()
    furnitureReviewObject = furnitureReviewList[reviewId]

    userReviewsDict = usersDict[furnitureReviewObject.get_userId()].get_reviewsDict()
    userReviewsDict[furnitureId].remove(reviewId)
    usersDict[furnitureReviewObject.get_userId()].set_reviewsDict(userReviewsDict)

    furnitureReviewList.pop(reviewId)
    furnitureDict[furnitureId].set_reviews(furnitureReviewList)


    db['Users'] = usersDict
    db['Furniture'] = furnitureDict
    db.close()
    return redirect(url_for('ourProductsProduct', id=furnitureId))


@app.route('/ourProducts/tag/<string:tag>')
def productsTag(tag):
    session['SELECTTAG'] = tag
    return redirect(url_for('ourProducts'))

@app.route('/addToCart/<int:id>', methods=["POST"])
def addToCart(id):

    usersDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        usersDict = db['Users'] #assign Users storage into usersDict
    except:
        print("Error in retrieving Users from storage.db.")

    req = request.form
    quantity = int(req["quantity"])
    usersDict[session["USERID"]].add_To_Cart(id, quantity)
    print(usersDict[session["USERID"]].get_cart())
    db['Users'] = usersDict
    db.close()
    return redirect(url_for('cart'))

@app.route('/Cart')
def cart():
    if session.get("USERID") == None:
        return redirect(url_for('login'))
    db = shelve.open('storage.db', 'c')
    usersDict = {}
    try:
        usersDict = db['Users']
    except:
        print("Error in retrieving Users from storage.db.")

    furnitureDict = {}
    try:
        furnitureDict = db['Furniture']
    except:
        pass
    db.close()
    cartDict = usersDict[session["USERID"]].get_cart() #{id:quantity}
    totalCost = decimal.Decimal(0)
    for furnitureId in cartDict:
        print(furnitureDict[furnitureId].get_cost())
        totalCost += (furnitureDict[furnitureId].get_cost() * cartDict[furnitureId])

    currentUser = usersDict[session["USERID"]]
    totalSpent = currentUser.get_totalSpent()
    privilege = None
    totalDiscount = None
    discount = 0
    if totalSpent > 1000:
        privilege = 'Gold'
        totalDiscount = round(totalCost * decimal.Decimal(0.075), 2)
        discount = 7.5
    elif totalSpent > 500:
        privilege = 'Silver'
        totalDiscount = round(totalCost * decimal.Decimal(0.045), 2)
        discount = 4.5
    elif totalSpent > 200:
        privilege = 'Bronze'
        totalDiscount = round(totalCost * decimal.Decimal(0.02), 2)
        discount = 2

    return render_template('cartPage.html', cartDict=cartDict, cartcount=len(cartDict), furnitureDict=furnitureDict, totalCost=totalCost, totalDiscount=totalDiscount, privilege=privilege, totalSpent=totalSpent, discount=discount)

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

#daniel start
@app.route('/paymentmethod',methods=['GET',"POST"])
def paymentmethod():
    if session.get("USERID") != None:
        usersDict = {}
        db = shelve.open('storage.db', 'c')
        try:
            usersDict = db['Users'] #assign Users storage into usersDict
        except:
            pass
        db.close()
        currentuser = usersDict[session.get("USERID")]
        creditcarddict = currentuser.get_creditcard()

        creditcards = {}
        mcclist = []
        visalist = []
        for creditcardsid in creditcarddict:
            currentcreditcard = creditcarddict[creditcardsid]
            ccnumber = currentcreditcard.get_creditcardnumber()
            strccname = str(ccnumber)
            cclen = len(strccname) -4
            replacedccn = strccname[0:-4].replace(strccname[0:-4],cclen * "*")
            newdisplayccn = replacedccn + strccname[-4:]
            currentcreditcard.set_creditcardnumber(newdisplayccn)
            if currentcreditcard.get_creditcardtype() == "Mastercard":
                mcclist.append(currentcreditcard)
            elif currentcreditcard.get_creditcardtype() == "Visa":
                visalist.append(currentcreditcard)

        creditcards['Mastercard'] = mcclist
        creditcards['Visa'] = visalist
        if request.method == 'POST':
            if request.form.get('selectcreditcard') is None:
                return redirect(url_for("paymentmethod"))
            else:
                db = shelve.open('storage.db', 'c')
                ccId = int(request.form.get('selectcreditcard'))
                session['currentCCCardId'] = ccId
                db['Users'] = usersDict
                db.close()
                return redirect(url_for("confirmationorder"))
        db.close()
        return render_template("paymentmethod.html",creditcarddict = creditcards)
    return redirect(url_for('login'))

@app.route('/addcreditcard',methods=['GET', 'POST'])
def addcreditcard():
    if session.get("USERID") != None:
        createCreditCardForm = CreateCreditCardForm(request.form)

        db = shelve.open('storage.db', 'c')
        usersdict = db['Users']
        currentuser = usersdict[session.get("USERID")]

        if request.method == 'POST' and createCreditCardForm.validate():
            #set new credit card id
            if currentuser.get_creditcardID() != 0:
                counter = currentuser.get_creditcardID() + 1
                currentuser.set_creditcardID(counter)
            else:
                currentuser.set_creditcardID(1)
            print("CCD",createCreditCardForm.expirationdate.data)
            testdate = date.today()
            print(testdate)
            ccdict = currentuser.get_creditcard()
            for creditcards in ccdict:
                print(creditcards)
            creditCardObject = User.Creditcard(createCreditCardForm.cctype.data,
                                               createCreditCardForm.ccnumber.data,
                                               createCreditCardForm.ccscode.data,
                                               createCreditCardForm.expirationdate.data,
                                               createCreditCardForm.billinginformationname.data,
                                               createCreditCardForm.city.data,
                                               createCreditCardForm.billingaddress.data,
                                               createCreditCardForm.postalcode.data,
                                               createCreditCardForm.country.data,
                                               createCreditCardForm.phonenumber.data,
                                               currentuser.get_creditcardID())

            #insert credit card into current user object
            creditCardDict = currentuser.get_creditcard() #{id:object}
            creditCardDict[currentuser.get_creditcardID()] = creditCardObject
            currentuser.set_creditcard(creditCardDict)
            db['Users'] = usersdict
            db.close()
            return redirect(url_for("paymentmethod"))
        return render_template("addcreditcard.html",form=createCreditCardForm)
    return redirect(url_for('login'))

@app.route('/displaydeletecreditcards')
def displaydeletecreditcards():
    if session.get("USERID") == None:
            return redirect(url_for('home'))
    db = shelve.open('storage.db', 'c')
    userDict = db['Users']
    db.close()
    currentuser = userDict[session.get("USERID")]
    creditcards = currentuser.get_creditcard()
    cclist = []
    for creditcard in creditcards:
        creditcardobject = creditcards[creditcard]
        print(creditcardobject.get_creditCardCount())

        ccnumber = creditcardobject.get_creditcardnumber()
        strccname = str(ccnumber)
        cclen = len(strccname) -4
        replacedccn = strccname[0:-4].replace(strccname[0:-4],cclen * "*")
        newdisplayccn = replacedccn + strccname[-4:]
        print(newdisplayccn)
        creditcardobject.set_creditcardnumber(newdisplayccn)
        creditcardobject.set_securitycode("***")
        cclist.append(creditcardobject)
    return render_template('displaydeletecreditcards.html',cclist = cclist)

@app.route('/deleteCreditCard/<int:id>', methods=['POST'])
def deleteCreditCard(id):
    print("hello",id)
    usersDict = {}
    db = shelve.open('storage.db', 'w')
    usersDict = db['Users']
    currentuser = usersDict[session.get("USERID")]
    ccdict = currentuser.get_creditcard()
    print("testing",currentuser.get_creditcard())
    ccdict.pop(id)

    currentuser.set_creditcard(ccdict)
    print(currentuser.get_creditcard())
    db['Users'] = usersDict
    db.close()
    return redirect(url_for('displaydeletecreditcards'))

@app.route('/confirmationorder',methods=['GET', 'POST'])
def confirmationorder():
    if session['currentCCCardId'] == None:
        return redirect(url_for('home'))

    db = shelve.open('storage.db', 'c')
    userDict = db['Users']
    currentUser = userDict[session.get("USERID")]
    usersCardId = session['currentCCCardId']
    creditCardDict = currentUser.get_creditcard()
    #start of change for replace string slicing
    ccobject = creditCardDict[usersCardId]
    strccname = str(ccobject.get_creditcardnumber())
    cclen = len(strccname) -4
    replacedccn = strccname[0:-4].replace(strccname[0:-4],cclen * "*")
    newdisplayccn = replacedccn + strccname[-4:]
    #string slice this \/
    #end of change for replace
    createOrderForm = CreateOrderForm(request.form)
    if request.method == 'POST' and createOrderForm.validate(): #only runs if post button clicked
        session['currentCCCardId'] = None
        userCart = currentUser.get_cart()

        furnitureDict = db['Furniture']
        totalPrice = 0
        furnitureList = []
        for furnitureId in userCart:#get cart stuff in a for loop
            furnitureObject = furnitureDict[furnitureId]
            newfurnitureObject = Furniture.CartFurniture(furnitureObject.get_name(),furnitureObject.get_cost(), furnitureObject.get_description(), furnitureObject.get_length(), furnitureObject.get_width(),furnitureObject.get_height(), furnitureObject.get_filename(),userCart[furnitureId], furnitureId)
            furnitureTotalcost = newfurnitureObject.get_totalprice()
            totalPrice += furnitureTotalcost
            furnitureList.append(newfurnitureObject)

        if currentUser.get_totalSpent() > 1000:
            totalPrice = round(totalPrice * 0.925, 2)
        elif currentUser.get_totalSpent() > 500:
            totalPrice = round(totalPrice * 0.955, 2)
        elif currentUser.get_totalSpent() > 200:
            totalPrice = round(totalPrice * 0.98, 2)
        #set time
        currentdate = date.today()

        eta4 = 4
        currentdate4 = currentdate - timedelta(days=eta4)
        eta3 = 3
        deliverydate4 = currentdate4 + timedelta(days=eta3)
        #currentdate3 = currentdate - timedelta(days=eta3)
        # deliverydate3 = currentdate3 + timedelta(days=eta3)
        eta5 = 5
        currentdate5 = currentdate - timedelta(days=eta5)
        deliverydate5 = currentdate5 + timedelta(days=eta3)
        eta = 3
        deliverydate = date.today() + timedelta(days=eta)

        try:
          db['OrderID'] = db['OrderID'] + 1
        except:
          db['OrderID'] = 1
        ordersDict = currentUser.get_orderDict()
        orderObject = User.Orders(session.get("USERID"),db['OrderID'],currentdate, deliverydate, totalPrice, furnitureList,createOrderForm.phonenumber.data,createOrderForm.postalcode.data,createOrderForm.country.data,createOrderForm.deliveryaddress.data,ccobject.get_creditcardnumber(),ccobject.get_creditcardtype())
        ordersDict[db['OrderID']] = orderObject # store order in the dict
        currentUser.set_orderDict(ordersDict)
        userDict[session.get("USERID")] = currentUser

        currentUser.set_cart({})

        db['Users'] = userDict
        db.close()
        return redirect(url_for('orderhistory'))
    return render_template('confirmationorder.html', form=createOrderForm, ccobject=ccobject, displayccn = newdisplayccn)

@app.route('/orderhistory')
def orderhistory():
    if session.get("USERID") == None:
        return redirect(url_for('home'))

    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    usersDict = db['Users'] #assign Users storage into usersDict
    currentUser = usersDict[session.get("USERID")]
    db.close()
    getOrders = currentUser.get_orderDict()# now i am at 1:{ orders object }
    orderFurnitureItems = []
    completedFurnitureItems = []
    for orderId in getOrders:
        orderobject = getOrders[orderId]

        if orderobject.get_completionstatus() == "Incomplete":
            currentorder = getOrders[orderId]
            ccnumber = currentorder.get_ccnumber()
            strccname = str(ccnumber)
            cclen = len(strccname) -4
            replacedccn = strccname[0:-4].replace(strccname[0:-4],cclen * "*")
            newdisplayccn = replacedccn + strccname[-4:]
            print(newdisplayccn)
            currentorder.set_ccnumber(newdisplayccn)
            orderFurnitureItems.append(currentorder)
            print("Added to incomplete")
        else:
            orders = getOrders[orderId].get_orderlist()
            print("completed order",orders)
            for furnitureitem in orders:
                print(furnitureitem.get_cartfurnitureID())
    for orderId in getOrders:
        orderobject = getOrders[orderId]
        if orderobject.get_completionstatus() == "Completed":
            currentorder = getOrders[orderId]
            ccnumber = currentorder.get_ccnumber()
            strccname = str(ccnumber)
            cclen = len(strccname) -4
            replacedccn = strccname[0:-4].replace(strccname[0:-4],cclen * "*")
            newdisplayccn = replacedccn + strccname[-4:]
            currentorder.set_ccnumber(newdisplayccn)
            completedFurnitureItems.append(currentorder)
            print("Added to completed")
        else:
            orders = getOrders[orderId].get_orderlist()
            print("unsuccessful",orders)
            for furnitureitem in orders:
                print(furnitureitem.get_cartfurnitureID())
    return render_template('orderhistory.html', orderFurnitureItems=orderFurnitureItems,completedFurnitureItems = completedFurnitureItems,username=usersDict[session["USERID"]].get_username())

@app.route('/displayorders',methods=['GET', 'POST'])
def displayorders():
    if session.get("USERID") == None:
        return redirect(url_for('home'))
    else:
        usersDict = {}

        db = shelve.open('storage.db', 'c')
        usersDict = db['Users']
        orderslist = []
        completedorderslist = []
        for user in usersDict:
            orderdict = {}
            userobject = usersDict[user]
            userorders = userobject.get_orderDict()
            for order in userorders:
                userorders[order].set_orderID(str(order))
                orderslist.append(userorders[order])

        db.close()
        return render_template('displayorders.html',orderslist = orderslist)

@app.route('/change_status', methods=["POST"])
def change_status():
    req = request.get_json() #{userId:userId, orderId:orderId, status:status}
    print("Changing delivery status")
    usersDict = {}
    db = shelve.open('storage.db', 'c')
    try:
        usersDict = db['Users']
    except:
        print("Its an error, but honestly it usually means there isnt a 'Users' Key yet, which would be weird")

    usersDict = db['Users']
    currentUser = usersDict[req['userId']]
    currentOrder = currentUser.get_orderDict()[req['orderId']]
    print(currentOrder.get_deliverystatus())
    status = req["status"]
    currentOrder.set_deliverystatus(status)
    print(currentOrder.get_deliverystatus())

    db['Users'] = usersDict
    db.close()
    res = make_response(jsonify(req), 200)
    return res

@app.route('/change_completionstatus', methods=["POST"])
def change_completionstatus():
    req = request.get_json() #{userId:userId, orderId:orderId, status:status}
    print(req)
    usersDict = []
    db = shelve.open('storage.db', 'c')
    try:
        usersDict = db['Users']
    except:
        print("Its an error, but honestly it usually means there isnt a 'Users' Key yet, which would be weird")

    usersDict = db['Users']
    legitorderid = req['orderId']
    print(legitorderid)
    realorderid = legitorderid
    currentUser = usersDict[req['userId']]
    currentOrder = currentUser.get_orderDict()[realorderid]
    currentOrder.set_completionstatus(req["completionstatus"])
    print(currentOrder.get_completionstatus())

    totalCost = currentOrder.get_totalcost()
    if req["completionstatus"] == 'Completed':
        currentUser.set_totalSpent(currentUser.get_totalSpent() + totalCost)
    else:
        currentUser.set_totalSpent(currentUser.get_totalSpent() - totalCost)


    completedOrdersDict = {}
    db = shelve.open('storage.db', 'c')
    try:
        completedOrdersDict = db['CompletedOrders']
    except:
        pass

    #Bought Items
    if req["completionstatus"] == 'Completed':
        print('Set Complete bought items')
        boughtList = currentUser.get_boughtItems()
        orderList = currentOrder.get_orderlist()
        for object in orderList:
            id = object.get_cartfurnitureID()
            print(id)
            if id not in boughtList:
                boughtList.append(id)
            print(boughtList)
        currentUser.set_boughtItems(boughtList)

        completedOrdersDict[currentOrder.get_orderID()] = currentOrder

    elif req["completionstatus"] == 'Incomplete':
        print('Set incomplete bought items')
        boughtList = currentUser.get_boughtItems()
        orderList = currentOrder.get_orderlist()
        for object in orderList:
            id = object.get_cartfurnitureID()
            print(id)
            if id in boughtList:
                boughtList.remove(id)
            print(boughtList)
        currentUser.set_boughtItems(boughtList)

        completedOrdersDict.pop(currentOrder.get_orderID())

    db['CompletedOrders'] = completedOrdersDict
    db['Users'] = usersDict
    db.close()
    res = make_response(jsonify(req), 200)
    return res
#daniel end

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/question', methods=['GET', 'POST'])
def question(): #def function
    if session.get("USERID") == None: #retieve userid from session
        return redirect(url_for('login'))#redirect

    form = QuestionForm(request.form)
    if request.method == 'POST' and form.validate(): #only runs if post button clicked/validation of forms
        qnDict = {} #create dictionary
        db = shelve.open('storage.db', 'c')#open storage
        try:
            qnDict = db['Questions']#get question from storage
        except:
            pass

        userId = db['Users'].get(session['USERID']).get_userID() #get userId from storage

        try:
            qnDict['lastId'] += 1
        except:
            qnDict['lastId'] = 1
        questionId = qnDict['lastId']

        now = datetime.now()
        timePosted = now.strftime("%d/%m/%Y %H:%M")

        questionObject = Question.Question(userId, questionId, form.question.data, timePosted)#put all through the function question in the class question
        qnDict[questionId] = questionObject #store question inside dictionary

        db['Questions'] = qnDict #put qustion inside database {1:<object>, 2:<object>, 3:<object>, 'lastId':3}
        db.close() #close the storage

        return render_template('question.html', complete=True)
    return render_template('question.html', form=form)

@app.route('/retrievequestions')
def retrievequestions():
    if session.get("USERID") == None: #retieve userid from session
        return redirect(url_for('home'))#redirect

    db = shelve.open('storage.db', 'c')
    qnDict = {}
    try:
        qnDict = db['Questions']
    except:
        pass
    db.close()

    print(qnDict)
    questionList = []
    for questionId in qnDict: #look through qndict
        if questionId == 'lastId':
            continue
        questionObject = qnDict[questionId]
        questionList.append(questionObject)
    print(questionList)
    return render_template('adminQuestionDisplay.html', questionList=questionList) #display page

@app.route('/adminReplies/<int:id>', methods=['GET', 'POST'])
def adminReplies(id): #def function
    if session.get("USERID") == None: #retieve userid from session
        return redirect(url_for('home'))#redirect

    form = QuestionReplyForm(request.form)
    if request.method == 'POST' and form.validate(): #only runs if post button clicked/validation of forms
        db = shelve.open('storage.db', 'c')
        qnDict = {}
        try:
            qnDict = db['Questions']
        except:
            pass

        questionObject = qnDict[id]
        questionObject.set_answer(form.reply.data)

        db['Questions'] = qnDict
        db.close()
        return redirect(url_for('retrievequestions'))
    return render_template('questionReply.html', form=form)

@app.route('/inbox')
def inbox():
    if session.get("USERID") == None: #retieve userid from session
        return redirect(url_for('login'))#redirect

    db = shelve.open('storage.db', 'c')
    qnDict = {}
    try:
        qnDict = db['Questions']
    except:
        pass

    print(qnDict)
    userId = session["USERID"]
    questionList = []
    for questionId in qnDict: #look through qndict
        if questionId == 'lastId':
            continue
        questionObject = qnDict[questionId]
        if questionObject.get_userId() == userId:
            questionList.append(questionObject)
    print(questionList)
    return render_template('inbox.html', questionList=questionList)


@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm(request.form)
    db = shelve.open('storage.db', 'c')
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
                if check_password_hash(usersDict[i].get_password(), loginForm.password.data): #hashing check passwords check if pass valid

                    if usersDict[i].get_resetPassword():
                        session["RESETPWID"] = usersDict[i].get_userID()
                        return redirect(url_for('resetPassword'))

                    session["USERID"] = usersDict[i].get_userID()
                    print(session["USERID"])
                    if usersDict[i].get_membership() == 'Admin':
                        session["ADMIN"] = True
                    return redirect(url_for('home'))

        return render_template('login.html', form=loginForm, invalid=True)
    return render_template('login.html', form=loginForm)

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    form = ForgotPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        emailInput = form.email.data

        usersDict = {}
        db = shelve.open('storage.db', 'c')
        try:
            usersDict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

        recipient = None
        userID = None #pretty useless
        for id in usersDict:
            if usersDict[id].get_email() == emailInput:
                userID = id
                recipient = emailInput

        if recipient == None:
            return render_template('forgotPassword.html', form=form, noEmail=True)

        digitsDict = {}
        db = shelve.open('storage.db', 'c')
        try:
            digitsDict = db['ForgetPwDigits']
        except:
            pass

        secretDigits = ''
        while True:
            for i in range(8):
                secretDigits += str(random.randint(0,9))

            availableDigit = True
            for key in digitsDict:
                if secretDigits == digitsDict[key]:
                    availableDigit = False
            if availableDigit:
                break

        digitsDict[userID] = secretDigits
        db['ForgetPwDigits'] = digitsDict
        db.close()


        link = request.url_root + 'newPassword/' + secretDigits
        msg = Message("Recovery Email", recipients=[recipient])
        msg.body = "Click this link to reset your password --->" + link
        mail.send(msg)
        print("Data received. Sending new password link...")

        return redirect(url_for('home'))
    return render_template('forgotPassword.html', form=form)

@app.route('/newPassword/<string:digits>', methods=['GET', 'POST'])
def newPassword(digits):
    digitsDict = {}
    db = shelve.open('storage.db', 'c')
    try:
        digitsDict = db['ForgetPwDigits']
    except:
        pass
    db.close()

    userID = None
    for ID in digitsDict:
        if digitsDict[ID] == digits:
            userID = ID
    if userID == None:
        return redirect(url_for('home'))

    form = NewPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.newPassword.data != form.newPasswordConfirm.data:
            return redirect(request.url)

        db = shelve.open('storage.db', 'w')
        usersDict = db['Users']

        hashed_password = generate_password_hash(form.newPassword.data,method='sha256') #80 char hash
        (usersDict[userID]).set_password(hashed_password)

        db['Users'] = usersDict

        digitsDict.pop(userID)
        db['ForgetPwDigits'] = digitsDict

        db.close()
        return redirect(url_for('login'))
    return render_template('newPassword.html', form=form)

@app.route('/resetPassword', methods=['GET', 'POST']) #Force Reset Password
def resetPassword():
    if session["RESETPWID"] == None:
        return redirect(url_for('home'))

    form = ChangePasswordForm(request.form)
    userID = session["RESETPWID"]

    if request.method == 'POST' and form.validate():
        print('Reseting')
        usersDict = {}
        db = shelve.open('storage.db', 'w')
        usersDict = db['Users']
        user = usersDict.get(userID)
        session["RESETPWID"] = None

        if check_password_hash(user.get_password(), form.oldPassword.data) == False: #check passwords check if pass valid #sha
            return render_template('changePassword.html',invalid=True,form=form) #changes here to make feedback to the user
        if form.newPassword.data != form.newPasswordConfirm.data:
            return redirect(url_for('changePassword'))

        new_hashed_password = generate_password_hash(form.newPassword.data,method='sha256')#generate the hash password
        user.set_password(new_hashed_password)
        user.set_resetPassword(None)
        db['Users'] = usersDict
        db.close()
        return redirect(url_for('login'))
    else:
        return render_template('changePassword.html', form=form)


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

        if createUserForm.password.data != createUserForm.confirmPassword.data:
                return render_template('createUser.html', form=createUserForm, notSame=True)

        if len(usersDict) != 0:
            usersDictKeys = list(usersDict)
            User.User.countID = usersDictKeys[-1] + 1 #new countID is the key of last item in usersDict, + 1
        else:
            User.User.countID = 1

        #Hashing of passwords
        hashed_password = generate_password_hash(createUserForm.password.data,method='sha256') #80 char hash
        #create list of data into 'user' variable
        user = User.User(createUserForm.username.data,
                         createUserForm.email.data,
                         createUserForm.firstName.data,
                         createUserForm.lastName.data,
                         hashed_password,
                         createUserForm.gender.data)
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
    print(session.get("ADMIN"))
    if session.get("ADMIN") != None: #Returns None if not admin, True if admin
        session["ADMIN"] = None #if admin, set admin session to none
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
        tier = None
        rgoal = 0
        user = usersDict[session["USERID"]]
        print(user.get_totalSpent())
        if user.get_totalSpent() >= 1000:
            tier = "You are now a Gold member (7.5% off all furniture)"
            rgoal = "You are now currently in the highest tier"
        elif user.get_totalSpent() >= 500:
            tier = "You are now a Silver member (4.5% off all furniture)"
            rgoal = 1000 - user.get_totalSpent()
            rgoal = round(rgoal, 2)
        elif user.get_totalSpent() >= 200:
            tier = "You are now a Bronze member (2% off all furniture)"
            rgoal = 500 - user.get_totalSpent()
            rgoal =round(rgoal, 2)
        else:
            tier = "You are now a Default member"
            rgoal = 200 - user.get_totalSpent()
            rgoal = round(rgoal, 2)
        return render_template('profile.html', user=user, tier=tier, rgoal=rgoal)
    return redirect(url_for('login'))

@app.route('/changeProfile', methods=['GET', 'POST'])
def changeProfile():
    changeProfileForm = ChangeProfileForm(request.form)
    if request.method == 'POST' and changeProfileForm.validate():
        usersDict = {}
        db = shelve.open('storage.db', 'w')
        usersDict = db['Users']
        user = usersDict.get(session["USERID"])

        user.set_firstName(changeProfileForm.firstName.data)
        user.set_lastName(changeProfileForm.lastName.data)
        user.set_gender(changeProfileForm.gender.data)
        db['Users'] = usersDict
        db.close()
        return redirect(url_for('profile'))
    else:
        usersDict = {}
        db = shelve.open('storage.db', 'r')
        usersDict = db['Users']
        db.close()

        user = usersDict.get(session["USERID"]) #retrieve user data of specific id into user variable
        changeProfileForm.firstName.data = user.get_firstName()
        changeProfileForm.lastName.data = user.get_lastName()
        changeProfileForm.gender.data = user.get_gender()
        return render_template('changeProfile.html', form=changeProfileForm)

@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    changePasswordForm = ChangePasswordForm(request.form)
    if request.method == 'POST' and changePasswordForm.validate():
        db = shelve.open('storage.db', 'w')
        usersDict = db['Users']
        user = usersDict.get(session["USERID"])

        if check_password_hash(user.get_password(),changePasswordForm.oldPassword.data) == False: #check passwords check if pass valid #sha
            return render_template('changePassword.html',invalid=True,form=changePasswordForm) #changes here to make feedback to the user
        if changePasswordForm.newPassword.data != changePasswordForm.newPasswordConfirm.data:
            return redirect(url_for('changePassword'))

        new_hashed_password = generate_password_hash(changePasswordForm.newPassword.data,method='sha256')#generate the hash password
        user.set_password(new_hashed_password)#set the hash password
        db['Users'] = usersDict
        db.close()
        return redirect(url_for('profile'))
    else:
        return render_template('changePassword.html', form=changePasswordForm)

@app.route('/verifyEmail')
def verifyEmail():
    db = shelve.open('storage.db', 'c')
    usersDict = db['Users']

    user = usersDict[session["USERID"]]
    if user.get_emailVerified() == True:
        return render_template('verifyEmail.html', verified=True)

    digitsDict = {}
    try:
        digitsDict = db['VerifyEmailDigits']
    except:
        pass

    secretDigits = ''
    while True:
        for i in range(8):
            secretDigits += str(random.randint(0,9))

        availableDigit = True
        for key in digitsDict:
            if secretDigits == digitsDict[key]:
                availableDigit = False
        if availableDigit:
            break

    digitsDict[user.get_userID()] = secretDigits
    db['VerifyEmailDigits'] = digitsDict
    db.close()

    link = request.url_root + 'verifyEmail/' + secretDigits
    recipient = user.get_email()
    msg = Message("Verify your account", recipients=[recipient])
    msg.body = "Verify your email here -> " + link
    mail.send(msg)
    print("Data received. Sending verification email...")
    return render_template('verifyEmail.html')

@app.route('/verifyEmail/<string:digits>')
def verifiedEmail(digits):
    digitsDict = {}
    db = shelve.open('storage.db', 'c')
    try:
        digitsDict = db['VerifyEmailDigits']
    except:
        pass
    db.close()
    print(digitsDict)
    userID = None
    for ID in digitsDict:
        if digitsDict[ID] == digits:
            userID = ID
    if userID == None:
        print("redirected")
        return redirect(url_for('home'))

    #Verify Email
    digitsDict.pop(userID)
    db = shelve.open('storage.db', 'c')
    db['VerifyEmailDigits'] = digitsDict
    usersDict = db['Users']
    usersDict[userID].set_emailVerified(True)
    db['Users'] = usersDict
    db.close()
    return redirect(url_for('verifyEmail'))

@app.route('/wishlist')
def wishlist():
    if session.get("USERID") != None:
        furnitureDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            furnitureDict = db['Furniture']
        except:
            print('error')
        usersDict = db['Users'] #assign Users storage into usersDict
        db.close()

        userWishlist = usersDict[session.get("USERID")].get_wishlist() #[id, id, id]
        print(userWishlist)
        furnitureList = []
        for id in userWishlist:
            furnitureList.append(furnitureDict[id])

        return render_template('displaywishlist.html', furnitureList=furnitureList)
    return redirect(url_for('home'))

@app.route('/addToWishList/<int:id>')
def addToWishList(id):
    print(id)
    if session.get("USERID") != None:
        furnitureDict = {}
        db = shelve.open('storage.db', 'c')
        try:
            furnitureDict = db['Furniture']
        except:
            print('error')
        usersDict = db['Users']

        userWishlist = usersDict[session.get("USERID")].get_wishlist()

        if id not in furnitureDict: #check if valid id
            return redirect(url_for('home'))
        elif id not in userWishlist: #if id not in wishlist already
            userWishlist.append(id) #add it in, if not, do nothing
            usersDict[session.get("USERID")].set_wishlist(userWishlist)

        print("Wishlist: ", userWishlist)
        db['Users'] = usersDict #update new 'Users' in database
        db.close() #always close your database

        return redirect(url_for('wishlist'))
    return redirect(url_for('home'))

@app.route('/deletewishlist/<int:id>', methods=['GET','POST'])
def deletewishlist(id):
    if request.method == 'GET':
        print('get method')
        return redirect(url_for('home'))
    #otherwise, post method from wishlist page
    if session.get("USERID") != None:
        usersDict = {}
        db = shelve.open('storage.db','c')
        usersDict = db['Users']

        wishlist = usersDict[session.get('USERID')].get_wishlist() #[1]
        print(wishlist)
        print(wishlist[0] + id)
        wishlist.remove(id)
        usersDict[session.get('USERID')].set_wishlist(wishlist)

        db['Users'] = usersDict
        return redirect(url_for('wishlist'))
    print('normal home')
    return redirect(url_for('home'))


#=========================ADMINISTRATOR FUNCTIONS===========================#
app.config["IMAGE_UPLOADS"] = "C:/Users/Daniel/Desktop/appdevproject/Assignmentfinal/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPG", "PNG", "WEBP"]
def allowed_image(filename):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1] #get extension
    print('extension', ext)
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        print('True')
        return True
    else:
        return False

@app.route("/createFurniture", methods=["GET", "POST"])
def createFurniture():
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    createFurnitureForm = FurnitureForm()
    if request.method == "POST":
        print('Validated')
        #------------MAKE FURNITURE DICTIONARY-------------#
        furnitureDict = {}
        db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
        try:
            furnitureDict = db['Furniture'] #assign Users storage into usersDict
        except:
            print("error in creating furniture")

        if len(furnitureDict) != 0:
            furnitureDictKeys = list(furnitureDict)
            Furniture.Furniture.countID = furnitureDictKeys[-1] + 1 #new countID is the key of last item in usersDict, + 1
        else:
            Furniture.Furniture.countID = 1

        furniture = Furniture.Furniture(createFurnitureForm.name.data,
                 createFurnitureForm.cost.data,
                 createFurnitureForm.description.data,
                 createFurnitureForm.length.data,
                 createFurnitureForm.width.data,
                 createFurnitureForm.height.data)

        #---------SAVING THE IMAGE--------------#
        f = createFurnitureForm.image.data
        print(f)
        if f.filename == "":
            print("Image must have a filename")
            return redirect(request.url)
        if not allowed_image(f.filename):
            print("that image extension is not allowed")
            return redirect(request.url)
        else:
            filename = secure_filename(f.filename)
            ext = filename.rsplit(".", 1)[1] #get extension
            filename = str(furniture.get_furnitureID()) + '.' + ext #change new filename based on furniture id
            f.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))

        #---------------------------------------------#
        #create list of data into 'furniture' variable
        furniture.set_filename(filename) #set filename of furniture object
        furnitureDict[furniture.get_furnitureID()] = furniture #put 'furniture' object into furnitureDict

        #-------STORING TAGS--------#
        tagsDict = {'allTags':[]}
        try:
            tagsDict = db['Tags'] #assign Users storage into usersDict
        except:
            print("Error in retrieving Tags from storage.db, it is probably empty.")
        #Cleaning list, making first letter of each word in tag uppercased, and remove white spaces at start and end
        tagList = createFurnitureForm.tags.data.split('\n')
        for item in range(len(tagList)):
            if '\r' in tagList[item]:
                tagList[item] = tagList[item][:tagList[item].find('\r')]
            tagList[item] = (tagList[item].strip()).title()
        #----Store Tags into furniture---#
        furniture.set_tags(tagList)
        print(furniture.get_tags())
        #----Making tag List----#
        for tag in tagList:
            #tagsDict storing, key is tag, value is furniture id
            tagListValue = tagsDict.get(tag)
            if tagListValue != None:
                tagListValue.append(furniture.get_furnitureID())
                tagsDict[tag] = tagListValue
            else:
                tagsDict[tag] = [furniture.get_furnitureID()]
            #tagsDict storing, key is 'allTags', value is tag
            if tag not in tagsDict['allTags']:
                tagsDict['allTags'].append(tag)
        #---Final Save---#
        db['Tags'] = tagsDict
        db['Furniture'] = furnitureDict #update new 'Furniture' in database

        db.close()
        return redirect(url_for('retrieveFurniture'))

    tagsDict = {'allTags':[]}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        tagsDict = db['Tags'] #assign Users storage into usersDict
    except:
        print("Error in retrieving Tags from storage.db.")

    tagList = tagsDict['allTags']
    tagListSize = len(tagList)
    return render_template('createFurniture.html', form=createFurnitureForm, tagList=tagList, tagCount=tagListSize)

@app.route('/retrieveFurniture')
def retrieveFurniture():
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    furnitureDict = {}
    tagsDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Users storage into usersDict
    except:
        print("Error in retrieving furniture")
    try:
        tagsDict = db['Tags'] #assign Users storage into usersDict
    except:
        print("Error in retrieving Tags from storage.db.")
    db.close()

    furnitureList = []
    #Insert every dictionary into furnitureList list
    for key in furnitureDict:
        furniture = furnitureDict.get(key)
        furnitureList.append(furniture)
    return render_template('retrieveFurniture.html', furnitureList=furnitureList, count=len(furnitureList))

@app.route('/updateFurniture/<int:id>/', methods=['GET', 'POST'])
def updateFurniture(id):
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    form = UpdateFurnitureForm()
    if request.method == 'POST':
        print('Done')
        furnitureDict = {}
        db = shelve.open('storage.db', 'w')
        furnitureDict = db['Furniture']
        furniture = furnitureDict.get(id)
        furniture.set_name(form.name.data)

        #---------SAVING THE IMAGE--------------#
        if form.imageUpdate.data != None:
            f = form.imageUpdate.data
            print(f)
            if f.filename == "":
                print("Image must have a filename")
                return redirect(request.url)
            if not allowed_image(f.filename):
                print("that image extension is not allowed")
                return redirect(request.url)
            else:
                filename = secure_filename(f.filename)
                ext = filename.rsplit(".", 1)[1] #get extension
                filename = str(id) + '.' + ext #change new filename based on furniture id
                f.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            furniture.set_filename(filename) #set filename of furniture object

        #---------------------------------------------#
        furniture.set_cost(form.cost.data)

        #---- Make new tagList ----#
        tagList = form.tags.data.split('\n')
        for item in range(len(tagList)):
            if '\r' in tagList[item]:
                tagList[item] = tagList[item][:tagList[item].find('\r')]
            tagList[item] = (tagList[item].strip()).title()
        #----Remaking tagDict----#
        tagsDict = db['Tags'] #assign Users storage into usersDict
        #removing
        oldtagList = furniture.get_tags()
        for tag in oldtagList:
            tagsDict[tag].remove(id)
            if tagsDict[tag] == []:
                tagsDict.pop(tag)
                tagsDict['allTags'].remove(tag)
        #adding new
        for tag in tagList:
            #tagsDict storing, key is tag, value is furniture id
            tagListValue = tagsDict.get(tag)
            if tagListValue != None:
                tagListValue.append(id)
                tagsDict[tag] = tagListValue
            else:
                tagsDict[tag] = [id]
            #tagsDict storing, key is 'allTags', value is tag
            if tag not in tagsDict['allTags']:
                tagsDict['allTags'].append(tag)
        #------------------Final Save--------------------#
        db['Tags'] = tagsDict
        print(tagsDict)
        furniture.set_tags(tagList)
        #---------------------------#

        furniture.set_description(form.description.data)
        furniture.set_dimensions(form.length.data, form.width.data, form.height.data)
        db['Furniture'] = furnitureDict
        db.close()
        return redirect(url_for('retrieveFurniture'))
    else:
        furnitureDict = {}
        db = shelve.open('storage.db', 'r')
        furnitureDict = db['Furniture']
        tagsDict = db['Tags'] #assign Users storage into usersDict
        db.close()

        furniture = furnitureDict.get(id) #retrieve user data of specific id into user variable
        form.name.data = furniture.get_name()
        formImageSrc = "/static/img/uploads/" + furniture.get_filename()
        form.cost.data = furniture.get_cost()

        oldTagsList = furniture.get_tags()
        tagData = ''
        for tag in oldTagsList:
            if tag != oldTagsList[-1]:
                tagData = tagData + tag + '\n'
            else:
                tagData = tagData + tag
        form.tags.data = tagData

        form.description.data = furniture.get_description()
        form.length.data = furniture.get_length()
        form.width.data = furniture.get_width()
        form.height.data = furniture.get_height()

        tagList = tagsDict['allTags']
        tagListSize = len(tagList)
        return render_template('updateFurniture.html', form=form, formImageSrc=formImageSrc, tagList=tagList, tagCount=tagListSize)

@app.route('/deleteFurniture/<int:id>', methods=['POST'])
def deleteFurniture(id):
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    furnitureDict = {}
    db = shelve.open('storage.db', 'w')
    furnitureDict = db['Furniture']
    tagsDict = db['Tags'] #assign Users storage into usersDict
    #removing tags from tagsDict
    oldtagList = furnitureDict[id].get_tags()
    for tag in oldtagList:
        tagsDict[tag].remove(id)
        if tagsDict[tag] == []:
            tagsDict.pop(tag)
            tagsDict['allTags'].remove(tag)

    furnitureDict.pop(id) #remove selected id
    db['Furniture'] = furnitureDict
    db['Tags'] = tagsDict
    db.close()
    return redirect(url_for('retrieveFurniture'))

@app.route('/charts')
def charts():
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    return render_template('charts.html')

@app.route('/chartsTopPrice')
def chartsTopPrice():
    db = shelve.open('storage.db', 'c')
    furnitureDict = {}
    try:
        furnitureDict = db['Furniture']
    except:
        pass
    db.close()

    objectList = []
    for key in furnitureDict:
        objectList.append(furnitureDict[key])

    def by_highestPrice(object):
        return object.get_cost()
    objectList = sorted(objectList, key=by_highestPrice, reverse=True) #Highest first
    objectList = objectList[0:15]
    print(objectList)

    xaxis = []
    for object in objectList:
        xaxis.append(str(object.get_cost()))
    yaxis = []
    for object in objectList:
        yaxis.append(object.get_name())

    return jsonify({'xaxis':xaxis, 'yaxis':yaxis})


@app.route('/chartsLowestPrice')
def chartsLowestPrice():
    db = shelve.open('storage.db', 'c')
    furnitureDict = {}
    try:
        furnitureDict = db['Furniture']
    except:
        pass
    db.close()

    objectList = []
    for key in furnitureDict:
        objectList.append(furnitureDict[key])

    def by_highestPrice(object):
        return object.get_cost()
    objectList = sorted(objectList, key=by_highestPrice) #Highest first
    objectList = objectList[0:15]
    print(objectList)

    xaxis = []
    for object in objectList:
        xaxis.append(str(object.get_cost()))
    yaxis = []
    for object in objectList:
        yaxis.append(object.get_name())

    return jsonify({'xaxis':xaxis, 'yaxis':yaxis})

@app.route('/chartsRevenue')
def chartsRevenue():
    db = shelve.open('storage.db', 'c')
    furnitureDict = {}
    try:
        furnitureDict = db['Furniture']
    except:
        pass
    completedOrdersDict = {}
    try:
        completedOrdersDict = db['CompletedOrders']
    except:
        pass
    db.close()

    dateToSpentDict = {}
    print(completedOrdersDict)
    for orderId in completedOrdersDict:
        orderObject = completedOrdersDict[orderId]
        if orderObject.get_completionstatus() == 'Completed':
            date = orderObject.get_orderdate()
            if date not in dateToSpentDict:
                print('This should only happen 1 time')
                dateToSpentDict[date] = orderObject.get_totalcost()
            else:
                print('good')
                currentPrice = dateToSpentDict[date]
                updatedPrice = currentPrice + orderObject.get_totalcost()
                dateToSpentDict[orderObject.get_orderdate()] = round(updatedPrice, 2)


    ordered1 = collections.OrderedDict(sorted(dateToSpentDict.items(), key=lambda t: t[0]))
    ordered = {}
    for key in ordered1:
        ordered[str(key)] = ordered1[key]
    #Ordered = {date:value}
    xaxis = []
    for date in ordered:
        xaxis.append(date)
    yaxis = []
    for date in ordered:
        yaxis.append(ordered[date])
    return jsonify({'xaxis':xaxis, 'yaxis':yaxis})

@app.route('/chartsTopRated')
def chartsTopRated():
    db = shelve.open('storage.db', 'c')
    furnitureDict = {}
    try:
        furnitureDict = db['Furniture']
    except:
        pass
    db.close()

    objectList = []
    for key in furnitureDict:
        objectList.append(furnitureDict[key])

    def by_rating(object):
        return object.get_stars()
    objectList = sorted(objectList, key=by_rating, reverse=True)
    objectList = objectList[0:15]

    xaxis = []
    for object in objectList:
        xaxis.append(object.get_stars())
    yaxis = []
    for object in objectList:
        yaxis.append(object.get_name())

    return jsonify({'xaxis':xaxis, 'yaxis':yaxis})

@app.route('/retrieveUsers')
def retrieveUsers():
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    usersDict = {}
    db = shelve.open('storage.db', 'c')
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
        userObject = usersDict.get(key)
        userSHAPassword = userObject.get_password()
        shortenedPass = userSHAPassword[0:10] + '...'
        userObject.set_password(shortenedPass)
        usersList.append(userObject)
    #return sends the variable back to person
    return render_template('retrieveUsers.html', usersList=usersList, count=len(usersList))

@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = UpdateUserForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        usersDict = {}
        db = shelve.open('storage.db', 'w')
        usersDict = db['Users']
        user = usersDict.get(id)
        user.set_username(updateUserForm.username.data)
        user.set_email(updateUserForm.email.data)
        user.set_firstName(updateUserForm.firstName.data)
        user.set_lastName(updateUserForm.lastName.data)
        user.set_membership(updateUserForm.membership.data)
        user.set_gender(updateUserForm.gender.data)
        if session["USERID"] == id and updateUserForm.membership.data == 'Admin':
            session["ADMIN"] = True
        db['Users'] = usersDict
        db.close()
        return redirect(url_for('retrieveUsers'))
    else:
        usersDict = {}
        db = shelve.open('storage.db', 'r')
        usersDict = db['Users']
        db.close()

        user = usersDict.get(id) #retrieve user data of specific id into user variable
        updateUserForm.username.data = user.get_username()
        updateUserForm.email.data = user.get_email()
        updateUserForm.firstName.data = user.get_firstName()
        updateUserForm.lastName.data = user.get_lastName()
        updateUserForm.membership.data = user.get_membership()
        updateUserForm.gender.data = user.get_gender()
        return render_template('updateUser.html', form=updateUserForm)

@app.route('/resetUserPassword/<int:id>', methods=['POST'])
def resetUserPassword(id):
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    usersDict = {}
    db = shelve.open('storage.db', 'w')
    usersDict = db['Users']

    usersDict[id].set_resetPassword(True)

    db['Users'] = usersDict
    db.close()

    return redirect(url_for('retrieveUsers'))

@app.route('/deleteUser/<int:id>', methods=['POST'])
def deleteUser(id):
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))
    usersDict = {}
    db = shelve.open('storage.db', 'w')
    usersDict = db['Users']
    usersDict.pop(id) #remove selected id

    db['Users'] = usersDict
    db.close()

    return redirect(url_for('retrieveUsers'))

@app.route('/homeDisplayItems')
def displayItems():
    if session.get("ADMIN") == None:
        return redirect(url_for('home'))

    furnitureDict = {}
    db = shelve.open('storage.db', 'c') #assign storage file to variable database, c stands for read and write
    try:
        furnitureDict = db['Furniture'] #assign Furniture storage into furnitureDict
    except:
        print("Error with home display Items, no furniture")

    homeDisplayList = []
    try:
        homeDisplayList = db['HomeDisplay']
    except:
        pass
    db.close()

    furnitureList = []
    for key in furnitureDict:
        furniture = furnitureDict.get(key)
        furnitureList.append(furniture)

    return render_template('homeDisplayItems.html', list=furnitureList, homeDisplayList=json.dumps(homeDisplayList))

@app.route('/add_item', methods=["POST"])
def add_item():
    req = request.get_json() #id

    homeDisplayList = []
    db = shelve.open('storage.db', 'c')
    try:
        homeDisplayList = db['HomeDisplay']
    except:
        print("Its an error, but honestly it usually means there isnt a 'HomeDisplay' Key yet")

    if len(homeDisplayList) == 6:
        res = make_response(jsonify('Full'), 200)
        return res

    homeDisplayList.append(req)
    db['HomeDisplay'] = homeDisplayList
    db.close()

    print(homeDisplayList)
    res = make_response(jsonify(req), 200)
    return res

@app.route('/remove_item', methods=["POST"])
def remove_item():
    req = request.get_json() #id

    homeDisplayDict = {}
    db = shelve.open('storage.db', 'c')
    try:
        homeDisplayDict = db['HomeDisplay']
    except:
        print("Its an error, but honestly it usually means there isnt a 'HomeDisplay' Key yet")

    homeDisplayDict.remove(req)

    db['HomeDisplay'] = homeDisplayDict
    db.close()

    print(homeDisplayDict)
    res = make_response(jsonify(req), 200)
    return res

if __name__ == '__main__':
    app.run()


