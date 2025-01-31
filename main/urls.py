from django.urls import path

from .views import get_main_page, car_detail

urlpatterns = [
    path('',get_main_page),
    path('car_detail/<int:id>',car_detail,name='car_detail'),
]