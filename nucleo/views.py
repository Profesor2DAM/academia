from django.shortcuts import redirect, render
import datetime
from django.http import HttpResponse
from nucleo.models import Business, Employees
from django.http.response import Http404
from nucleo.forms import BusinessForm, ContactForm
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from webpersonal import settings
from reportlab.pdfgen import canvas
from reportlab.platypus import TableStyle, Table
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from io import BytesIO
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import EmployeesSerializers
from .models import Employees
from rest_framework import status
from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
 
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status
 
from django.contrib.auth.models import User
 
 
# Create your views here.
class TestView(APIView):
  
    def get(self, request, format=None):
        return Response({'detail': "GET Response"})
 
    def post(self, request, format=None):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Invalid JSON - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        if "user" not in data or "password" not in data:
            return Response(
                'Wrong credentials',
                status=status.HTTP_401_UNAUTHORIZED
            )
 
        user = User.objects.get(username=data["user"])
        if not user:
            return Response(
                'No default user, please create one',
                status=status.HTTP_404_NOT_FOUND
            )
 
        token = Token.objects.get_or_create(user=user)
        return Response({'detail': 'POST answer', 'token': token[0].key})

class Employees_APIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, *args, **kwargs):
        empl = Employees.objects.all()
        serializer = EmployeesSerializers(empl, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = EmployeesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Employees_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        empl = self.get_object(pk)
        serializer = EmployeesSerializers(empl)  
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        empl = self.get_object(pk)
        serializer = EmployeesSerializers(empl, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        empl = self.get_object(pk)
        empl.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InformeEmpleadosPDF(View):  
     
    def cabecera(self,pdf):
        #Utilizamos el archivo logo.png
        archivo_imagen = settings.BASE_DIR+'/nucleo/static/img/logo.png'
        #Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90,preserveAspectRatio=True)  
        #Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        #Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(230, 790, u"ACADEMIA DE ALUMNOS")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, 770, u"INFORME DE EMPLEADOS")

    def tabla(self,pdf,y):
        #Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Nombre', 'Apellido', 'Empresa')
        #Creamos una lista de tuplas que van a contener a las personas
        detalles = [(emp.firstName, emp.lastName, emp.business) for emp in Employees.objects.all()]
        #Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[5 * cm, 5 * cm, 5 * cm])
        #Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                #La primera fila(encabezados) va a estar centrada
                ('ALIGN',(0,0),(3,0),'CENTER'),
                #Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (-1, -1), 1, colors.black), 
                #El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        #Establecemos el tamaño de la hoja que ocupará la tabla 
        detalle_orden.wrapOn(pdf, 800, 600)
        #Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 60,y)
         
    def get(self, request, *args, **kwargs):
        #Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        #La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        #Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        #Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)
        #Con show page hacemos un corte de página para pasar a la siguiente
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

class EmployeeCreateView(CreateView):
    model=Employees
    fields=['firstName','lastName','date','business']
    success_url="/"

class EmployeeUpdateView(UpdateView):
    model=Employees
    fields=['firstName','lastName','date','business']
    success_url="/"

class EmployeeDeleteView(DeleteView):
    model=Employees
    success_url="/"

class EmployeeDetailView(DetailView):
    model=Employees

class EmployeeListView(ListView):
    model=Employees

class HomePageView(TemplateView):
    template_name="nucleo/empresa.html"

def contact(request):
    contact_form=ContactForm()

    if request.method=="POST":
        contact_form=ContactForm(data=request.POST)
        if contact_form.is_valid():
            name=request.POST.get('name','')
            email=request.POST.get('email','')
            content=request.POST.get('content','')
            #Suponemos que todo ha ido bien, redireccionamos
            return redirect(reverse('contact')+"?ok")

    return render(request,"nucleo/contact.html",{'form':contact_form})

def createBusiness(request):
    if request.method=="POST":
        form=BusinessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listBusiness')
    else:
        form=BusinessForm()
    return render(request,"nucleo/createBusiness.html",{'form':form})

def fecha_actual(request):
    hoy=datetime.datetime.now()
    html="<html><body>Hoy es %s.</body></html>" % hoy
    return HttpResponse(html)

def index(request):
    listEmployees=Employees.objects.order_by("-firstName")
    context={'employees':listEmployees}
    return render(request,'nucleo/index.html',context)

def employeeDetail(request,employee_id):
    try:
        empl=Employees.objects.get(pk=employee_id)
    except empl.DoesNotExist:
        raise Http404('Employee not exists')
    context={'empl':empl}
    return render(request,"nucleo/detail.html",context)

def listBusiness(request):
    business=Business.objects.all()
    context={'business':business}
    return render(request,"nucleo/listBusiness.html",context)

class HomePageView(TemplateView):
    template_name="nucleo/empresa.html"