from django import forms
from django.contrib.auth.forms import AuthenticationForm
from . import models

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        try:
            employee = models.Employee.objects.get(user=user)
        except:
            print("!!!!!!!!!!!!!!!!!")


        # if not user.is_active or not user.is_validated:
        #     raise forms.ValidationError('There was a problem with your login.', code='invalid_login')