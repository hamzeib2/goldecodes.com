from django.forms import ModelForm
from .models import *
import datetime

class Prd_Form(ModelForm):
    class Meta:
        model = CustomerProduct
        fields = ['customer','name','price','digital','category','tall_desc','image', 'extra_photo','customer_store_name','product_brand_tag','product_tag']
        #fields = ['customer','name'] #if I want just some fields not all of them


class UP_Prd_Form(ModelForm):
    class Meta:
        model = Product
        fields = ['customer','name','price']
        


class ADD_Prd_Form(ModelForm):
    required_css_class='required-field'
    class Meta:
        model = Product
        fields = ['customer','name','price','digital','category', 'short_desc','tall_desc','num_views','image', 'extra_photo','customer_store_name','product_brand_tag','product_tag']
        
class Brand_Form(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'

class Tag_Form(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class Customer_Form(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
             
    def __init__(self, *args,**kwargs):
        super(Customer_Form,self).__init__(*args, **kwargs)
        current_day=int(datetime.date.today().strftime("%d"))
        current_month=int(datetime.date.today().strftime("%m"))
        update_day=int(self.instance.info_updated.strftime("%d"))
        update_month=int(self.instance.info_updated.strftime("%m"))
        bool=False
        day_range=0
        if current_month == update_month:
            day_range=current_day - update_day
        elif update_month in (1,5,7,8,10,12):
            day_range = 31-update_day+current_day
        elif update_month in (3,4,6,9,11):
            day_range = 30-update_day+current_day
        elif update_month in (2):
            day_range = 28-update_day+current_day
        if day_range<=10:
            bool = True
        if bool:
            self.fields['name'].disabled=True
            self.fields['age'].disabled=True
            self.fields['work_field'].disabled=True
            self.fields['study'].disabled=True
            self.fields['sex'].disabled=True
