from django import forms
from nucleo.models import Business

class ContactFormAntiguo(forms.Form):
    name=forms.CharField(label="Nombre",required=True)
    email=forms.EmailField(label="Email",required=True)
    content=forms.CharField(label="Contenido",required=True,widget=forms.Textarea)

class ContactForm(forms.Form):
    name=forms.CharField(label="Nombre", required=True, widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Escribe tu nombre'}
    ))
    email=forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder':'Escribe tu email'}
        ))
    
    content=forms.CharField(label="Contenido",required=True,widget=forms.Textarea(
        attrs={'class':'form-control','rows':3,'placeholder':'Escribe tu mensaje'}))

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Business
        fields="__all__"

    