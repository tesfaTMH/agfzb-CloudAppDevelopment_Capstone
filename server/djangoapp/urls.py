from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
# using builtin LoginView for login and logout
from django.contrib.auth import views as auth_views
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    # path for about view
    path('about/', view=views.about, name='about'),
    
    # path for contact us view
    path('contact/', view=views.contact, name='contact-us'),
    # path for registration
    path('registration/', view=views.registration_request, name='register'),

    # path for login
    path('login/', auth_views.LoginView.as_view(template_name='djangoapp/login.html'), name='login'),
    #path('login/', views.login_request, name='login'),

    # path for logout
    path('logout/',auth_views.LogoutView.as_view(template_name='djangoapp/logout.html'), name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)