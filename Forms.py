from wtforms import Form, StringField, PasswordField, DecimalField, IntegerField, RadioField, SelectField, TextAreaField, MultipleFileField, validators
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.widgets import html5
from wtforms.fields.html5 import DateField
from datetime import date
def emailvalidate():
    def _email(form,field):
        print(field.data)
        email = field.data or 0
        stremail = str(email)
        if stremail.endswith('.com') == True:
            print("email ends with .com")
            if stremail.endswith('@gmail.com') == True:
                print(stremail,"gmail account")
                pass
            elif stremail.endswith('@hotmail.com') == True:
                print(stremail,"hotmail account")
                pass
            elif stremail.endswith('@yahoo.com') == True:
                print(stremail,"yahoo account")
                pass
            else:
                print(stremail)
                raise ValidationError("Invalid email, (gmail,hotmail or yahoo)")
        else:
            raise ValidationError("invalid email detected, emails should end with .com")
    return _email
def validateimg():
    message = 'Images accepted only in .png and .jpg format'
    def _img(form, field):
        img = field.data or 0
        strimg = str(img)
        ext = strimg.split("(", 1)[0]
        newext = ext[15:-2]

        if newext.endswith('.png') or newext.endswith('.jpg') or newext.endswith('.webp'):
            print("Image is .png, .jpg, or .webp")
            pass
        else:
            raise ValidationError(message)
    return _img
def validateupdateimg():
    message = 'Images accepted only in .png, .webp and .jpg format'
    def _valimg(form, field):
        img = field.data or 0
        print(field.data)
        strimg = str(img)
        ext = strimg.split("(", 1)[0]
        newext = ext[15:-2]

        if img == None:
            print("empty img update")
            pass
        if newext.endswith('.png') or newext.endswith('.jpg') or newext.endswith('.webp'):
            print("Image is .png, .jpg, or .webp")
            pass
        else:
            raise ValidationError(message)
    return _valimg
def validategenders():
    message = 'Invalid Gender?'

    def _valigs(form, field):
        gender = field.data or 0
        print(gender)
        strgender = str(gender)
        if gender == "Select":
            raise ValidationError("Please Select your Gender")

        elif gender == "F" or gender == "M":
            print("gender clear")
            pass
        else:
            raise ValidationError(message)
    return _valigs

class CreateUserForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', [
        validators.Length(min=1, max=150),
        #validators.Regexp('\w+', message="Username must contain only letters numbers or underscore"),
        validators.DataRequired(),emailvalidate()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    confirmPassword = PasswordField('Confrim Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', validators = [validategenders()], choices=[('Select', 'Select'), ('F', 'Female'), ('M', 'Male')], default='Select')

class UpdateUserForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email', validators = [
        validators.Length(min=1, max=150),
        #validators.Regexp('\w+', message="Username must contain only letters numbers or underscore"),
        validators.DataRequired(),emailvalidate()])
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('Default', 'Default'), ('Admin', 'Admin')], default='Default')
    gender = SelectField('Gender', validators = [validategenders()], choices=[('Select', 'Select'), ('F', 'Female'), ('M', 'Male')], default='Select')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=1, max=150), validators.DataRequired()])

class ChangeProfileForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', validators = [validategenders()], choices=[('Select', 'Select'), ('F', 'Female'), ('M', 'Male')], default='Select')

class ChangePasswordForm(Form):
    oldPassword = PasswordField('Old Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    newPassword = PasswordField('New Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    newPasswordConfirm = PasswordField('Confirm New Password', [validators.Length(min=1, max=150), validators.DataRequired()])
def costvalidate():
    message = 'Your price must not be  $0 and below'

    def _clength(form, field):
        c = field.data or 0
        if c <= 0:
            raise ValidationError(message)

        elif c > 0:
            strc = str(c)
            if strc.count(".") >= 2:
                raise ValidationError("A price does not have more than 1 .")
            else:
                findadot = strc.find(".")
                if findadot != -1:
                    decimalc = strc[findadot:]
                    if len(decimalc) >=4:
                        raise ValidationError("Money does not have more than 2 decimal points")
                    else:
                        pass
                else:
                    pass
        else:
            raise ValidationError("Your Price may have special characters or letters in it")

    return _clength
def lwhvalidate():
    message = 'Your dimension cannot be less than 0'

    def _lwhlength(form, field):
        c = field.data or 0
        print(c)
        if c >= 0:
            print("Dimension is valid")
            pass
        else:
            raise ValidationError(message)
    return _lwhlength

class FurnitureForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Select Image (Only .JPG, .webp, and .PNG allowed)', validators=[FileRequired(),validateimg()])
    cost = DecimalField('Cost ($)',validators=[costvalidate()])
    tags = TextAreaField("Type Tags of this Furniture here (Use multiple lines to separate Tags) ", [validators.data_required()])
    description = TextAreaField('Description', [validators.data_required()])
    length = IntegerField('Length (cm)', widget=html5.NumberInput(), validators=[validators.InputRequired(),lwhvalidate()])
    width = IntegerField('Width (cm)', widget=html5.NumberInput(), validators=[validators.InputRequired(),lwhvalidate()])
    height = IntegerField('Height (cm)', widget=html5.NumberInput(), validators=[validators.InputRequired(),lwhvalidate()])


class UpdateFurnitureForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    imageUpdate = FileField('Select Image (Only .JPG, .webp, and .PNG allowed)',validators=[validateupdateimg()])
    cost = DecimalField('Cost ($)',validators=[costvalidate()])
    tags = TextAreaField("Type Tags of this Furniture here (Use multiple lines to separate Tags) ", [validators.data_required()])
    description = TextAreaField('Description', [validators.data_required()])
    length = IntegerField('Length (cm)', widget=html5.NumberInput(), validators=[validators.InputRequired(),lwhvalidate()])
    width = IntegerField('Width (cm)', widget=html5.NumberInput(), validators=[validators.InputRequired(),lwhvalidate()])
    height = IntegerField('Height (cm)', widget=html5.NumberInput(), validators=[validators.InputRequired(),lwhvalidate()])

class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [validators.data_required()])
    image = FileField('Optional Image to display (Only .JPG and .PNG allowed)')

