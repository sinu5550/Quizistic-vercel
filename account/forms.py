from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        our_user = super().save(commit=False) 
        if commit == True:
            our_user.save()

            UserProfile.objects.create(user = our_user )
        return our_user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class profilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile Picture', required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_image','user'] 
        widgets = {'user': forms.HiddenInput()}


class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]
    
    def __init__(self, *args, **kwargs):
        super(ChangeUserForm,self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        
