from ast import List
from os import name
from tkinter.tix import Tree
from django.http import JsonResponse
from django.shortcuts import render,redirect , HttpResponse
from django.contrib.auth.models import Group,User,auth
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import *
import json
import datetime
import random
import requests
from . util import cartData , guestOrder,update_user_order,create_customer_prd,is_admin,append_order_into_text_file,get_orders_from_text_file,create_map,append_prefer_in_file,get_prefer_from_file,create_map_current_location_only,append_order_category_into_text_file , get_trend_from_file
from .forms import UP_Prd_Form,ADD_Prd_Form,Customer_Form,Brand_Form,Tag_Form
from .association_rules import process_association,process_association_categories
from django.forms import inlineformset_factory
from .decorators import unauth_user,allowed_users,auth_user
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

import folium
import pandas as pd
import numpy as np
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.crypto import get_random_string
from django.http import Http404

###################################




@unauth_user
def register_user(request):
    if request.method=='POST':
        uname = request.POST['username']    
        password = request.POST['password']
        password2 = request.POST['password2']
        try:
            if password == password2:
                my_user = User.objects.create_user(uname , '' , password)
                print(uname , password)
                my_user.save()
                my_group = Group.objects.get(name='customers')
                my_group.user_set.add(my_user)
                
                customer = Customer.objects.create(user = my_user , email = uname , password = password)
                user = authenticate(request , username = uname , password = password)
                login(request , user)
                update_user_order(request)
                
                return redirect ('verifyemail')
            else:
                messages.success(request , (" There Is Error In Your Password..!!"))
                return redirect ('register')
        except:
            messages.success(request , (" This Email is Used..!!"))
            return redirect ('register')
    else:
        return render(request , 'auth/signup.html')
##########################################################create verify

def create_verify(request):

    al = ['a' , 'b' , 'c' ,'d' , 'e' ,'f' , 'g' , 'h', 'i' ,'j' ,'k' , 'l' ,'m' ,'n', 'o' ,'p','q' , 'r','s', 't','u','v', 'w','x', 'y' ,'z']
    AL = ['A' ,'B' ,'C' ,'D' ,'E', 'F', 'G', 'H' , 'I', 'G' , 'K', 'L', 'M', 'N', 'O', 'P','Q', 'R','S', 'T','U','V','W','X','Y','Z']
    num = ['0','1','2','3','4','5','6','7','8','9']
    
    i = 1
    while True:
        ia = random.randint(0,23)
        iA = random.randint(0,23)
        inn = random.randint(0,9)
        iqu = random.randint(0,2)
        alph = al[ia]
        Alph = AL[iA]
        Num = num[inn]
        
        if i > 2:
            paAssq = Alph + alph + Num 
        else:
            psAsq =   Alph + Alph + Num + Num +alph
        if i >= 3:
            break
        else:
            i = i+1
        continue 
    return psAsq + paAssq
###############LOGIN
@unauth_user
def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password  = request.POST['password']
        try:
            customer = Customer.objects.get(email = email )
            user = authenticate(request , username = email , password = password)
            if user is not None:
                if customer.suspand == True:
                    messages.success(request , ("Your Account Has Been Suspended...!!!"))
                    return redirect('login')
                
                login(request , user)
                return redirect('store')
            else:
                messages.success(request , ("Email or Password is Wrong...!!!"))
                
                return redirect('login')
        except:
            messages.success(request , ("This Email Does Not Exist...!!!"))
                
            return redirect('login')
    else:
        return render(request , 'auth/login.html')

###################################################



@auth_user
def logout_user(request):
    logout(request)
    
    return redirect ('login')
###################################################
@auth_user
@csrf_exempt
def verify_email(request):
    co = request.user.customer
    
    customer = Customer.objects.get(email = co )
    code = create_verify(request)
    customer.verify_code = code
    customer.save()
    
    send_mail("test sign up " , code , settings.EMAIL_HOST_USER , [customer] , fail_silently=False)
    context ={'co':co,'code':code}
    return render(request , 'store_temps/verify_email.html' , context)
###################################################
def process_verify(request):
    data = json.loads(request.body)
    verify = data['verify']
    cust = request.user.customer
    
    customer = Customer.objects.get(email = cust )
    
    
    
    v_code = Customer.objects.get(email = customer).verify_code
    if v_code == verify:
       redirect ('store')
        
    else:
        messages.success(request , ("Error in Verify Code , We Send Another one..!!!"))
        redirect ('verifyemail')

    return JsonResponse('item was added',safe=False)


###################################
@auth_user
@allowed_users(allowed_roles=['admins'])
def admin(request):
    
    sort_orders_id = []
    orders=Order.objects.all()
    rejected_orders = Order.objects.filter(complete=True,delevered=False , rejected = True)
    complete_orders_and_not_delevered=Order.objects.filter(complete=True)
    for i in complete_orders_and_not_delevered:
        sort_orders_id.append(i.id)
    
    completed = []
    sort_orders = sorted(sort_orders_id, reverse=True)
    print(sort_orders)
    for i in sort_orders:
        for j in complete_orders_and_not_delevered:
            if i == j.id:
                completed.append(j)
    print(completed)
    delevered_orders=Order.objects.filter(complete=True,delevered=True)
    customer=Customer.objects.all()
    products=Product.objects.all()
    cus_products=CustomerProduct.objects.all()

    total_customers = customer.count()
    total_orders = orders.count()

    for i in complete_orders_and_not_delevered:
        t = Order.objects.get(transaction_id = i.transaction_id)
        t.state = 'Processing'
        t.save()
    for j in delevered_orders:
        d = Order.objects.get(transaction_id = j.transaction_id)
        d.state = 'Complate'
        d.save()
    
    for i in rejected_orders:
        r = Order.objects.get(transaction_id = i.transaction_id)
        r.state = 'Rejected'
        r.save()



    #admin_page
    context={'completed':completed,'rejected_orders': rejected_orders,'delevered_orders':delevered_orders,'complete_orders':complete_orders_and_not_delevered,'total_customers':total_customers ,'cus_prds':cus_products ,'total_orders':total_orders ,'products':products , 'orders':orders , 'customer':customer}
    return render(request,'admintemp/admin.html',context)

