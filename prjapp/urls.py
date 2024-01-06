from os import name
from django.urls import path

from . import views




urlpatterns = [
    path('' , views.register_user , name= 'register'),
    path('login/' , views.login_user , name= 'login'),
    path('logout/' , views.logout_user , name= 'logout'),
 

    ###############Path For Page in Store Temps
    path('maintenance/' , views.maintenance , name= 'maintenance'),
    path('store/' , views.store , name='store'),
    path('cart/' , views.cart , name='cart'),
    path('checkout/' , views.Checkout , name='checkout'),
    path('verifyemail/' , views.verify_email , name= 'verifyemail'),
    
    path('about_you/', views.about_you , name= 'about_you'),
    path('coustomer_page/', views.account , name= 'coustomer_page'),
    path('contact_us/', views.contact_us , name= 'contact_us'),

    ###############Path For Process in Store Temps
    path('process_verify/' , views.process_verify , name= 'process_verify'),
    path('process_contact/' , views.process_contact , name= 'process_contact'),
    path('updateitem/' , views.updateItem , name='updateitem'),
    path('process_order/' , views.processOrder , name='process_order'),
    path('preferance/', views.preferance , name= 'preferance'),
    path('update_location/', views.update_location , name= 'update_location'),
     # path('page_not_found/' , views.page_not_found , name= 'page_not_found'), This Used in Main URLS.py


    ###############Path For Page in Search Temps
    path('search/' , views.Search , name='search'),
    path('Recent-Upload/' , views.upload_search , name='upload_search'),
    path('XBOX/' , views.XBOX , name='XBOX'),
    path('Walmart/' , views.Walmart , name='Walmart'),
    path('Amazon/' , views.Amazon , name='Amazon'),
    path('Razer_Gold/' , views.Razer_Gold , name='Razer_Gold'),
    path('Uber/' , views.Uber , name='Uber'),
    path('Master_Card/' , views.Master_Card , name='Master_Card'),
    path('Itunes/' , views.Itunes , name='Itunes'),
    path('FreeFire/' , views.FreeFire , name='FreeFire'),
    path('Pubg/' , views.Pubg , name='Pubg'),



    ###############Path For Page in Admin Temps
    path('admin_page/', views.admin_page , name= 'admin_page'),
    path('storeadmin/', views.admin , name= 'storeadmin'),

    path('customer_controls/', views.customer_controls , name= 'customer_controls'),
    path('complete_orders/', views.complete_orders , name= 'complete_orders'),

    path('set_ads/', views.set_ads , name= 'set_ads'),
    path('set_discount/', views.set_discount , name= 'set_discount'),
    path('set_quantity/', views.set_quantity , name= 'set_quantity'),
    path('set_revenue/', views.set_revenue , name= 'set_revenue'),
    path('get_coupon/', views.get_coupon , name= 'get_coupon'),
    path('add_product/', views.add_product , name= 'add_product'),
    path('delete_product/', views.delete_product , name= 'delete_product'),
    path('show_prd_orderd/<str:order_id>', views.show_prd_orderd , name= 'show_prd_orderd'),
    path('show_prd/<str:prd_id>', views.show_prd , name= 'show_prd'),
    # path('earnings_report/', views.earnings_report , name= 'earnings_report'),

    path('email_inbox/' , views.email_inbox , name= 'email_inbox'),
    path('read_email/<str:email_id>' , views.read_email , name= 'read_email'),

    ###############Path For Process in Admin Temps
    
    path('process_ads/', views.process_ads , name= 'process_ads'),
    path('edit_price/', views.edit_price , name= 'edit_price'),
    path('edit_quantity/', views.edit_quantity , name= 'edit_quantity'),
    path('edit_revenue/', views.edit_revenue , name= 'edit_revenue'),
    path('confirm_coupon/', views.confirm_coupon , name= 'confirm_coupon'),
    path('process_coupon/', views.process_coupon , name= 'process_coupon'),
    
    path('delevered/<str:order_id>', views.delevered , name= 'delevered'),
    path('rejected/<str:order_id>', views.rejected , name= 'rejected'),
    path('delete_order/<str:order_id>', views.delete_order , name= 'delete_order'), 
    path('delete_message/<str:message_id>', views.delete_message , name= 'delete_message'), 

    path('delete_user/<str:customer_id>', views.delete_user , name= 'delete_user'),
    path('suspended/<str:customer_id>', views.suspended , name= 'suspended'),
    path('notsuspended/<str:customer_id>', views.notsuspended , name= 'notsuspended'),
    
    
    ######################Path Not Used Yet
    path('customer/', views.customer , name= 'customer'),
    path('update_location/', views.update_location , name= 'update_location'),
    path('update_prd/<str:prd_id>/', views.update_prd , name= 'update_prd'),
    path('test/', views.process_test , name= 'test'),
    
   
    
    
    
    ##############Path For API ##########################
    path('getads/', views.getads , name= 'getads'),
    path('getordersrows/' , views.getordersrows , name='getordersrows'),
    path('getproduct/' , views.getproducts , name='getproducts'),
    path('getcustomer/' , views.getcustomer , name='getcustomer'),
    path('getcoupons/' , views.getcoupons , name='getcoupons')
    
    ]

