# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from models import Bottle, Cocktail, Cocktailinfo
from webgui.form import *
from django.forms.formsets import formset_factory, BaseFormSet
from django.core.context_processors import csrf
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import randint


def homepage(request):
    """
    Homepage of the Bar Pi app. Show all availlable coktail
    :param request: metadata about the request
    :return: Homepage
    """
    cocktails = Cocktail.objects.all()
    return render(request, 'homepage.html', {'coktails': cocktails})


def create_cocktail(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False

    BottleItemFormSet = formset_factory(BottleItemForm, max_num=10, formset=RequiredFormSet)

    if request.method == 'POST':  # If the form has been submitted...
        bottle_list_form = CoktailForm(request.POST)  # A form bound to the POST data
        # Create a formset from the submitted data
        cocktail_item_formset = BottleItemFormSet(request.POST, request.FILES)

        if bottle_list_form.is_valid() and cocktail_item_formset.is_valid():
            # create the cocktail
            cocktail = Cocktail()
            cocktail.lock = False
            cocktail.name = bottle_list_form.cleaned_data['name']
            cocktail.save()

            for form in cocktail_item_formset.forms:
                volume = form.cleaned_data['volume']
                bottle = Bottle.objects.get(id=form.cleaned_data['bottle'].id)
                info_cocktail = Cocktailinfo(bottle=bottle, cocktail=cocktail, volume=volume)
                info_cocktail.save()
            messages.add_message(request, messages.SUCCESS, "Cocktail créé avec succès")
            return redirect('webgui.views.homepage')
    else:
        bottle_list_form = CoktailForm()
        cocktail_item_formset = BottleItemFormSet()

    c = {'bottle_list_form': bottle_list_form,
         'cocktail_item_formset': cocktail_item_formset,
        }
    c.update(csrf(request))
    return render(request, 'create_cocktail.html', c)


def delete_cocktail(request, id):
    cocktail = Cocktail.objects.get(id=id)
    cocktail.delete()
    messages.add_message(request, messages.SUCCESS, "Cocktail supprimé")
    return redirect('webgui.views.homepage')


def login_page(request):
    if request.POST:
        form = LoginForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password, request=request)
            print "authenticate user :"+str(user)
            if user is not None:
                login(request, user)
                return redirect('webgui.views.admin_homepage')
            else:
                messages.add_message(request, messages.ERROR, "Login ou mot de passe invalide", extra_tags='danger')
                form = LoginForm()  # An unbound form
                return render(request, 'login_form.html', {'form': form})
        else:
            messages.add_message(request, messages.ERROR, "Login ou mot de passe invalide", extra_tags='danger')
            return render(request, 'login_form.html', {'form': form})

    else:
        form = LoginForm()  # An unbound form
        return render(request, 'login_form.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('webgui.views.homepage')


@login_required(login_url='/login/')
def admin_homepage(request):
    bottles = Bottle.objects.all().order_by('slot')
    return render(request, 'admin_homepage.html', {'bottles': bottles})


@login_required(login_url='/login/')
def delete_bottle(request, id):
    bottle = Bottle.objects.get(id=id)
    cocktails = Cocktail.objects.filter(bottles=id)
    if request.POST:
        # remove cocktail
        for cocktail in cocktails:
            cocktail.delete()
        # remove bottle
        bottle = Bottle.objects.get(id=id)
        bottle.delete()
        messages.add_message(request, messages.SUCCESS, "Bouteille supprimée")
        return redirect('webgui.views.admin_homepage')
    else:
        return render(request, 'delete_bottle.html', {'bottle': bottle, 'cocktails': cocktails})


@login_required(login_url='/login/')
def create_bottle(request):
    if request.POST:
        form = BottleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webgui.views.admin_homepage')
    else:
        form = BottleForm()
    return render(request, 'create_bottle.html', {'form': form})


@login_required(login_url='/login/')
def update_bottle(request, id):
    bottle = get_object_or_404(Bottle, id=id)
    form = BottleForm(request.POST or None, instance=bottle)
    if form.is_valid():
        form.save()
        return redirect('webgui.views.admin_homepage')
    return render(request, "update_bottle.html", {'form': form,
                                                  'bottle': bottle})


def run_cocktail(request, id):
    # get cocktail by id
    cocktail = Cocktail.objects.get(id=id)
    # TODO: call rasp lib
    max_time = 1000
    return render(request, "run_cocktail.html", {'max_time': max_time,
                                                 'cocktail': cocktail})

def run_random(request):
    # get all cocktail
    cocktails = Cocktail.objects.all()
    # random
    cocktail = cocktails[randint(0, len(cocktails))]
    # TODO: call rasp lib
    max_time = 1000
    return render(request, "run_cocktail.html", {'max_time': max_time,
                                                 'cocktail': cocktail})


