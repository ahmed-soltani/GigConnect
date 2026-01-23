from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import MyUser

class MySignUpForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'profile_picture')
        # password ist wegen UserCreationForm schon mit dabei


class UpdateUserForm(ModelForm):

    class Meta:
        model = MyUser
        fields = ('profile_picture', 'first_name', 'last_name', 'email', 'date_of_birth',)