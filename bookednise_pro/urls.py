"""
URL configuration for bookednise_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/accounts/', include('accounts.api.urls', 'accounts_api')),
    path('api/shop/', include('shop.api.urls', 'shop_api')),
    path('api/user-profile/', include('user_profile.api.urls', 'user_profile_api')),
    path('api/homepage/', include('homepage.api.urls', 'homepage_api')),
    path('api/bookings/', include('bookings.api.urls', 'bookings_api')),
    path('api/admin-app/', include('admin_app.api.urls', 'admin_app_api')),
    path('api/slots/', include('slots.api.urls', 'slots_api')),
    path('api/bank_account/', include('bank_account.api.urls', 'bank_account_api')),
    path('api/payments/', include('payments.api.urls', 'payments_api')),
    path("chat/", include("chats.urls")),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