###################################
@auth_user
@allowed_users(allowed_roles=['admins'])
def admin_page(request):
    
    sort_orders_id = []
    orders=Order.objects.all()
    rejected_orders = Order.objects.filter(complete=True,delevered=False , rejected = True)
    complete_orders_and_not_delevered=Order.objects.filter(complete=True)
    for i in complete_orders_and_not_delevered:
        sort_orders_id.append(i.id)
    
    completed = []
    sort_orders = sorted(sort_orders_id, reverse=True)
    # print(sort_orders)
    for i in sort_orders:
        for j in complete_orders_and_not_delevered:
            if i == j.id:
                completed.append(j)
    # print(completed)
    delevered_orders=Order.objects.filter(complete=True,delevered=True)
    customer=Customer.objects.all()
    products=Product.objects.all()
    cus_products=CustomerProduct.objects.all()

    total_customers = customer.count()
    total_orders = orders.count()
    order_items = Orderitem.objects.all()
    revenue = 0.0
    for i in orders:
        revenue += i.get_revenue
    
    # print('==================revenue')
    # print(revenue)

    #orr = earnings_report(request)
    # print('==================orr')
    # print(orr)

    # print('==================orr')
    # print(one_day_ago)


    for i in complete_orders_and_not_delevered:
        t = Order.objects.get(transaction_id = i.transaction_id)
        t.state = 'Processing'
        t.save()
    for j in delevered_orders:
        d = Order.objects.get(transaction_id = j.transaction_id)
        d.state = 'Complate'
        d.save()
    
    for i in rejected_orders:
        r = Order.objects.get(transaction_id = i.transaction_id)
        r.state = 'Rejected'
        r.save()



    #admin_page
    context={'revenue':revenue,'completed':completed,'rejected_orders': rejected_orders,'delevered_orders':delevered_orders,'complete_orders':complete_orders_and_not_delevered,'total_customers':total_customers ,'cus_prds':cus_products ,'total_orders':total_orders ,'products':products , 'orders':orders , 'customer':customer}
    return render(request,'admintemp/admin_page.html',context)

#################################################################

# def earnings_report(request):
#     today = datetime.date.today()
#     one_day_ago = today - datetime.timedelta(days=1)
#     # orders = Order.objects.filter(date_orderd=today)
#     # orders = Order.objects.get()

#     # return orders

#####################################################

def email_inbox(request):
    email = InboxEmail.objects.all()
    sort_orders_id = []
    for i in email:
        sort_orders_id.append(i.id)
    
    completed = []
    sort_email = sorted(sort_orders_id, reverse=True)
    print(sort_email)
    for i in sort_email:
        for j in email:
            if i == j.id:
                completed.append(j)
    context = {'completed':completed,'email':email}
    return render(request,'admintemp/email_inbox.html',context)

def read_email(request , email_id):
    this_email = InboxEmail.objects.get(id = email_id)
    context = {'this_email':this_email}
    return render(request,'admintemp/email_read.html',context)

def delete_message(request,message_id):
    this_message=InboxEmail.objects.get(id=message_id)
    
    this_message.delete()
    return HttpResponse("Success!")


#######################################################################
def customer_controls(request):
    customer=Customer.objects.all()
    context = {'customer':customer}
    return render(request,'admintemp/customer_controls.html',context)

#################################################

def complete_orders(request):
    sort_orders_id = []
    orders=Order.objects.all()
    rejected_orders = Order.objects.filter(complete=True,delevered=False , rejected = True)
    complete_orders_and_not_delevered=Order.objects.filter(complete=True)
    for i in complete_orders_and_not_delevered:
        sort_orders_id.append(i.id)
    
    completed = []
    sort_orders = sorted(sort_orders_id, reverse=True)
    # print(sort_orders)
    for i in sort_orders:
        for j in complete_orders_and_not_delevered:
            if i == j.id:
                completed.append(j)
    # print(completed)
    delevered_orders=Order.objects.filter(complete=True,delevered=True)
    customer=Customer.objects.all()
    products=Product.objects.all()
    cus_products=CustomerProduct.objects.all()

    total_customers = customer.count()
    total_orders = orders.count()
    
    for i in complete_orders_and_not_delevered:
        t = Order.objects.get(transaction_id = i.transaction_id)
        t.state = 'Processing'
        t.save()
    for j in delevered_orders:
        d = Order.objects.get(transaction_id = j.transaction_id)
        d.state = 'Complate'
        d.save()
    
    for i in rejected_orders:
        r = Order.objects.get(transaction_id = i.transaction_id)
        r.state = 'Rejected'
        r.save()



    #admin_page
    context={'completed':completed,'rejected_orders': rejected_orders,'delevered_orders':delevered_orders,'complete_orders':complete_orders_and_not_delevered,'total_customers':total_customers ,'cus_prds':cus_products ,'total_orders':total_orders ,'products':products , 'orders':orders , 'customer':customer}
    return render(request,'admintemp/complete_orders.html',context)


#########################################################customer_id
def suspended(request , customer_id):
    this_cust = Customer.objects.get(id = customer_id)
    print(this_cust)
    if this_cust.suspand == False:
        this_cust.suspand = True
        this_cust.save()
   
    
    return HttpResponse("Success!")

