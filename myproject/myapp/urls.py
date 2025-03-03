from django.urls import path
from . import views 

urlpatterns =[
    path("",views.home,name='home'),
    # path("registration/",views.registration,name="registration"),
    # path("login/",views.login,name="login"),
    path("cars/",views.cars,name="cars"),
    path("cardescription/",views.car_description,name="car_description"),
    path("book_appointment/",views.book_appointment,name="book_appoinment"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view, name="logout")
]
