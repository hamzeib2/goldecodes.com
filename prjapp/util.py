import json
from . models import *
from .forms import Prd_Form
from django.forms import inlineformset_factory
from django.shortcuts import render,redirect , HttpResponse
from .decorators import unauth_user,allowed_users,auth_user
import folium
import random


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])#اذا مو مسجل دخول اليوزر رح نجيب من الريكويست الكوكيز يلي بدنا ياها ولانو هي سترينغ رح نعملا بارس ل""جيسون"" ستاتهام ههه
    except:
        cart ={} #لازم نعمل شرط اذا ما كان عنا كوكيز يخليها فاضية
        #print('cart' , cart)

    items=[]
    order={'get_cart_total' : 0 , 'get_cart_quantity' : 0 , 'shipping':False}
    cartitems=order['get_cart_quantity']

    for i in cart:
        try:  #حطيناها بجملة تري مشان اذا راح منتج من القاعدة مثلا مايطلع خطا وهو هم يستعلم بعتقد بيصير يتجاوز المنتج يلي مانو موجود

            cartitems += cart[i]['quantity']
            
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])#عم تجيب سهر المنتج يلي بالحلقة ونضربو بالكمية الموجودة بالكارت

            order['get_cart_total'] += total#عم نضيف عالمجموع سعر الطلبية كلها
            order['get_cart_quantity'] += cart[i]['quantity']#عم نضيف العناصر


            item = {        #هلق المنتجات بدنا نعرضا فمنجيب المعلومات عن طريق الاي دي من القاعدة ومنضيفا لاوبجكت ايتمس
                'product':{
                    'id':product.id,
                    'name':product.name ,
                    'price':product.price ,
                    'category':product.category,
                    'imageURL':product.imageURL,
                    },
                'quantity' : cart[i]['quantity'],
                'get_total' : total
                }
            items.append(item)

            if product.digital == False: # هي هون مادخلا مدري ليش حطا
                order['shipping'] = True

        except:
            pass

    return {'items' : items , 'order' : order  , 'cartitems' : cartitems}



def cartData(request):

    if request.user.is_authenticated:
        try:
            customer=request.user.customer#ربطنا اليوزر مع الزبون بعلاقة ون تو ون لهيك منقدر نوصل للزبون عن طريق اليوزر يلي مسجل دخول
        except:
            Customer.objects.create(user=request.user,name=request.user.username)       
        order, created=Order.objects.get_or_create(customer=customer ,complete=False)#هي طريقة لحتى نستعلم عن الاوردر واذا مافي اوردر رح ننشئ اوردر مررنا الزبون والكومبليت فالس لان بدنا البطاقة مانا مكتملة
        items=order.orderitem_set.all()#orderitem is achild of order we can access it by parent.child that attach to it all lower casses
        cartitems=order.get_cart_quantity
    else:
        cookieData = cookieCart(request)
        cartitems = cookieData ['cartitems']
        order = cookieData ['order']
        items = cookieData ['items']
    return {'items' : items , 'order' : order  , 'cartitems' : cartitems}







