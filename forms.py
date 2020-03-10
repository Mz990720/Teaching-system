from wtforms.fields import simple, core
from wtforms import Form, validators, widgets, ValidationError
import calendar


class LoginForm(Form):
    username = simple.StringField(
        label='Username',
        widget=widgets.TextInput(),
        validators=[validators.DataRequired(message="Username can not be empty")])
    password = simple.PasswordField(
        label='Password',
        widget=widgets.PasswordInput(),
        validators=[validators.DataRequired(message='Password can not be empty')])
    submit = simple.SubmitField(
        label='Submit',
        widget=widgets.SubmitInput()
    )

class RegistrationForm(Form):
    #def validate_username(self):
        #if not verify_user_register(self.realname.data,self.citizenid.data):
            #raise ValidationError(u'Real Name not match CitizenId')
    username = simple.StringField(
        label='Username',
        widget=widgets.TextInput(),
        validators=[validators.DataRequired(message="Username can not be empty")])
    password = simple.PasswordField(
        label='Password',
        widget=widgets.PasswordInput(),
        validators=[validators.DataRequired(message='Password can not be empty')])
    email = simple.StringField(
        label='Email',
        widget=widgets.TextInput(),
        validators=[validators.DataRequired(message='Email can not be empty'),
                    validators.Email(message='Wrong Email Syntax')])
    phone = simple.StringField(
        label='Phone',
        widget=widgets.TextInput(),
        validators=[validators.DataRequired(message="phone can not be empty")])
    submit = simple.SubmitField(
        label='Submit',
        widget=widgets.SubmitInput())

