from .forms import UsersForm,LoginForm,OwnersForm,UserUpdateForm
from django.core.exceptions import ValidationError
from .models import Users
#Django Libs
from decimal import Decimal
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.contrib.auth import authenticate,login, logout
from django.views.generic.edit import FormView,CreateView,UpdateView
from django.urls import reverse_lazy

# Create your views here.
def mainPage(request):
    print(request.META.get('HTTP_USER_AGENT', '')) #Debug, Comprobar si navegacion es correcta.
    return render(request,"index.html")

class Registro(CreateView):
    template_name = "register.html"
    form_class = UsersForm
    model = Users
    success_url = reverse_lazy("Login")

class updateUser(UpdateView):
    template_name = "contents/editUser.html"
    form_class = UserUpdateForm
    model = Users
    success_url = reverse_lazy("Landing")

def loginView(request):
    form = LoginForm()
    data = {'form':form}
    return render(request,"login.html",data)

def auth(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        authentication = authenticate(request,username=email,password=password)
        if (authentication != None):
            login(request,authentication)
            if authentication.usertype.id == 99:
                messages.warning(request, f"Usuario desabilitado. Contacte al administrador.")
                return redirect("Login")
            return redirect("Landing") #Redirect to userLand
        
        else:
            print(form.non_field_errors)
            errors = form.errors
            print(errors)
            return loginView(request)

    return redirect("Main")

def deauth(request):
    logout(request)
    messages.success(request, f"Sesión cerrada correctamente.")
    return redirect("Main")

def updateLocation(request):
    try:
        data = json.loads(request.body)

        latitude = Decimal(data.get('latitude'))
        longitude = Decimal(data.get('longitude'))

        user = request.user
        print(user.userlocation)
        user.userlocation = Point(longitude,latitude,srid=4326)
        user.save()
        print(user.userlocation)

        return JsonResponse({
            'status':'Exitoso',
            'message':'Ubicación Guardada con exito'
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message':'Json Invalido'
    })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
