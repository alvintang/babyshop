from base.decorators import anonymous_required

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import password_validators_help_texts
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from registration.backends.hmac.views import RegistrationView as ActivationRegistrationView
from registration.backends.simple.views import RegistrationView

from .forms import UserRegisterForm, LoginForm

User = get_user_model()

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@method_decorator(anonymous_required(redirect_url='index'), name='dispatch')
class UserActivationRegisterView(ActivationRegistrationView):
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super(UserActivationRegisterView, self).get_context_data(**kwargs)
        context["password_rules"] = password_validators_help_texts()
        return context

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is simply the
        username, signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user
        })
        subject = render_to_string('registration/activation_email_subject.txt',
                                   context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message_text = render_to_string('registration/activation_email.txt', context)
        message_html = render_to_string('registration/activation_email.html', context)

        msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [user.email, 'issa@babysetgo.ph', 'issarufinasenga@gmail.com'])
        msg.attach_alternative(message_html, "text/html")
        msg.send()


@method_decorator(anonymous_required(redirect_url='index'), name='dispatch')
class UserNormalRegisterView(RegistrationView):
    form_class = UserRegisterForm

@method_decorator(anonymous_required(redirect_url='index'), name='dispatch')
class UserLoginView(RegistrationView):
    template_name = 'registration/login.html'
    form_class = LoginForm


@method_decorator(login_required(login_url='index'), name='dispatch')
class HomeView(TemplateView):
    """
    Home view
    """
    template_name = 'registry/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['authenticated'] = self.request.user.is_authenticated()
        if context['authenticated']:
            context['user_detail'] = User.objects.get(username=self.request.user)
        return context