class ForgotPasswordForm(Form):
    email = StringField('Type your email here so we can send you a recovery email', [
        validators.Length(min=1, max=150),
        #validators.Regexp('\w+', message="Username must contain only letters numbers or underscore"),
        validators.DataRequired(),emailvalidate()])

class NewPasswordForm(Form):
    newPassword = PasswordField('New Password', [validators.Length(min=1, max=150), validators.DataRequired()])
    newPasswordConfirm = PasswordField('Confirm New Password', [validators.Length(min=1, max=150), validators.DataRequired()])

def pnlength():
    message = 'Your security code should only have 8 digits'

    def _length(form, field):
        l = field.data or 0
        lenl = len(str(l))
        if lenl == 8:
            print("Phone number passed")
            pass
        else:
            raise ValidationError(message)
    return _length

class CreateOrderForm(Form):
#delete of credit cardnumber cause i can already get it from credit card
    deliveryaddress = StringField('Delivery Address ', validators=[validators.Length(min=1, max=150), validators.DataRequired()])
    postalcode = IntegerField('Postal Code', widget=html5.NumberInput(), validators=[validators.InputRequired()])
    country = SelectField('Country:', [validators.DataRequired()], choices=[('S', 'Singapore'), ('MY', 'Malaysia')], default='')
    phonenumber = IntegerField('Phone Number', widget=html5.NumberInput(), validators=[validators.InputRequired(),pnlength()])
def ccnlength():
    message = 'Credit Card Length must be 16 numbers'
    def _length(form, field):
        l = field.data or 0
        lenl = len(str(l))
        if lenl == 16:
            print("Credit card successfully added")
            pass
        else:
            raise ValidationError(message)
    return _length
def ccslength():
    message = 'Your security code should only have 3 digits'
    def _length(form, field):
        l = field.data or 0
        lenl = len(str(l))
        if lenl == 3:
            print("Credit card security code successfully added")
            pass
        else:
            raise ValidationError(message)
    return _length
def datevalidate():
    def _date(form, field):
        l = field.data or 0
        testdate = date.today()
        print(l)
        if l >= testdate:
            print("Date successfully validated")
            pass
        else:
            raise ValidationError("invalid date")
    return _date

class CreateCreditCardForm(Form):
    cctype = RadioField('Credit Card Type:', choices=[("Mastercard","Mastercard"),("Visa","Visa")],default='Mastercard',validators=[validators.DataRequired()])
    ccnumber = StringField('Credit Card Number', widget=html5.NumberInput(), validators=[validators.InputRequired(),ccnlength()])
    ccscode = StringField('Security Code', widget=html5.NumberInput(), validators=[validators.InputRequired(),ccslength()])
    expirationdate = DateField('Expiration Date',format='%Y-%m-%d', validators=[validators.DataRequired(), datevalidate()])
    billinginformationname = StringField('Full Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    city = StringField('City', [validators.Length(min=1, max=150), validators.DataRequired()])
    billingaddress = StringField('Billing ', [validators.Length(min=1, max=150), validators.DataRequired()])
    postalcode = IntegerField('Postal Code', widget=html5.NumberInput(), validators=[validators.InputRequired()])
    country = SelectField('Country:', [validators.DataRequired()], choices=[('Singapore', 'Singapore'), ('Malaysia', 'Malaysia')], default='Singapore')
    phonenumber = IntegerField('Phone Number', widget=html5.NumberInput(), validators=[validators.InputRequired(),pnlength()])

class QuestionForm(Form):
    question = StringField('Type Here', validators=[validators.InputRequired()])

class QuestionReplyForm(Form):
    reply = StringField('Reply', validators=[validators.InputRequired()])
