from django.contrib import admin

from shop.models import ServiceCategory, Shop, ShopInterior, ShopExterior, ShopPackagePromotion, ShopPromotion, ShopVisit, ShopWork, ShopService, ShopStaff, ShopPackage, \
    ServiceSpecialist, ShopAvailability

# Register your models here.
admin.site.register(Shop)
admin.site.register(ShopInterior)
admin.site.register(ShopExterior)
admin.site.register(ShopWork)
admin.site.register(ShopService)
admin.site.register(ShopStaff)
admin.site.register(ServiceSpecialist)
admin.site.register(ShopPackage)

admin.site.register(ShopPromotion)
admin.site.register(ShopVisit)
admin.site.register(ShopPackagePromotion)
admin.site.register(ServiceCategory)
admin.site.register(ShopAvailability)
