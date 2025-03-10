from django.urls import path
from . import views 

urlpatterns =[
    path("",views.home,name='home'),
    # path("registration/",views.registration,name="registration"),
    # path("login/",views.login,name="login"),
    path("cars/",views.cars,name="cars"),
    path("cardescription/<str:pk>",views.car_description,name="car_description"),
    path("book_appointment/<str:pk>",views.book_appointment,name="book_appointment"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("user_dashboard/",views.user_dashboard, name="user_dashboard"),
    path("logout/",views.logout_view, name="logout"),
    path("user_appointments",views.user_appointments,name="user_appointments"),
]
