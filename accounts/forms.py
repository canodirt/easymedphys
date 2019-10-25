from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import CustomUser, getOccupationChoices
from crispy_forms.layout import Layout, Div
from crispy_forms.helper import FormHelper
from allauth.account.forms import SignupForm

# class CustomUserCreationForm(UserCreationForm):
#
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email',  'first_name', 'last_name',)
#
# class CustomUserChangeForm(UserChangeForm):
#
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email')
# from django.contrib.auth.models import User
#
#
#

# class SignUpForm(UserCreationForm):
class SignUpForm(SignupForm):

    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    first_name = forms.CharField(max_length=254, required=True)
    last_name = forms.CharField(max_length=254, required=True)
    occupation = forms.ChoiceField(choices = getOccupationChoices())
    campep = forms.BooleanField(required=False)
    mdcb = forms.BooleanField(required=False)
    class Meta:
        model = CustomUser
        # model
        #  = User
        fields = ('email', 'first_name', 'last_name', 'occupation', 'campep', 'mdcb','password1', 'password2')
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'campep':'Do you need CAMPEP credits?',
            'mdcb': 'Do you need MDCB credits?',
        }


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)



class LoginForm(forms.Form):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    password = forms.CharField(max_length=999)

    class Meta:
        model = CustomUser
        # model = User
        fields = ('email', 'password')
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')



    # def __init__(self, *args, **kwargs):
    #     super(SignUpForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
