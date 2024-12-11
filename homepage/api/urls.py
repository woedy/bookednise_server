from django.urls import path

from homepage.api.views import client_homepage_new_view, explore_shops_view, shop_homepage_view, client_homepage_view

app_name = 'homepage'

urlpatterns = [
    path('shop-homepage/', shop_homepage_view, name="shop_homepage"),
    path('client-homepage/', client_homepage_view, name="client_homepage_view"),
    path('client-homepage-new/', client_homepage_new_view, name="client_homepage_new_view"),
    path('explore-shops/', explore_shops_view, name="explore_shops_view"),
]