#######################################################################
def notsuspended(request , customer_id):
    this_cust = Customer.objects.get(id = customer_id)
    print(this_cust)
    if this_cust.suspand == True:
        this_cust.suspand = False
        this_cust.save()
    
    return HttpResponse("Success!")

#######################################################################
def delete_user(request,customer_id):
    this_cust = Customer.objects.get(id = customer_id)
    cust = User.objects.get(username = this_cust.email)
    print(this_cust)
    cust.delete()
    return HttpResponse("Success!")
#########################################################

def delevered(request,order_id):
    this_order=Order.objects.get(id=order_id)
    print(this_order)
    this_order.delevered=True
    this_order.rejected = False
    this_order.state = 'Complate'
    this_order.save()
    return HttpResponse("Success!")

#######################################################################

def rejected(request, order_id):
    this_order=Order.objects.get(id=order_id)
    print(this_order)
    this_order.delevered = False
    this_order.rejected = True
    this_order.state = 'Rejected'
    this_order.save()
    return HttpResponse("Success!")

#########################################################
def delete_order(request,order_id):
    this_order=Order.objects.get(id=order_id)
    print(this_order)
    this_order.delete()
    return HttpResponse("Success!")
#########################################################
def show_prd(request,prd_id):
    product=Product.objects.get(id=prd_id)
    context={'product':product}
    return render(request,'admintemp/show_prd.html',context)
#########################################################
@auth_user
@allowed_users(allowed_roles=['admins'])
def show_prd_orderd(request,order_id):
    this_order=Order.objects.get(id=order_id)
    orderitem=this_order.orderitem_set.all()


    # location=Location_data.objects.get(customer=this_order.customer)
    # current_loc_data={'name':this_order.customer.name,
    #                   'location':{
    #                     'latitude':location.lat,
    #                     'longitude':location.lon
    #                 }}
    # other_location_details=[]
    # for item in orderitem:
    #     try:
    #         dealer=item.product.customer
    #         dealer_location=Location_data.objects.get(customer=dealer)
    #         loc_det={'name':dealer.name,
    #                  'location':{
    #                     'latitude':dealer_location.lat,
    #                     'longitude':dealer_location.lon
    #                 }}
    #         other_location_details.append(loc_det)
    #     except:
    #         pass
    # m1=create_map_current_location_only(current_loc_data)
    # m2=create_map(current_loc_data,other_location_details)

    
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartitems']
    shop = Shippingadd.objects.filter(
                order = order_id
                
            )
    print(shop)
    #'map2':m2._repr_html_()'map1':m1._repr_html_() ,
    context = {  'items':orderitem , 'shop':shop }


    return render(request,'admintemp/show_ordered_prd.html',context)

#########################################################

def set_ads(request):
    ads = Ads.objects.all()
    if request.method == "POST":
        Ad1 =  request.POST['AdNO1']
        Ad2 = request.POST['AdNO2']
        Ad3 = request.POST['AdNo3']
        Ad4 = request.POST['AdNO4']
        Ad5 = request.POST['AdNO5']
        # if Ad1 is not None:
        #     ad = Ads.objects.get(name = 'AdNO1' )
        #     ad.photo = Ad1
        #     ad.save()
        # if Ad2 is not None:
        #     ad = Ads.objects.get(name = 'AdNO2' )
        #     ad.photo = Ad2
        #     ad.save()
        # if Ad3 is not None:
        #     ad = Ads.objects.get(name = 'AdNO3' )
        #     ad.photo = Ad3
        #     ad.save()
        # if Ad4 is not None:
        #     ad = Ads.objects.get(name = 'AdNO4' )
        #     ad.photo = Ad4
        #     ad.save()
        # if Ad5 is not None:
        #     ad = Ads.objects.get(name = 'AdNO5' )
        #     ad.photo = Ad5
        #     ad.save()
    context = {'ads':ads}
    return render(request,'admintemp/set_ads.html',context)


#################################################

def process_ads(request):
    data = json.loads(request.body)
    photo = data['photo']
    name = data['name']

    ad = Ads.objects.get(name = name)
    
    file_path = photo
    re = 'C:\fakepath\a'

    result = file_path[len(re)+1 :]
    ad.photo = result
    ad.save()


    return JsonResponse('item was added',safe=False)

#########################################################

@auth_user
@allowed_users(allowed_roles=['admins'])
def get_coupon(request):
    try:
        coup = Coupons.objects.last()
        coup_value = coup.value
        coup_coupon = coup.coupon
    except:
        coup_value = ''
        coup_coupon = ''
    context = {'coupo':coup_coupon , 'vcoupo':coup_value}
    return render(request,'admintemp/get_coupon.html',context)

###################################################
@auth_user
@allowed_users(allowed_roles=['admins'])
def process_coupon(request):
    data = json.loads(request.body)
    coupo = data['coupo']
    vcoupo = data['vcoupo']

    coupon = Coupons.objects.create(coupon = coupo , value = vcoupo)

    return JsonResponse('item was added',safe=False)

################################################

def set_revenue(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request,'admintemp/set_revenue.html',context)
##############################################
def edit_revenue(request):
    data = json.loads(request.body)
    prdid = data['prdid']
    prc = data['prc']
    

    customer = request.user.customer
    product = Product.objects.get(id=prdid)
    product.revenue = prc
    product.save()
    # order , created = Order.objects.get_or_create(customer = customer , complete = False)

    # orderitem , created = Orderitem.objects.get_or_create(order = order , product = product)

    # if action =='add':
    #     orderitem.quantity = (orderitem.quantity + 1)
    # elif action == 'remove':
    #     orderitem.quantity = (orderitem.quantity - 1)

    # orderitem.save()

    # if orderitem.quantity <= 0:
    #     orderitem.delete()

    return JsonResponse('item was added',safe=False)

