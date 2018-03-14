from base.validators import is_password_secure
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm

from .models import User


class UserRegisterForm(RegistrationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': "form-control"}),
        validators=[RegexValidator(
                        regex=is_password_secure,
                        code=_('Invalid password'))],
        )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': "form-control"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        validators=[RegexValidator(
                        regex=is_password_secure,
                        code=_('Invalid password'))],
        )

    username = forms.CharField(
        label=_("Username"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        )

    email = forms.CharField(
        label=_("Email"),
        strip=False,
        widget=forms.EmailInput(attrs={'class': "form-control"}),
        )

    tel_no = forms.CharField(
        label=_("Telephone Number"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        )

    mobile = forms.CharField(
        label=_("Mobile Number"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        )

    facebook = forms.CharField(
        label=_("Facebook Username"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=False,
        )

    instagram = forms.CharField(
        label=_("Instagram Username"),
        strip=False,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        required=False,
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'tel_no', 'mobile', 'facebook', 'instagram')


class LoginForm(forms.Form):
    email = forms.CharField(label=_("Email"), required=True,
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _('Your email')}))
    password = forms.CharField(label=_("Password"), max_length=32,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': _('Your password')}),
                               required=True, validators=[
                                    RegexValidator(
                                        # regex=is_password_secure,
                                        code=_('Invalid password'))],)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                username = get_user_model().objects.get(email=email).username
            except:
                raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))
        return self.cleaned_data
