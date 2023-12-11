from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .forms import UserRegisterForm
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_review
from .models import CarMake, CarModel, CarDealer

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contactus.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:dealer_details')
        else:
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!!. You are able to login.')
            return redirect('djangoapp:login')
        else:
            form = UserRegisterForm()
    return render(request, 'djangoapp/registration.html',{'form':form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = " ".join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context = {"dealership_list": dealerships}
        #context = dict()
        #context["dealership_list"] = dealerships
        print(context)
        return render(request, "djangoapp/dealership-list.html", context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "http://127.0.0.1:5000/api/get_reviews"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        # Concat all review's
        #dealer_reviews = " ".join([dealer.review for dealer in reviews])
        # Return a list of dealer short name
        context = {"reviews": reviews}
        #print(reviews[0].review)
        return render(
            request, 
            "djangoapp/dealer_details.html", context
            #{"reviews": reviews, "dealer_id": dealer_id},
        )


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        cars = CarModel.objects.filter(dealerId=dealer_id)
        context = {
            "cars": cars,
            "dealer_id": dealer_id,
        }
        return render(request, "djangoapp/add_review.html", context)
    if request.method == "POST":
        url = "http://127.0.0.1:5000/api/post_review"
        review = {}
        input_data = request.POST
        review["dealership"] = int(dealer_id)
        review["review"] = input_data["content"]
        review["purchase"] = input_data.get("purchasecheck", False)
        review["purchase_date"] = input_data["purchasedate"]
        car = CarModel.objects.get(pk=input_data["car"])
        if car:
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
        else:
            review["car_make"] = "None"
            review["car_model"] = "None"
            review["car_year"] = "None"
        review["name"] = "name"
        review["id"] = 1
        json_payload = {"review": review}
        post_review(url, json_payload)
        print(review["name"])
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)