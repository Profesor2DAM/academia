from rest_framework import serializers
from nucleo.models import Employees

class EmployeesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees  
        fields = ['firstName', 'lastName', 'business']