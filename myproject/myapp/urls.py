#urls.py:
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
    path("user_dashboard/<str:pk>",views.user_dashboard, name="user_dashboard"),
    path("logout/",views.logout_view, name="logout"),
    path("user_appointments",views.user_appointments,name="user_appointments"),
    path("delete_appointment/<str:pk>",views.delete_appointment,name="delete_appointment"),
    path('admin/chat/', views.admin_chat, name='admin_chat'),
    path('cancel_appointment/<str:pk>', views.cancel_appointment, name='cancel_appointment'),
]


from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
