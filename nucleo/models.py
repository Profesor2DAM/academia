from django.db import models

class Persona(models.Model):
    nombre=models.CharField(max_length=30)
    apellido=models.CharField(max_length=30)

class Business(models.Model):
    name=models.CharField(max_length=50,verbose_name="Nombre")
    city=models.CharField(max_length=50,verbose_name="Ciudad")

    class Meta:
        verbose_name="Empresa"
        verbose_name_plural="Empresas"

    def __str__(self):
        return self.name

class Employees(models.Model):
    firstName= models.CharField(max_length=50,verbose_name="Nombre")
    lastName=models.CharField(max_length=50,verbose_name="Apellido")
    date=models.DateField(verbose_name="Fecha de Nacimiento")
    photo=models.ImageField(upload_to='photos/',verbose_name="Foto")
    business=models.ForeignKey(Business,on_delete=models.CASCADE,verbose_name="Empresa")

    class Meta:
        verbose_name="Empleado"
        verbose_name_plural="Empleados"

    def __str__(self):
        return self.firstName+" "+self.lastName+" "+self.business.name