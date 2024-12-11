from django.shortcuts import render
from django.urls import path

from shop.api.promos_view import add_promotion, archive_promotion, delete_promotion, edit_promotion, get_all_archived_promotions_view, get_all_promotions_view, get_promotion_details_view, unarchive_promotion
from shop.api.shop_promos_view import add_shop_promotion, get_all_shop_promotions_view
from shop.api.views import add_shop_location_address_view, add_shop_view, edit_package_view, edit_staff_view, get_location_name, get_service_categories_view, list_all_nearby_shops_view, remove_shop_exterior_view, remove_shop_interior_view, remove_shop_work_view, remove_staff_photo_view, set_or_update_shop_availability, setup_shop_view, setup_services_view, setup_staff_view, list_all_shops_view, \
    shop_details_view, add_package_view, setup_payment_view, get_staffs_view, remove_staff_view, admin_add_shop_view, \
    check_shop_email_exists, setup_shop_exterior_view, setup_shop_interior_view, setup_shop_work_view, \
    get_services_view, remove_service_view, get_package_view, shop_visit_count_view, staff_details_view, package_details_view, \
    remove_package_view, setup_services_staff_view, set_shop_availability, list_shop_availability, edit_shop_view, \
    check_registration_complete

app_name = 'shop'

urlpatterns = [
    path('check-shop-email-exists/', check_shop_email_exists, name="check_shop_email_exists"),
    path('check-registration-complete/', check_registration_complete, name="check_registration_complete"),
    path('admin-add-shop/', admin_add_shop_view, name="admin_add_shop_view"),

    path('add-shop/', add_shop_view, name="add_shop_view"),
    path('edit-shop/', edit_shop_view, name="edit_shop_view"),

    path('setup-shop/', setup_shop_view, name="setup_shop_view"),
    path('add-shop-location-address/', add_shop_location_address_view, name="add_shop_location_address_view"),
    path('get-location-name/', get_location_name, name="get_location_name"),
    path('setup-shop-exterior/', setup_shop_exterior_view, name="setup_shop_exterior_view"),
    path('remove-shop-exterior/', remove_shop_exterior_view, name="remove_shop_exterior_view"),
    path('setup-shop-interior/', setup_shop_interior_view, name="setup_shop_interior_view"),
    path('remove-shop-interior/', remove_shop_interior_view, name="remove_shop_interior_view"),
    path('setup-shop-work/', setup_shop_work_view, name="setup_shop_work_view"),
    path('remove-shop-work/', remove_shop_work_view, name="remove_shop_work_view"),

    path('setup-services/', setup_services_view, name="setup_services_view"),
    path('setup-services-staff/', setup_services_staff_view, name="setup_services_staff_view"),

    path('setup-payment/', setup_payment_view, name="setup_payment_view"),
    path('add-package/', add_package_view, name="add_package_view"),
    path('update-package/', edit_package_view, name="edit_package_view"),

    path('setup-staffs/', setup_staff_view, name="setup_staff_view"),
    path('edit-staff/', edit_staff_view, name="edit_staff_view"),
    path('remove-staff-photo/', remove_staff_photo_view, name="remove_staff_photo_view"),

    path('remove-staff/', remove_staff_view, name="remove_staff_view"),
    path('list-shops/', list_all_shops_view, name="list_all_shops_view"),
    path('list-nearby-shops/', list_all_nearby_shops_view, name="list_all_nearby_shops_view"),
    path('shop-details/', shop_details_view, name="shop_details_view"),

    path('get-staffs/', get_staffs_view, name="get_staffs_view"),
    path('get-staff-details/', staff_details_view, name="staff_details_view"),

    path('get-service-categories/', get_service_categories_view, name="get_service_categories_view"),
    path('get-services/', get_services_view, name="get_services_view"),

    path('get-packages/', get_package_view, name="get_package_view"),
    path('get-package-details/', package_details_view, name="package_details_view"),
    path('remove-package/', remove_package_view, name="remove_package_view"),

    path('remove-service/', remove_service_view, name="remove_service_view"),

    path('set-shop-availability/', set_or_update_shop_availability, name="set_or_update_shop_availability"),
    #path('set-shop-availability/', set_shop_availability, name="set_shop_availability"),
    path('list-shop-availability/', list_shop_availability, name="list_shop_availability"),





        path('add-package-promotion/', add_promotion, name="add_promotion"),
    path('edit-promotion/', edit_promotion, name="edit_promotion"),
    path('get-all-package-promotions/', get_all_promotions_view, name="get_all_promotions_view"),
    path('get-promotion-details/', get_promotion_details_view, name="get_promotion_details_view"),
    path('archive-promotion/', archive_promotion, name="archive_promotion"),
    path('delete-promotion/', delete_promotion, name="delete_promotion"),
    path('unarchive-promotion/', unarchive_promotion, name="unarchive_promotion"),
    path('get-all-archived-promotions/', get_all_archived_promotions_view, name="get_all_archived_promotions_view"),
   
        path('add-shop-promotion/', add_shop_promotion, name="add_shop_promotion"),

       path('get-all-shop-promotions/', get_all_shop_promotions_view, name="get_all_shop_promotions_view"),

   
   
    path('get-shop-visit-count/', shop_visit_count_view, name="shop_visit_count_view"),

]