from django.urls import path

from .views import get_main_page, car_detail, add_car, edit_car, edit_car_formset,catalog_page,shop_list

urlpatterns = [
    path('',get_main_page,name="main"),
    path('car_detail/<int:id>/',car_detail,name='car_detail'),
    path('add_car/',add_car,name='add_car'),
    path('edit_car/<int:id>/',edit_car,name='johan'),
    path('edit_car_formset/<int:id>/',edit_car_formset,name='test'),
    path('catalog_page/',catalog_page,name='catalog_page'),
    path('shop_list/',shop_list,name='shop_list'),
]