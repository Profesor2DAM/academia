from django.contrib import admin
from django.urls import path
from nucleo import views
from nucleo.views import InformeEmpleadosPDF, Employees_APIView, Employees_APIView_Detail, TestView

urlpatterns = [
    path('', views.index, name="index"),
    path('detail/<int:employee_id>/',views.employeeDetail,name="EmployeeDetail"),
    path('business', views.listBusiness,name="listBusiness"),
    path('contacto',views.contact,name="contact"),
    path('empresa',views.HomePageView.as_view(),name="empresa"),
    path('createBusiness', views.createBusiness,name="createBusiness"),
    path('listEmployees',views.EmployeeListView.as_view(),name="listEmployees"),
    path('employees/<int:pk>',views.EmployeeDetailView.as_view(),name="detailEmployee"),
    path('createEmployee',views.EmployeeCreateView.as_view(),name="createEmployee"),
    path('updateEmployee/<int:pk>',views.EmployeeUpdateView.as_view(),name="updateEmployee"),
    path('deleteEmployee/<int:pk>',views.EmployeeDeleteView.as_view(),name="deleteEmployee"),
    path('informe_pdf',InformeEmpleadosPDF.as_view(), name="informe_pdf"),
    path('api/employees', Employees_APIView.as_view()), 
    path('api/employees/<int:pk>/', Employees_APIView_Detail.as_view()),
    path('api/token/',TestView.as_view())
]