##################################################
@auth_user
@allowed_users(allowed_roles=['admins'])
def set_quantity(request):
    customer = request.user.customer
    prd_form = ADD_Prd_Form(initial = {'customer':customer})
    prd_form_img =inlineformset_factory(Product , Prd_image_store , fields = ('prd_name' , 'prds_img'))
    prd_imgs = prd_form_img()
    products = Product.objects.all()
    if request.method == "POST":
        pr =  request.POST['new_price'] 
        print(pr)  
        # prd_form = ADD_Prd_Form(request.POST , request.FILES)
        # if prd_form.is_valid():
        #     prd_form.save()
        #     prd= Product.objects.order_by('date_upload').last()
        #     prd_imgs = prd_form_img(request.POST , request.FILES , instance=prd)
        #     if prd_imgs.is_valid():
        #         prd_imgs.save()
        #     return redirect('/storeadmin')
        
    context={'products':products,'form':prd_form , 'prd_imgs':prd_imgs}
    return render(request,'admintemp/set_quantity.html',context)

#########################################################
@csrf_exempt
def edit_quantity(request):
    data = json.loads(request.body)
    prdid = data['prdid']
    prc = data['prc']
    

    customer = request.user.customer
    product = Product.objects.get(id=prdid)
    product.quantity = prc
    product.save()
    # order , created = Order.objects.get_or_create(customer = customer , complete = False)

    # orderitem , created = Orderitem.objects.get_or_create(order = order , product = product)

    # if action =='add':
    #     orderitem.quantity = (orderitem.quantity + 1)
    # elif action == 'remove':
    #     orderitem.quantity = (orderitem.quantity - 1)

    # orderitem.save()

    # if orderitem.quantity <= 0:
    #     orderitem.delete()

    return JsonResponse('item was added',safe=False)

#######################################################
@auth_user
@allowed_users(allowed_roles=['admins'])
def set_discount(request):
    customer = request.user.customer
    prd_form = ADD_Prd_Form(initial = {'customer':customer})
    prd_form_img =inlineformset_factory(Product , Prd_image_store , fields = ('prd_name' , 'prds_img'))
    prd_imgs = prd_form_img()
    products = Product.objects.all()
    if request.method == "POST":
        pr =  request.POST['new_price'] 
        print(pr)  
        # prd_form = ADD_Prd_Form(request.POST , request.FILES)
        # if prd_form.is_valid():
        #     prd_form.save()
        #     prd= Product.objects.order_by('date_upload').last()
        #     prd_imgs = prd_form_img(request.POST , request.FILES , instance=prd)
        #     if prd_imgs.is_valid():
        #         prd_imgs.save()
        #     return redirect('/storeadmin')
        
    context={'products':products,'form':prd_form , 'prd_imgs':prd_imgs}
    return render(request,'admintemp/set_discount.html',context)

#########################################################
@csrf_exempt
def edit_price(request):
    data = json.loads(request.body)
    prdid = data['prdid']
    prc = data['prc']
    

    customer = request.user.customer
    product = Product.objects.get(id=prdid)
    product.offer = prc
    product.save()
    # order , created = Order.objects.get_or_create(customer = customer , complete = False)

    # orderitem , created = Orderitem.objects.get_or_create(order = order , product = product)

    # if action =='add':
    #     orderitem.quantity = (orderitem.quantity + 1)
    # elif action == 'remove':
    #     orderitem.quantity = (orderitem.quantity - 1)

    # orderitem.save()

    # if orderitem.quantity <= 0:
    #     orderitem.delete()

    return JsonResponse('item was added',safe=False)
#########################################################
@csrf_exempt
def confirm_coupon(request):
    data = json.loads(request.body)
    coup = data['coupon']
    customer = request.user.customer
    
    coupon = Coupons.objects.get(coupon = coup)
    dataa = cartData(request)   
    items = dataa['items']
    order = dataa['order']
    cartItems = dataa['cartitems']
    co = order.get_cart_total - coupon.value
    # product = Product.objects.get(id=prdid)
    # product.offer = prc
    # product.save()
    
    return JsonResponse('item was added',safe=False)
#########################################################
@auth_user
@allowed_users(allowed_roles=['admins'])
def add_product(request):
    customer= request.user.customer
    if request.method == 'POST':
        prd_name = request.POST['prd_name']
        prd_price = request.POST['prd_price']
        prd_revenue = request.POST['prd_revenue']
        prd_dis = request.POST['prd_dis']
        prd_qua = request.POST['prd_qua']
        prd_cat = request.POST['prd_cat']
        prd_img = request.POST['prd_img']

        Short_desc = "It's take about 7 Hours at least to processed"
        Num_views = 321

        pro = Product.objects.create(customer = customer , name = prd_name, price = prd_price, offer = prd_dis ,revenue = prd_revenue, quantity = prd_qua,
                                     category = prd_cat, short_desc = Short_desc, num_views = Num_views, image= prd_img)
    context={}
    return render(request,'admintemp/add_product.html',context)

#############################################

@auth_user
@allowed_users(allowed_roles=['admins'])
def delete_product(request):
    if request.method == 'POST':
        prd_name = request.POST['prd_name']
        try:
            pro = Product.objects.get(name = prd_name)
            pro.delete()
        except:
            messages.success(request , ("You Enter Wrong Name...!!!"))
    context={}
    return render(request,'admintemp/delete_product.html',context)

#############################################

