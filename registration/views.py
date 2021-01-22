from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from registration.forms import UserCreationFormWithEmail 
from django.urls import reverse_lazy
from django import forms
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SignupView(CreateView):
    form_class=UserCreationFormWithEmail
    template_name='registration/registro.html'

    def get_success_url(self):
        return reverse_lazy('login')+'?register'
    
    def get_form(self,form_class=None):
        form=super(SignupView,self).get_form()
        form.fields['username'].widget=forms.TextInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Nombre de usuario'})
        form.fields['email'].widget=forms.EmailInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Dirección email'})
        form.fields['password1'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Contraseña'})
        form.fields['password2'].widget=forms.PasswordInput(attrs={'class':'form-control mb2',
                                                    'placeholder':'Repite la contraseña'})
        return form
