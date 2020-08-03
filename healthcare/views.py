from django.shortcuts import render , redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.core.exceptions import ObjectDoesNotExist



from .models import *
from .forms import *

# Create your views here.

def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request,'Account was created for ' + username)

            return redirect('login')

    context= {'form': form}
    return render(request, 'healthcare/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username,password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Username or Password is incorrect')

    content= {}
    return render(request, 'healthcare/login.html', content)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        current_user = request.user

        try:
            patient = Patient.objects.get(user = current_user)
        except ObjectDoesNotExist:
            messages.info(request, 'Sign in as Patient')
            return redirect('logout')

        context = {'user': current_user, 'patient': patient}
    else:
        context= {}
    return render(request, 'healthcare/home.html', context )




def editPateint(request,pk):
    patient = Patient.objects.get(id = pk)
    form = PatientForm(instance = patient)
    context = {'form': form, 'patient': patient}

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'healthcare/patientForm.html', context)


def testLocation(request):
   testLocations = TestLocation.objects.all()

   if request.user.is_authenticated:
       current_user = request.user
       patient = Patient.objects.get(user=current_user)
       context = {'testLocations': testLocations, 'patient': patient}
   else:
        context = {'testLocations': testLocations}


   return render(request, 'healthcare/testLocationForm.html', context)




