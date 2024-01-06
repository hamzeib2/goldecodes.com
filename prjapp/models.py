from django.db import models
from django.contrib.auth.models import User

# Create your models here.(DataBase..!!!)


#models.ForeignKey(which table we want connact )    this for connact table

class Ads(models.Model):
    name=models.CharField(max_length=200,null=True)
    photo = models.ImageField(null=True,blank=True)
    def __str__(self):
        return self.name +" "+"id:"+" "+str(self.id)

    @property 
    def imageURL(self):#اذا ما عنا صورة رح يعطينا خطا لهيك عملنا تابع مشان يشوف اذا في صورة بيحط الرابط واذا لا بيخلي الرابط فاضي
        try:
            url = self.photo.url
        except:
            url=''
        return url


class Coupons(models.Model):
    coupon = models.CharField(max_length=255, blank=True , null=True)
    value = models.IntegerField(blank=True , null=True)
    def __str__(self):
        return self.coupon + ' : '+ str(self.value)
    


class DayEarnings(models.Model):

    earnings_date = models.DateField()
    earnings_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    def __str__(self):
        return str(self.earnings_date) + ' : '+ str(self.earnings_amount)








class userpreferance(models.Model):
    user = models.ForeignKey( User , on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True , null=True)
    prefer = models.CharField(max_length=255, blank=True , null=True)
    unique = models.CharField(max_length=10 , blank=True , null=True)
    old_step = models.CharField(max_length=255, blank=True , null=True)

    def __str__(self):
        return str(self.user)+' ' +'preferance'