@auth_user
def update_prd(request, prd_id):
    prd=Product.objects.get(id=prd_id)
    if request.user.customer == prd.customer:
        print(prd)
        form=UP_Prd_Form(instance=prd)
        if request.method == 'POST':
            form=UP_Prd_Form(request.POST,  request.FILES ,instance=prd)
            if form.is_valid():
                form.save()
                return redirect('customer')
    else:
        return redirect('customer')
    context={'form':form}
    return render(request,'admintemp/create_prd.html',context)

#########################################################
@csrf_exempt
def update_location(request):
    customer=request.user.customer
    if request.method == "POST":
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        latitude = data.get("float_value_1")
        longitude = data.get("float_value_2")
        print(latitude,longitude)
        # Do something with the float values
        loc_data , created= Location_data.objects.get_or_create(customer=customer)
        loc_data.lat=latitude
        loc_data.lon=longitude
        loc_data.save()
        return HttpResponse("Success!")
#########################################################
@auth_user
def customer(request):
    customer=request.user.customer
    orders=customer.order_set.all()
    total_orders = orders.count()
    products=Product.objects.filter(customer=customer)
    customer_form = Customer_Form(instance=customer)
    items=[]

    for i in orders :
        order_items=i.orderitem_set.all()
        items.append(order_items)
    
    if request.method == 'POST':  
        if 'customerform' in request.POST:      
            customer_form = Customer_Form(request.POST , request.FILES,instance=customer)
            if customer_form.is_valid():
                customer_form.save()

    brand = Brand_Form()
    if request.method == 'POST':
        if 'addbrand' in request.POST:      
            brand = Brand_Form(request.POST)
            if brand.is_valid():
                brand.save()
                return redirect('/customer')
    
    tag = Tag_Form()
    if request.method == 'POST':  
        if 'addtag' in request.POST:    
            tag = Tag_Form(request.POST)
            if tag.is_valid():
                tag.save()
                return redirect('/customer')
        
    context = {'add_tag':tag,'add_brand':brand,'Customer_Form':customer_form,'products':products ,'customer':customer ,'total_orders':total_orders - 1, 'orders':orders ,'items':items}
    return render(request,'admintemp/customer.html',context)

######################### def product not used yet ################################
def process_test(request):
    m= folium.Map(location=[34.7268,36.7234],zoom_start=25)
    coordinates=(34.7268,36.7234)
    folium.Marker(coordinates).add_to(m)
    context = {'map':m._repr_html_()}
    return render (request,'test2.html',context)

########################################################
@auth_user
def account(request):
    customer=request.user.customer
    cust = Customer.objects.get(email = customer)
    if cust.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    
    orders=customer.order_set.all()
    total_orders = orders.count()
    products=Product.objects.filter(customer=customer)
    main_pro = Product.objects.all()
    customerproduct = CustomerProduct.objects.all()
    items=[]
    k = 0
    for i in orders :
        order_items=i.orderitem_set.all()
        items.append(order_items)
    for i in products:
        k+=1
    



    context = {'k':k,'products':products , 'orders':orders ,'items':items ,'total_orders':total_orders}

    return render(request ,'store_temps/customer.html', context )
