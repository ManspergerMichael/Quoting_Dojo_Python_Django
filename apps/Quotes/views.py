from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from .models import Quotes
from ..login.models import User
from django.contrib import messages

# Create your views here.
def quotes(request):
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'this_user' : this_user,
        'user_faves' : this_user.faveorites.all(),
        'quotes' : Quotes.objects.exclude(faveorited_by = this_user)
    }
    #get all quotes exclude faveorites by user
    #get quotes faveorited by user
    return render(request, 'Quotes/quotes.html', context)
def add(request, methods="POST"):
    errors = Quotes.objects.quote_Validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)#this creates the key value pairs for error messages
        return redirect('quotes')
    else:
        # get user who added quote
        this_user = User.objects.get(id = request.session['user_id'])
        #create quote object with user
        Quotes.objects.create(quoted_by = request.POST['quoted_by'], quote = request.POST['quote'], added_by = this_user)
        return redirect(reverse('quotes'))

def faveorite(request, id):
    #add user object,in session to faveorited_by of quote, id passed by form.
    this_quote = Quotes.objects.get(id = id)
    this_user = User.objects.get(id = request.session['user_id'])
    this_quote.faveorited_by.add(this_user)
    this_quote.save()
    return redirect(reverse('quotes'))

def remove(request, id):
    #get qote object id, passed, remove from faveorited_by table
    this_user = User.objects.get(id = request.session['user_id'])
    this_quote = Quotes.objects.get(id = id)
    this_quote.faveorited_by.remove(this_user)
    this_quote.save()
    return redirect(reverse('quotes'))

def user(request, id ):
    this_user = User.objects.get(id = id)
    context = {
        'user' : this_user,
        'quotes' : Quotes.objects.filter(added_by = this_user),
        'count' : Quotes.objects.filter(added_by = this_user).count()
    }
    return render(request, 'Quotes/users.html', context)

def logout(request):
    request.session['user_id'] = 0
    request.session.modified = True
    return redirect(reverse('landing'))