from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    dealerId = models.IntegerField()

    TOYOTA = "Toyota"
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    VAN = "Van"
    PICKUP = "Pickup"
    TRUCK = "Truck"
    BIKE = "Bike"
    SCOOTER = "Scooter"
    OTHER = "Other"
    CAR_TYPE_CHOICES = [(TOYOTA, "Toyota"),
                   (SEDAN, "Sedan"), 
                   (SUV, "SUV"), 
                   (WAGON, "Wagon"),  
                   (VAN, "Van"), 
                   (PICKUP, "Pickup"),
                   (TRUCK, "Truck"), 
                   (BIKE, "Motor bike"), 
                   (SCOOTER, "Scooter"), (OTHER, 'Other')]
    carType = models.CharField(max_length=10, 
                               choices=CAR_TYPE_CHOICES, default=TOYOTA)
    year = models.DateField(null=True)

    def __str__(self):
        return f"{self.name}, manfucture in {self.year} and model {self.carType}"
    

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        self.address = address      # Dealer address
        self.city = city            # Dealer city
        self.full_name = full_name  # Full name of dealership
        self.id = id                # Dealership id
        self.lat = lat              # Dealer lat
        self.long = long            # Dealer long
        self.short_name = short_name# Dealer short name
        self.st = st                # State alpha code
        self.state = state          # Full state name
        self.zip = zip              # Dealer zip
        
    def __str__(self):
        return f"Car dealer name: {self.full_name}"

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, id, name, purchase, review, car_make=None, car_model=None, car_year=None, purchase_date=None, sentiment="neutral"):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id  # The id of the review
        self.name = name  # Name of the reviewer
        self.purchase = purchase  # Did the reviewer purchase the car? bool
        self.purchase_date = purchase_date
        self.review = review  # The actual review text
        self.sentiment = sentiment  # Watson NLU sentiment analysis of review

    def __str__(self):
        return f"Reviewer: {self.name}"