from django.contrib import admin
from nucleo.models import Business,Employees
from django import forms


class EmployeeAdminForm(forms.ModelForm):
    def clean_firstName(self):
        if len(self.cleaned_data['firstName'])<3:
            raise forms.ValidationError('First Name is very short')
        else:
            return self.cleaned_data['firstName']

class EmployeeAdmin(admin.ModelAdmin):
    form=EmployeeAdminForm

class EmployeInLine(admin.TabularInline):
    model=Employees

class BusinessAdmin(admin.ModelAdmin):
    list_filter=['city']
    ordering=['name']
    list_per_page=3
    inlines=[EmployeInLine,]
    
# Register your models here.
admin.site.register(Business,BusinessAdmin)
admin.site.register(Employees,EmployeeAdmin)