def guestOrder(request , data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer , created = Customer.objects.get_or_create(email = email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer = customer, complete = False)

    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        orderItem = Orderitem.objects.create(product = product , order = order , quantity = item['quantity'])
    
    return customer , order

@auth_user
def update_user_order(request):
    cookieData = cookieCart(request)
    customer=request.user.customer 
    order = Order.objects.create(customer = customer, complete = False)
    items = cookieData['items']
    for item in items:
        product = Product.objects.get(id = item['product']['id'])
        orderItem = Orderitem.objects.create(product = product , order = order , quantity = item['quantity'])
       

@auth_user
def create_customer_prd(request):
    customer = request.user.customer
    prd_form = Prd_Form(initial = {'customer':customer})
    prd_form_img =inlineformset_factory(CustomerProduct , Prd_image_customer , fields = ('prd_name' , 'prds_img'))
    prd_imgs = prd_form_img()
    
    if request.method == 'POST':      
        prd_form = Prd_Form(request.POST , request.FILES)
        if prd_form.is_valid():
            prd_form.save()
            cus_prd= CustomerProduct.objects.order_by('date_upload').last()
            prd_imgs = prd_form_img(request.POST , request.FILES , instance=cus_prd)
            if prd_imgs.is_valid():
                prd_imgs.save()
            return redirect('/store')
        
    context={'prd_form':prd_form , 'prd_imgs':prd_imgs}
    return context


@auth_user  
def is_admin(request):
    bool =False
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
        if group == 'admins':
            bool = True
    return bool


def append_order_into_text_file(order,items):
    with open("prjapp/test_file/sample.text","a") as outfile:
        # outfile.writelines(order.date_orderd.strftime("%d/%m/%y")+"-")
        for item in items:
            if not item.product.name =="":
                outfile.writelines(item.product.name+",")
        outfile.writelines("\n")
    outfile.close()

def get_orders_from_text_file():
    transactions=[]
    with open("prjapp/test_file/sample.text","r") as outfile:
        for line in outfile:
            line=outfile.readline().strip()
            if line == "":
                continue
            line=line.split(',')
            if '' in line:
                line.remove('')
            transactions.append(line)
    # print(transactions)
    return transactions

def append_order_category_into_text_file(order,items):
    with open("prjapp/test_file/sample_category.text","a") as outfile:
        # outfile.writelines(order.date_orderd.strftime("%d/%m/%y")+"-")
        for item in items:
            if not item.product.name =="":
                outfile.writelines(item.product.category+",")
        outfile.writelines("\n")
    outfile.close()

def get_orders_category_from_text_file():
    transactions=[]
    with open("prjapp/test_file/sample_category.text","r") as outfile:
        for line in outfile:
            line=outfile.readline().strip()
            if line == "":
                continue
            line=line.split(',')
            if '' in line:
                line.remove('')
            transactions.append(line)
    # print(transactions)
    return transactions

def create_map(current_location_data,other_location_details):
    curren_lat=current_location_data['location']['latitude']
    current_lon=current_location_data['location']['longitude']
    m= folium.Map(location=[curren_lat,current_lon],zoom_start=25)
    coordinates=(curren_lat,current_lon)
    folium.Marker(coordinates,popup=current_location_data['name']).add_to(m)
    for loc in other_location_details:
        try:
            coordinates=(loc['location']['latitude'],loc['location']['longitude'])
            folium.Marker(coordinates,popup=loc['name']).add_to(m)
        except:
            pass
    return m
####################################
def create_map_current_location_only(current_location_data):
    curren_lat=current_location_data['location']['latitude']
    current_lon=current_location_data['location']['longitude']
    m= folium.Map(location=[curren_lat,current_lon],zoom_start=25)
    coordinates=(curren_lat,current_lon)
    folium.Marker(coordinates,popup=current_location_data['name']).add_to(m)
    return m


###################for preferance

def create_text_file():
    s= random.randint(1,10000000)
    audio_file = 'movess' +str(s) + '.text'
    file = open(audio_file, "a")
    # os.add(audio_file)
    #os.remove(audio_file)
    return file


import re
def append_prefer_in_file(moves ,rand):
    s= random.randint(1,10000000)
    text_file = 'movess' +str(s) + '.text'
    # file = open(text_file , 'a')
    with open( "prjapp/test_file/movess.text","a") as f:
        # outfile.writelines(order.date_orderd.strftime("%d/%m/%y")+"-")
        last = moves[len(moves)-1]
        first = moves[0]
        c = 1 
        while True:
            if last == moves[len(moves)-2]:
                    break
            
            if last =='[]':
                if last == first:
                    break
                
                last = moves[len(moves)-c]
                c +=1
            else:
               
                f.writelines(last)
                f.writelines("\n")
                
                break
        
        
    

def get_prefer_from_file():
    transactions=[]
    
    with open("prjapp/test_file/movess.text","r") as outfile:
        for line in outfile:
            line=outfile.readline().strip()
            if line == "":
                continue
            line=line.split(',')
            if ''  in line:
                line.remove('')
            if '[]'  in line:
                line.remove('')
            transactions.append(line)
    if transactions != []:
        te = transactions[len(transactions)-1]
        te= get_prefer(transactions)
    else:
        te = []   
    # print("trans")
    
    # print(transactions)
    
    return te


def get_prefer(transactions):
    
    preferace = {'clothes':0 , 'EGIFT Card': 0,'Book':0 ,'Home':0,'Fashion':0 , 'Electronic':0 , 'Mobiles':0 , 'shoes':0 }
    t = []
    for i in transactions:
        listt = [item.strip("[ ]") for item in i]
        l = [item.strip(" '' ") for item in listt]
        t.append(l)
    for i in t:
        for j in i:
            preferace[j] +=1
    key = sorted(preferace.keys() , key=lambda x: x , reverse=True)
    sorrted_preferance = sorted(preferace.items() , key = lambda x: x[1] , reverse=True)
    sd = []
    sk = []
    for i in sorrted_preferance:
        for j in i:
            sd.append(j)
    for i in sd:
        for j in key:
            if i == j:
                sk.append(i)
    co = 0
    pre = []
    for i in sk:
        if co>2:
            break
        else:
            pre.append(i)
            co +=1
    return pre


 ###################for Trending

def get_trend_from_file():
    transactions=[]
    
    with open("prjapp/test_file/sample.text","r") as outfile:
        for line in outfile:
            line=outfile.readline().strip()
            if line == "":
                continue
            line=line.split(',')
            if ''  in line:
                line.remove('')
            if '[]'  in line:
                line.remove('')
            transactions.append(line)
    if transactions != []:
        te = transactions[len(transactions)-1]
        products = Product.objects.all()
        arr = {}
        p = []
        pro = []
        for i in products:
            product = i.name
            pro.append(product)
            p.append(0)
        arr = {key: value for key, value in zip(pro,p )}
        te= get_trend(transactions , arr)
    else:
        te = []   
    # print("trans")
    
    # print(transactions)
    
    return te


def get_trend(transactions , arr):
   
    # {'watch': 0, 'head phones': 0, 'black tshirt': 0, 'sport shoes': 0, 'jeans jacket': 0, 'Deshes': 0, 'head phone': 0, 'shirt': 0, 'labtop': 0, 'labtops': 0, 'Hawawi p60': 0, 'IPhone 13': 0, 'Redmi Note 12': 0, 'NIRLON': 0, 'kitchen': 0, 'learn Python': 0, 'learn Python 2': 0, 'Learn JavaScript': 0, 'Learn JS(Ajax)': 0, 'Learn JavaScript (2)': 0, 'Itunes': 0, 'Amazon': 0, 'Rezer Gold': 0, 'Master Card': 0, 'Payeer': 0, 'MAC': 0, 'MACs': 0, 'books': 0, 'sneakers': 0, 'gentle shoes': 0, 't shirt': 0, 'leo': 0, 'watchs': 0, 'ketchup': 0, 'musterd': 0}
    
    trend = arr
    t = []
    for i in transactions:
        listt = [item.strip("[ ]") for item in i]
        l = [item.strip(" '' ") for item in listt]
        t.append(l)

    try:
        for i in t:
            for j in i:
                trend[j] +=1
    except:
        pass
    
    # print('---------------------------trendinggg')
    # print(trend)
    key = sorted(trend.keys() , key=lambda x: x , reverse=True)
    sorrted_trend = sorted(trend.items() , key = lambda x: x[1] , reverse=True)
    sd = []
    sk = []
    for i in sorrted_trend:
        for j in i:
            sd.append(j)
    for i in sd:
        for j in key:
            if i == j:
                sk.append(i)
    co = 0
    pre = []
    for i in sk:
        if co>5:
            break
        else:
            pre.append(i)
            co +=1
    return pre

######################################

