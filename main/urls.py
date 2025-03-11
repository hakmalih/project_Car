from django.urls import path

from .views import get_main_page, car_detail, add_car, edit_car, edit_car_formset, catalog_page, shop_list, \
    get_registration_page, enter_account, account_page, get_login_page, user_logout, get_profile_page

urlpatterns = [
    path('',get_main_page,name="main"),
    path('car_detail/<int:id>/',car_detail,name='car_detail'),
    path('add_car/',add_car,name='add_car'),
    path('edit_car/<int:id>/',edit_car,name='johan'),
    path('edit_car_formset/<int:id>/',edit_car_formset,name='test'),
    path('catalog_page/',catalog_page,name='catalog_page'),
    path('shop_list/',shop_list,name='shop_list'),
    path('registration/',get_registration_page,name='registration'),
    path('enter_account/',enter_account,name='enter_account'),
    path('account_page/',account_page,name='account_page'),
    path('login/',get_login_page,name='login'),
    path('logout/',user_logout,name='logout'),
    path('profile/',get_profile_page,name='profile'),
]