class Customer(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)# كل زبون واحد مرتبط بحساب واحد فقط وممكن نكون فاضي هي الخانة
    verify_code = models.CharField(max_length=200,null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    user_image = models.ImageField(null=True,blank=True)
    email=models.CharField(max_length=200,null=True,blank=True)
    phone=models.CharField(max_length=200,null=True,blank=True)
    telegram_username=models.CharField(max_length=200,null=True,blank=True)
    suspand =models.BooleanField(default=False)
    password = models.CharField(max_length=200,null=True,blank=True)
    age_range = (
        ('under 15','under 15'),
        ('from 15 to 20' , 'from 15 to 20'),
        ('from 21 to 25' , 'from 21 to 25'),
        ('from 26 to 32' , 'from 26 to 32'),
        ('from 33 to 36' , 'from 33 to 36'),
        ('from 37 to 42' , 'from 37 to 42'),
        ('from 43 to 47' , 'from 43 to 47'),
        ('more than 48' , 'more than 48'),
        )

    age=models.CharField(max_length=200,null=True ,blank=True,choices=age_range)
    study_field= (
        ('school_student', (
            ('elementry school', 'elemebtary school'),
            ('high school', 'high school'),
            ('other','other')
        )),
        ('college_student', (('medical colleges','medical colleges'),
                            ('engineering colleges','engineering colleges'),
                            ('literary colleges','litrary colleges'),
                            ('science colleges','science colleges'),
                            ('other','other'),)

        ))
    study=models.CharField(max_length=200,null=True,blank=True,choices=study_field)
    sex=(('male','male'),('female','female'))
    gender=models.CharField(max_length=200,null=True,blank=True,choices=sex)
    work= (
        ('governmental employee', (
            ('work in government department', 'work in government department'),
            ('teacher', 'teacher'),
            ('other','other')
        )),
        ('free_work',  (('clothes dealer','clothes dealer'),
                        ('electronics dealer','electronics dealer'),
                        ('librarian','librarian'),
                        ('not_working','not_working'),)

        ),
        ('other','other')
        )
    work_field=models.CharField(max_length=200,null=True ,blank=True,choices=work)
    info_updated = models.DateTimeField(auto_now=True,null=True,blank=True)


    def __str__(self):
        return str(self.email)#القيمة يلي رح يرجعها منل عنوان بالجداول التابع متل باني للكلاس
    
    @property 
    def imageURL(self):#اذا ما عنا صورة رح يعطينا خطا لهيك عملنا تابع مشان يشوف اذا في صورة بيحط الرابط واذا لا بيخلي الرابط فاضي
        try:
            url = self.user_image.url
        except:
            url=''
        return url
    
###############################################
class Location_data(models.Model):
    customer= models.OneToOneField(Customer,on_delete=models.CASCADE,null=True,blank=True)
    country_name=models.CharField(max_length=200,null=True)
    city_name=models.CharField(max_length=200,null=True)
    lat=models.FloatField(max_length=200,null=True)
    lon=models.FloatField(max_length=200,null=True)

    def __str__(self):
        return "location of : "+str(self.customer.name)
###############################################
class Customer_Store_Name(models.Model):
    store_name=models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.store_name 
################################################
class Brand(models.Model):
    prd_brand_name=models.CharField(max_length=200,null=True,blank=False)
    def __str__(self):
        return self.prd_brand_name 
################################################
class Tag(models.Model):
    prd_tag_name=models.CharField(max_length=200,null=True,blank=False)
    def __str__(self):
        return self.prd_tag_name       

###############################################
class CustomerProduct(models.Model):
    CATEGORY = (
        ('Mobiles' , 'Mobiles'),
        ('Electronic' , 'Electronic'),
        ('Home' , 'Home'),
        ('Fashion' , 'Fashion'),
        ('Book' , 'Book'),
        ('EGIFT Card' , 'EGIFT Card'),
        ('Market' , 'Market'),
        ('watch','watch'),
        ('shoes','shoes'),
        ('clothes','clothes'),
        ('other','other')
    )
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    name=models.CharField(max_length=200,null=True)#اسم المنتح
    price=models.DecimalField(max_digits=5,decimal_places=2)#السعر 5 خانات وخانتين بعد الفاصلة
    digital=models.BooleanField(default=False,null=True,blank=True)#  قيمة بتدل على انو المنتج رقمي ولا لا مشان النقل بعدين وفينا نخليها فاضية والديفولت تبعا فيزيائي قيمة البلانط ببتدل على انو ممكن يكون فاضي والنول انو ممكن يكون فاضي جوات الفاعدة
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    num_views = models.IntegerField(null=True,blank=True) 
    short_desc = models.TextField(blank=True,null=True)
    tall_desc = models.TextField(blank=True,null=True)
    date_upload = models.DateTimeField(auto_now_add=True , null=True)
    image=models.ImageField(null=True,blank=True)#حقل لحفظ صورة المنتج
    extra_photo = models.ImageField(null=True,blank=True)
    extra_img = models.ImageField(null=True,blank=True)
    customer_store_name=models.ManyToManyField(Customer_Store_Name)
    product_brand_tag=models.ManyToManyField(Brand)
    product_tag=models.ManyToManyField(Tag)
    def __str__(self):
        return self.name 
############################################################
class Prd_image_customer(models.Model):
    prd_name = models.ForeignKey(CustomerProduct,on_delete=models.CASCADE,null=True)
    prds_img = models.ImageField(null=True,blank=True)

    if prd_name is not None:
        def __str__(self):
            return self.prd_name.name+" "+"id:"+" "+str(self.prd_name.id)
        
############################################################
class Product(models.Model):
    CATEGORY = (
        ('Amazon' , 'Amazon'),
        ('Amazon-UK' , 'Amazon-UK'),
        ('Amazon-German','Amazon-German'),
        ('Itunes' , 'Itunes'),
        ('Razer-Gold' , 'Razer-Gold'),
        ('Razer-Gold-Global' , 'Razer-Gold-Global'),
        ('Master-Card' , 'Master-Card'),
        ('Wolmart' , 'Wolmart'),
        ('Uber' , 'Uber'),
        ('XBOX' , 'XBOX'),
        ('FreeFire','FreeFire'),
        ('Pubg','Pubg'),
        ('clothes','clothes'),
        ('other','other')
    )
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    name=models.CharField(max_length=200,null=True)
    price=models.IntegerField(default=0,null=True,blank=True)
    offer=models.FloatField()
    revenue = models.IntegerField(default=0,null=True,blank=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    digital=models.BooleanField(default=False,null=True,blank=True)#قيمة بتدل على انو المنتج رقمي ولا لا مشان النقل بعدين
    category = models.CharField(max_length=200 , choices=CATEGORY,blank=True)
    short_desc = models.TextField(blank=True)
    tall_desc = models.TextField(blank=True)
    num_views = models.IntegerField(null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    extra_photo = models.ImageField(null=True,blank=True)
    extra_img = models.ImageField(null=True,blank=True)
    date_upload = models.DateTimeField(auto_now_add=True , null=True,blank=True)
    customer_store_name=models.ManyToManyField(Customer_Store_Name,blank=True)
    product_brand_tag=models.ManyToManyField(Brand,blank=True)
    product_tag=models.ManyToManyField(Tag,blank=True)

    def __str__(self):
        return self.name +" "+"id:"+" "+str(self.id)

    @property 
    def imageURL(self):#اذا ما عنا صورة رح يعطينا خطا لهيك عملنا تابع مشان يشوف اذا في صورة بيحط الرابط واذا لا بيخلي الرابط فاضي
        try:
            url = self.image.url
        except:
            url=''
        return url
    

    @property
    def image_extra(self):
        try:
            url= self.extra_photo.url
        except:
            url=''
        return url
    
    @property
    def image_extra_p(self):
        try:
            url= self.extra_img.url
        except:
            url=''
        return url
############################################################################################
class Prd_image_store(models.Model):
    prd_name = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    prds_img = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.prd_name.name+" "+"id:"+" "+str(self.prd_name.id)

###########################################################################################
class Order(models.Model):
    CATEGORY = (
        ('Rejected' , 'Rejected'),
        ('Processing' , 'Processing'),
        ('Complate' , 'Complate'),
        
    )
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)# كل زبون ممكن بكون عندو اكنر من طلبية علاقة ميني تو ميني واذا انحذف اليوزر رح تصير الطلبية نول
    date_orderd=models.DateTimeField(auto_now=True)#حفظ زمن الطلبية
    complete=models.BooleanField(default=False) #مشان نشوف البطاقة اذا مكتملة ولا لا
    delevered=models.BooleanField(default=False)#مشان نشوف البطاقة اذا مكتملة ولا لا
    rejected=models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100 , null =True)#معلومات اضافية عن الطلبية
    state =  models.CharField(max_length=200 , choices=CATEGORY,blank=True)
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_state(self):
        if self.complete == True:
            state = 'Processing'
        if self.complete and self.delevered == True:
            state = 'Complete'
        return state



    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()#هي الطريقة يلي منجيب فيها الابناء كلن
        try:
            total = sum([item.get_price for item in orderitems])
        except:
            total = None
        return total
    
    @property
    def get_cart_quantity(self):
        orderitems=self.orderitem_set.all()#هي الطريقة يلي منجيب فيها الابناء كلن
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_revenue(self):
        orderitems=self.orderitem_set.all()#هي الطريقة يلي منجيب فيها الابناء كلن
        try:
            total = sum([(item.get_item_revenue) for item in orderitems])
        except:
            total = None
        return total

#######################################################################################################################

class Orderitem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)#بالكارت ممكن يكون اكتر طلبية للمنتج نفسو
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)#وبالكارت ممكن بكون من اورد ايتم للطلبية نفسها
    #orderitem is a child for both order and product
    #الطلبية ممكن يكون الا اكتر من اوردر ايتم والاورد ايتم يحتوي منتج
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        try:
            total=self.product.price * self.quantity#we want the total is price of product from parent product that attach to it * the quantity from here
        except:
            total = None
        return total

    @property
    def get_price_offer(self):
        try:
            total=self.product.price * ((100 - self.product.offer) / 100) #we want the total is price of product from parent product that attach to it * the quantity from here
            to = str(total)
            t = to[0:5]
            tt = float(t)
        except:
            total = None
            tt = total
        return tt

    @property
    def get_price(self):
        try:
            total=self.product.price * ((100 - self.product.offer) / 100) * self.quantity #we want the total is price of product from parent product that attach to it * the quantity from here
            to = str(total)
            t = to[0:5]
            tt = float(t)
        except:
            total = None
            tt = total
        return tt
    
    @property
    def get_item_revenue(self):
        try:
            total=self.product.price * (( self.product.revenue) / 100) * self.quantity #we want the total is price of product from parent product that attach to it * the quantity from here
            to = str(total)
            t = to[0:5]
            tt = float(t)
        except:
            total = None
            tt = total
        return tt
    
#################################
class InboxEmail(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    subject = models.CharField(max_length=200,null=False)
    message = models.CharField(max_length=20000,null=False)
    time_send = models.CharField(max_length=200,null=False)

#########################################################################################################################

class Shippingadd(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)#null can not be false beacuse there must be an order
    coupon=models.CharField(max_length=200,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    total_price = models.FloatField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address





