from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

# Create your views here.
def landing(request):
    return render(request, 'login/login.html')
def process(request, methods="POST"):
    errors = User.objects.user_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)#this creates the key value pairs for error messages
        return redirect('landing')

    if len(errors) == 0 and request.POST['type'] == 'register':
        fName = request.POST['first_name']
        lName = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        birthday = request.POST['birthday']

        User.objects.createUser(fName,lName,email,password,birthday)
        this_user = User.objects.get(email = email)
        request.session['user_id'] = this_user.id
        request.session.modified = True

        return redirect(reverse('quotes'))

    if len(errors) == 0 and request.POST['type'] == 'login':
        this_user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = this_user.id
        request.session.modified = True
        return redirect(reverse('quotes'))