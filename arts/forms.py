from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationFormUniqueEmail

from models import Artist, Art
from utils import date_based_slugify

class UserRegistrationForm(RegistrationFormUniqueEmail):
    first_name = forms.RegexField(regex=r'^\w+', label='First Name (optional)',
                                 required=False, max_length=30)
    last_name = forms.RegexField(regex=r'^\w+', label='Last Name (optional)',
                                 required=False, max_length=30)
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')
        plen = settings.REGISTRATION_PASSWORD_MIN_LENGTH
        if len(password1) < plen:
            raise forms.ValidationError("Password must be at least " +
                                        "{0} characters long".format(plen))
        return password1

# fill first & last name while registering a user
def user_created(sender, user, request, **kwargs):
    form = UserRegistrationForm(request.POST)
    user.first_name = form.data['first_name']
    user.last_name = form.data['last_name']
    user.save()

from registration.signals import user_registered
user_registered.connect(user_created)

class UserAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(label='E-mail')
    
    def __init__(self, request=None, *args, **kwargs):
        super(UserAuthenticationForm, self).__init__(request, *args, **kwargs)
        del self.fields['username']
        self.fields.keyOrder=['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct e-mail and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        self.check_for_test_cookie()
        return self.cleaned_data

class ArtForm(forms.ModelForm):
    class Meta:
        model = Art
        exclude = ('slug', 'artist')
    
    def __init__(self, user=None, *args, **kwargs):
        super(ArtForm, self).__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields['contributors'].queryset = Artist.objects.exclude(user=user)
    
    def save(self, *args, **kwargs):
        self.instance.slug = date_based_slugify(self.instance, 'name', 'pub_date')
        self.instance.artist = self.user.get_profile()
        super(ArtForm, self).save(*args, **kwargs)
