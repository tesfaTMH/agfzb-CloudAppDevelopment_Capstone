from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1 # for 1 extra form to display

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "make",
        "dealerId",
        "carType"
    ]
    search_fields = ["name"]
    
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)