###########################################################
@auth_user
def about_you(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    
    if request.method=='POST':
        
        fname = request.POST['fname'] 
        email = request.POST['email']   
        phone = request.POST['phone']   
        teleuser = request.POST['teleuser']   
        age = request.POST['age']   
        study = request.POST['study']   
        gender = request.POST['gender']   
        work = request.POST['work']      
        user_img = request.POST['user_img']
        
        customer.name = fname
        customer.email = email
        customer.phone = phone
        customer.telegram_username = teleuser
        customer.age = age
        customer.study = study
        customer.gender = gender
        customer.work_field = work
        customer.user_image = user_img
        customer.save()


        messages.success(request , (" Porfile Has Been Saved..!!"))
        return redirect ('about_you')



    context = {'customer':customer}
    return render(request ,'store_temps/about_you.html', context )
#############################################Maintenance

def maintenance(request):
    pass
    context = {}
    return render(request ,'store_temps/maintenance.html', context )

#####################################

def page_not_found(request , exception ):
    
    return render(request ,'store_temps/page404.html' )

#####################################
# from datetime import datetime
def contact_us(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ####################
    # if request.method=='POST':
    #     username = request.POST['username'] 
    #     subject = request.POST['subject']   
    #     message = request.POST['message']   
    #     d = str(datetime.now().day)
    #     m = str(datetime.now().month)
    #     y = str(datetime.now().year)
    #     h = str(datetime.now().hour)
    #     mn = str(datetime.now().minute)
    #     now =y+'-'+ m +'-'+d +' '+'in'+ ' ' +h+':' +mn


    #     email_inbox = InboxEmail.objects.create(customer = customer , subject = subject , message = message ,time_send = now )
    #     email_inbox.save()


    return render(request ,'store_temps/contact_us.html' )
####################################################
def process_contact(request):
    data = json.loads(request.body)
    subject = data['subject']
    message = data['message']
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    d = str(datetime.datetime.now().day)
    m = str(datetime.datetime.now().month)
    y = str(datetime.datetime.now().year)
    h = str(datetime.datetime.now().hour)
    mn = str(datetime.datetime.now().minute)
    now =y+'-'+ m +'-'+d +' '+'in'+ ' ' +h+':' +mn
    
    email_inbox = InboxEmail.objects.create(customer = customer , subject = subject , message = message ,time_send = now )
    email_inbox.save()

    
    return JsonResponse('item was added',safe=False)
#################################MAIN-PAGE
@auth_user
def store(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################
    tele = 'https://t.me/hamzeib'
    what = 'https://wa.me/963988354687'
    
    data = cartData(request)
    cartItems = data['cartitems']
    form = create_customer_prd(request)
    bool = is_admin(request)
    print(bool)
    get_orders_from_text_file()
    products=Product.objects.all()#استعلمنا عن كل المنتجات

    ############################################for Control Ads
    ad = []
    ads = Ads.objects.all()
    fad = Ads.objects.get(name = 'AdNO1')
    for i in ads:
        if i.name == 'AdNO1':
            continue
        ad.append(i)

    ########################################For Preferance
    # this_prefer = []
    # preferances = preferance(request)
    # print("preferances")
    # print(preferances)
    # categories = ["Book" ,"Fashion" ,"Electronic","Mobiles"]
    # try:
#     te = []
#     if request.user.is_authenticated:
#         rand = random.randint(10000000,999999999)
#         #old_step = userpreferance.objects.get(user = request.user).prefer
#         this_preferance  = userpreferance.objects.create(user = request.user , prefer = preferances , unique = rand )
#         this_preferance.save()

#         #old_step  =userpreferance.objects.get(prefer = preferances).old_step
#         last_ele = userpreferance.objects.get(unique = rand).prefer
#         last_ele_helper = userpreferance.objects.get(unique = rand).unique
#         print(last_ele)
#         moves = []
#         user_prefer = userpreferance.objects.all()
#         for i  in user_prefer:
#             moves.append(i.prefer)
        
    
    
#         #moves += m
#         print(moves)
#         last = moves[len(moves)-1]
#         #if last == []:
#         lastt = moves[len(moves)-2]
#         if last =='[]':
#             last = lastt
#         #     moves -=last
#         # print(moves)
#         first = moves[0]
#         print(first)
#         print('-----------------------')
#         print(last)
#         append_prefer_in_file(moves , request.user )
#         te = get_prefer_from_file()
        
#         for ele in user_prefer:
#             if ele.prefer == last_ele and ele.unique ==last_ele_helper:
#                 this_preferance  = userpreferance.objects.create(user = request.user , prefer = preferances , unique = rand,old_step=last )
                
#                 break
        
                

#             else:
#                 ele.delete()


    
    
#     if preferances == [] and te == []:
#         this_prefer = Product.objects.all()
#         z_index = random.randint(0,3)
#         p = categories[z_index]
#         res = Product.objects.filter(category= p )
#         this_prefer = res
#     else:
#         # listt = [item.strip("[ ]") for item in te]
#         # l = [item.strip(" '' ") for item in listt]
#          # l here I have a list come from file it last move for user in orders
#         preferances = te
#         if preferances == []:
#             this_prefer = Product.objects.all()
#             z_index = random.randint(0,3)
#             p = categories[z_index]
#             res = Product.objects.filter(category= p )
#             this_prefer = res
#     # il = userpreferance.objects.get(old_step=last).old_step
#     print("-----te----")
#     print(te)
#     # print(te[0])
    


   
#     print("----l---")
#     print(te)
#     #pre = userpreferance.objects.get(user = request.user)
#     ######here i wwwww
#     for i in preferances:
#         print(i)
#         if i == 'Fashion':
#             this_prefer += Fashion
#         if i == 'clothes':   
#             this_prefer += clothes
#         if i == 'EGIFT Card':   
#             this_prefer += EGIFT_Card
#         if i == 'watch':   
#             this_prefer += watch
#         if i == 'Book':   
#             this_prefer += Book
#         if i == 'Home & Kitchen':   
#             this_prefer += Home_and_Kitchen
#         if i == 'Electronic':   
#             this_prefer += elc
#         if i == 'Mobiles':   
#             this_prefer += Mobiles
#         if i == 'shoes':   
#             this_prefer += shoes
    
        
#     print(this_prefer)
    
    
    
#   ################################  
#     #this_preferance.delete()


#     #كلشي فوق ممرقو باسمو بالكونتيكست
   
#    ###################Trending part

    products = Product.objects.all()
    arr = {}
    p = []
    pro = []
    for i in products:
        product = i.name
        pro.append(product)
        p.append(0)
    
    arr = {key: value for key, value in zip(pro,p )}
    # print("--------------------------------------------------arrr")
    # print(arr)


    trend = get_trend_from_file()
    trending = []
    for i in trend:
        product = Product.objects.filter(name = i).first
        trending.append(product)
    # print('--------------------------------trinding')
    # print(trending)
#     #trend = tren
#     #print(trend)
#     trending = []
#     for i in trend:
#         product = Product.objects.filter(num_views = i).first
#         trending.append(product)
#     #print(trending)
#     ##############################Random Part
#     #ran = [] #this save number of random for dont repiat same product
#     # for i in products:
#     #     rand = random.randint()
#     #     if ran != []:
#     #         for j in ran:
#     #             if j == 

#     #rand = random.shuffle(products)
#     ran = []
#     for i in products:
#         ran.append(i)
#     random_sample = random.sample(ran, 16)  #sort in random order
#     rand = random_sample
#     # print(ran)
#     # print('--------------------------')
#     # print(rand)
#     count = 0
#     randon = []
#     for i in rand:
#         if count > 9:
#             break
#         else:
#             randon.append(i)
#             count +=1
#     #كلشي فوق ممرقو باسمو بالكونتيكست
# ########################################################
#     try:
#         if request.method=='POST':
#             customer =request.user.customer
#             name = request.POST['name']    
#             photo = request.POST['photo']
#             price = request.POST['price']
#             short_descript = request.POST['short_descript']
#             Ephoto = request.POST['Ephoto']
#             category = request.POST['category']
#             brand = request.POST['brand']
#             customer_prd = CustomerProduct.objects.create( customer = customer , name = name , price = price , short_desc = short_descript ,extra_photo =Ephoto , image = photo , num_views = 0,category=category   )
#             customer_prd.save()
    
#     except:
#         pass
    
    #'randon':randon,'trending':trending ,'this_prefer':this_prefer,'preferances':preferances
    context={'customer':customer,'fad':fad,'ad':ad,'trending':trending,'what':what,'tele':tele,'is_admin':bool,'form':form,'products':products , 'cartItems':cartItems }
    return render (request , 'store_temps/mainpage.html' , context)




############################CART
@auth_user
def cart(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################



    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartitems']

    # predicted_from_same_categories=Product.objects.none()
    # try:
    #     for prd in items:
    #         instance = Product.objects.filter(category=prd.product.category).exclude(id = prd.product.id)        
    #         predicted_from_same_categories |= instance

    # except:
    #     for prd in items:
    #         instance = Product.objects.filter(category=prd.get('product').get('category')).exclude(id = prd.get('product').get('id'))   
    #         predicted_from_same_categories |= instance
    # prediction_association = set()
    # prediction_association = process_association(items)
    # print(prediction_association)

    # prediction_association_categories = set()
    # prediction_association_categories = process_association_categories(items)
    # print("same category",predicted_from_same_categories)

    # predicted_product=Product.objects.none()
    # for pprd in prediction_association:
    #     instance = Product.objects.filter(name=pprd)
    #     predicted_product |= instance
    # print("predicted",predicted_product)

    # predicted_product_by_categories=Product.objects.none()
    # for pcategory in prediction_association_categories:
    #     instance = Product.objects.filter(category=pcategory)
    #     predicted_product_by_categories |= instance
    # print("predicted by cat",predicted_product_by_categories)

    # messages.success(request , (" Hello User , You Can't Go Forward Any More Please Login For continue"))
    
    #'predicted_from_same_categories':predicted_from_same_categories,'predicted_prd_by_categories':predicted_product_by_categories,'predict_prd':predicted_product,
    context = {'items':items , 'order':order , 'cartItems':cartItems}
    return render (request , 'store_temps/cart.html' , context )



#####################################Checkout
@auth_user
def Checkout(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################

    
    data = cartData(request)   
    items = data['items']
    order = data['order']
    cartItems = data['cartitems']
    #coupon = confirm_coupon(request)
    # try:
    #     location=Location_data.objects.get(customer=customer)
    #     current_loc_data={'name':customer.name,
    #                     'location':{
    #                         'latitude':location.lat,
    #                         'longitude':location.lon
    #                     }}
    #     other_location_details=[]
    #     for item in items:
    #         try:
    #             dealer=item.product.customer
    #             dealer_location=Location_data.objects.get(customer=dealer)
    #             loc_det={'name':dealer.name,
    #                     'location':{
    #                         'latitude':dealer_location.lat,
    #                         'longitude':dealer_location.lon
    #                     }}
    #             other_location_details.append(loc_det)
    #         except:
    #             pass
    #     m= create_map(current_loc_data,other_location_details)
    # except:
    #     m= folium.Map(zoom_start=25)
    append_order_into_text_file(order,items)
    # append_order_category_into_text_file(order,items)

    #'map':m._repr_html_() ,
    context = { 'items':items , 'order':order , 'cartItems':cartItems}
    return render (request , 'store_temps/checkout.html' , context )

######################################
@auth_user
@allowed_users(allowed_roles=['admins'])
@csrf_exempt
def confirm_coupon(request):
    data = json.loads(request.body)
    coup = data['coupon']
    customer = request.user.customer
    
    coupon = Coupons.objects.get(coupon = coup)
    dataa = cartData(request)   
    items = dataa['items']
    order = dataa['order']
    cartItems = dataa['cartitems']
    co = order.get_cart_total - coupon.value
    # product = Product.objects.get(id=prdid)
    # product.offer = prc
    # product.save()
    
    return co


##########################################PREFERANCE
def preferance(request):
    # data = json.loads(request.body)
    # prdid = data['prdid']
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = Order.objects.all()
        this_prefer ={}
        # preferace = {'clothes':0 , 'EGIFT Card': 0,'Book':0 ,'Fashion':0 , 'Electronic':0 , 'Mobiles':0 , 'shoes':0 }
        
        this_ord = []
        for i in orders:
            if i.customer == customer:
                this_ord.append(i) 
                print(this_ord)
        #     # this_order = Order.objects.get(customer = customer)
        this_orderitems = []
        for i in this_ord:
            this_orderitem = i.orderitem_set.all()
        #     #    print(this_orderitem)
            this_orderitems.append(this_orderitem)
        #     # this_orderitems = this_ord.orderitem_set.all()
        #     this_transaction=set()
            
        #     orr = Orderitem.objects.all()
        #     this_orr = []
        #     for i in orr:
        #         if i.customer == customer:
        #             this_orr.append(i)
        sd = []
        sk = []
        sorrted_preferance = {}
        products =[]
        for p in this_orderitem:
            this_prd=p.product.id
            
            #         this_transaction.add(this_prd)
            
            #         print(this_transaction)

            product = Product.objects.get(id=this_prd).category
            products.append(product)
        preferace = {'clothes':0 , 'EGIFT Card': 0,'Book':0 ,'Home':0,'Fashion':0 , 'Electronic':0 , 'Mobiles':0 , 'shoes':0 }
        key = sorted(preferace.keys() , key=lambda x: x , reverse=True)
        for i in products: 
            preferace[i] +=1
        #d = {'a': 1, 'b': 3, 'c': 0}
        # Sort the dictionary by value in descending order
        #sorted_d = sorted(d.items(), key=lambda x: x[1], reverse=True)
        # Print the sorted dictionary
            sorrted_preferance = sorted(preferace.items() , key = lambda x: x[1] , reverse=True)
            print(sorrted_preferance)
            
        for i in sorrted_preferance:
            for j in i:
                    #print(j)
                sd.append(j)
    #         if j == key:
    #             sd.append(j)

        for i in sd:
            for j in key:
                if i == j:
                    sk.append(i)
    #print(sk)
        co = 0
        pre = []
        for i in sk:
            if co>2:
                break
            else:
                pre.append(i)
                co +=1
        # preferances , created = userpreferance.objects.get_or_create(user = request.user , prefer = pre)
        # preferances.save()


        return  pre
    else:
        b = []
        return b



#########################################################

@auth_user
def updateItem(request):
    data = json.loads(request.body)
    prdid = data['prdid']
    action = data['action']
    print(action,prdid)#هي بس عالكوماند بتطلع

    customer = request.user.customer
    product = Product.objects.get(id=prdid)
    order , created = Order.objects.get_or_create(customer = customer , complete = False)

    orderitem , created = Orderitem.objects.get_or_create(order = order , product = product)

    Quantity = orderitem.product.quantity
    print(Quantity)
    if action =='add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    elif action =='addX10':
        orderitem.quantity = (orderitem.quantity + 10)
    elif action == 'removeX10':
        orderitem.quantity = (orderitem.quantity - 10)

    if orderitem.quantity >= Quantity:
        orderitem.quantity = Quantity
        
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    

    

    return JsonResponse('item was added',safe=False)
#######################################################

###########################
@auth_user
def getproducts(request):
    products= Product.objects.all()
    return JsonResponse({"products":list(products.values())})


###########################
@auth_user
def getcoupons(request):
    coupons= Coupons.objects.all()
    return JsonResponse({"coupons":list(coupons.values())})

#########################
@auth_user
def getordersrows(request):
    order_rows= Order.objects.all()
    return JsonResponse({"order_rows":list(order_rows.values())})

#########################

@auth_user
@allowed_users(allowed_roles=['admins'])
def getcustomer(request):
    coupons= Customer.objects.all()
    return JsonResponse({"customer":list(coupons.values())})

#########################

@auth_user
def getads(request):
    ads= Ads.objects.all()
    return JsonResponse({"ads":list(ads.values())})

#########################

@csrf_exempt
@auth_user
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer = customer , complete = False)
        # orderitem = Orderitem.objects.filter(order = order )
#  this_orderitems = []
#         for i in this_ord:
#             this_orderitem = i.orderitem_set.all()
#         #     #    print(this_orderitem)
#             this_orderitems.append(this_orderitem)
        
    else:
       customer , order =  guestOrder(request , data)

    orders = Order.objects.all()
    this_ord = []
    for i in orders:
        if i.customer == customer and i.complete == False:
            this_ord.append(i) 
    items = []
    for i in this_ord:
        this_orderitem = i.orderitem_set.all()
        # items.append(this_orderitem)
        for orderitem in this_orderitem:
            # orderitem = Orderitem.objects.get(order = i )
            prod = Product.objects.get(name = orderitem.product.name)
            prod.quantity -= orderitem.quantity
            prod.save()
        # print(orderitem)
        # for item in this_orderitem:
            # for i in item:
        print(prod.quantity)     
                
                
                
    # for i in order:
    #     this_orderitem = i.orderitem_set.all()
#  items=[]
#     k = 0
#     for i in orders :
#         order_items=i.orderitem_set.all()
#         items.append(order_items)
#     for i in products:
#         k+=1

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.state = 'Processing'
    order.save()
    
    if order.shipping == True:
            shop , created =  Shippingadd.objects.get_or_create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
                total_price = data['shipping']['total_price'],
                coupon = data['shipping']['coupon'],
            )
            shop.save()
    
    try:
        cou = Coupons.objects.get(coupon = shop.coupon )
        cou.delete()
    except:
        pass
    return JsonResponse('payment complete',safe=False)


#################search page



    
    
    

@auth_user
def Search(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################

    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render (request , 'search_page/main_search.html', context )
#############################
@auth_user
def upload_search(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################
    
    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}

    return render (request , 'search_page/upload_search.html', context )

#########################################################################################################33
@auth_user
def XBOX(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################

    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}

    return render (request , 'search_page/XBOX.html', context )

##############################
@auth_user
def Itunes(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################

    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render (request , 'search_page/Itunes.html' ,context)

##############################
@auth_user
def FreeFire(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################

    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render (request , 'search_page/FreeFire.html' ,context)

##############################
@auth_user
def Pubg(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################

    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render (request , 'search_page/Pubg.html' ,context)

##############################
@auth_user
def Master_Card(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################
    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render (request , 'search_page/Master_Card.html' ,context)

##############################
@auth_user
def Walmart(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################
    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render (request , 'search_page/Walmart.html' ,context)

##############################
@auth_user
def Amazon(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################
    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render(request , 'search_page/Amazon.html',context)

##############################
@auth_user
def Razer_Gold(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################
    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render(request , 'search_page/Razer_Gold.html',context)

##############################
@auth_user
def Uber(request):
    cust = request.user.customer
    customer = Customer.objects.get(email = cust)
    if customer.suspand == True:
        logout(request)
        messages.success(request , ("Your Account Has Been Suspended...!!!"))
        return redirect ('login')
    ##############################
    data = cartData(request)
    cartItems = data['cartitems']
    context = {'cartItems':cartItems}
    return render(request , 'search_page/Uber.html' ,context)

##############################






