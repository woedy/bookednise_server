import os
import random

from django.db import models
from django.db.models.signals import pre_save

from bookednise_pro import settings
from bookednise_pro.utils import unique_pack_promotion_id_generator, unique_promotion_id_generator, unique_shop_id_generator, unique_service_id_generator, unique_staff_id_generator
from django.core.validators import MinValueValidator, MaxValueValidator


User = settings.AUTH_USER_MODEL

def get_file_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_shop_logo_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_logo/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_shop_interior_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_interior/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )




def upload_shop_exterior_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_exterior/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



def upload_shop_work_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_work/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )




def upload_shop_work_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "shop_work/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_staff_photo_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "staffs/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def upload_package_photo_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "package/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )




def upload_service_category_photo_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_file_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "service_categories/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )



BUSINESS_TYPE_CHOICES = (
    ('Private', 'Private'),
    ('Public', 'Public'),

)
class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_user')
    shop_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    shop_name = models.CharField(max_length=255, blank=True, unique=True, null=True)

    business_type = models.CharField(max_length=255, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    cvr = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField( null=True, blank=True)




    business_days = models.CharField(max_length=255, null=True, blank=True)
    business_hours_open = models.CharField(max_length=255, null=True, blank=True)
    business_hours_close = models.CharField(max_length=255, null=True, blank=True)

    special_features = models.CharField(max_length=255, null=True, blank=True)

    rating = models.DecimalField(default=0.0, decimal_places=2, max_digits=2, null=True, blank=True)


    photo = models.ImageField(upload_to=upload_shop_logo_path, null=True, blank=True)

    verify_code = models.CharField(max_length=10, blank=True, null=True)

    open = models.BooleanField(default=True)

    shop_registered = models.BooleanField(default=False)
    shop_setup = models.BooleanField(default=False)
    service_setup = models.BooleanField(default=False)
    payment_setup = models.BooleanField(default=False)
    staff_setup = models.BooleanField(default=False)
    registration_complete = models.BooleanField(default=False)



    street_address1 = models.CharField(max_length=255, null=True, blank=True)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=255, null=True, blank=True)

    location_name = models.CharField(max_length=200, null=True, blank=True)
    digital_address = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)
    lng = models.DecimalField(default=0.0, max_digits=30, decimal_places=15, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def pre_save_shop_id_receiver(sender, instance, *args, **kwargs):
    if not instance.shop_id:
        instance.shop_id = unique_shop_id_generator(instance)

pre_save.connect(pre_save_shop_id_receiver, sender=Shop)



class ShopInterior(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_interior')
    photo = models.ImageField(upload_to=upload_shop_interior_path, null=True, blank=True)



class ShopExterior(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_exterior')
    photo = models.ImageField(upload_to=upload_shop_exterior_path, null=True, blank=True)


class ShopWork(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_work')
    photo = models.ImageField(upload_to=upload_shop_work_path, null=True, blank=True)



def get_default_staff_image():
    return "defaults/default_staff_image.jpg"






class ShopStaff(models.Model):
    staff_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_users')

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_staffs')
    staff_name = models.CharField(max_length=200,  null=True, blank=True)
    role = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_staff_photo_path, null=True, blank=True,  default=get_default_staff_image)
    rating = models.IntegerField(default=0, null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_staff_id_receiver(sender, instance, *args, **kwargs):
    if not instance.staff_id:
        instance.staff_id = unique_staff_id_generator(instance)

pre_save.connect(pre_save_staff_id_receiver, sender=ShopStaff)




class ServiceCategory(models.Model):
    name = models.CharField(max_length=5000, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to=upload_service_category_photo_path, null=True, blank=True)

    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



SERVICE_CHOICES = (
    ('Haircut', 'Haircut'),
    ('Nail Tech', 'Nail Tech'),
    ('Massage', 'Massage'),
    ('Hairstyle', 'Hairstyle'),

)
class ShopService(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop_services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name='service_categories')
    service_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    service_type = models.CharField(max_length=500, null=True, blank=True)
    #price = models.CharField(max_length=255, null=True, blank=True)
    #duration = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField( null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def pre_save_service_id_receiver(sender, instance, *args, **kwargs):
    if not instance.service_id:
        instance.service_id = unique_service_id_generator(instance)

pre_save.connect(pre_save_service_id_receiver, sender=ShopService)




class ServiceSpecialist(models.Model):
    service = models.ForeignKey(ShopService, on_delete=models.CASCADE, related_name='service_specialist')
    specialist = models.ForeignKey(ShopStaff, on_delete=models.CASCADE, related_name='staff_specialist')




def get_default_package_image():
    return "defaults/default_package_image.jpg"


class ShopPackage(models.Model):
    service = models.ForeignKey(ShopService, on_delete=models.CASCADE, related_name='package_service')
    package_name = models.CharField(max_length=200,  null=True, blank=True)
    photo = models.ImageField(upload_to=upload_package_photo_path, null=True, blank=True, default=get_default_package_image)
    price = models.CharField(max_length=255, null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)






#####################################################




SLOT_STATE_CHOICES = (
    ("Vacant", "Vacant"),
    ("Partial", "Partial"),
    ("Occupied", "Occupied")
)

# class ShopAvailability(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_slots")

#     date = models.DateField(null=True, blank=True)
#     state = models.CharField(default="Vacant", choices=SLOT_STATE_CHOICES, max_length=255)

#     open = models.TimeField(null=True, blank=True)
#     closed = models.TimeField(null=True, blank=True)

#     active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)





class ShopAvailability(models.Model):
    DAYS_OF_THE_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    shop = models.ForeignKey(Shop, related_name='shop_slots', on_delete=models.CASCADE)
    day = models.CharField(max_length=9, choices=DAYS_OF_THE_WEEK)
    open_time = models.TimeField(null=True, blank=True) # Store opening time
    closed_time = models.TimeField(null=True, blank=True) # Store closing time


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.day} - {self.shop.shop_id}"

    class Meta:
        unique_together = ('shop', 'day')  # Ensu




SLOT_STATE_CHOICES = (
    ("Gold", "Gold"),
    ("Silver", "Silver"),
    ("Bronze", "Bronze")
)


class ShopPromotion(models.Model):
    promotion_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_promos")
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    level = models.CharField(default="Gold", choices=SLOT_STATE_CHOICES, max_length=255)


    
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-start_date']


def pre_save_promotion_id_receiver(sender, instance, *args, **kwargs):
    if not instance.promotion_id:
        instance.promotion_id = unique_promotion_id_generator(instance)

pre_save.connect(pre_save_promotion_id_receiver, sender=ShopPromotion)




class ShopVisit(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop_visits")
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='visit_client')

    
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    



class ShopPackagePromotion(models.Model):
    pack_promotion_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="pack_promos")
    package = models.ForeignKey(ShopPackage, on_delete=models.CASCADE, related_name="promo_package")
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    coupon_code = models.CharField(max_length=20, unique=True, blank=True, null=True)


    
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['-start_date']


def pre_save_pack_promotion_id_receiver(sender, instance, *args, **kwargs):
    if not instance.pack_promotion_id:
        instance.pack_promotion_id = unique_pack_promotion_id_generator(instance)

pre_save.connect(pre_save_pack_promotion_id_receiver, sender=ShopPackagePromotion)


