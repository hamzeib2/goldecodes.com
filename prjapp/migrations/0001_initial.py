# Generated by Django 5.0 on 2023-12-29 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prd_brand_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.CharField(blank=True, max_length=255, null=True)),
                ('value', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer_Store_Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DayEarnings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earnings_date', models.DateField()),
                ('earnings_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prd_tag_name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verify_code', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('user_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('telegram_username', models.CharField(blank=True, max_length=200, null=True)),
                ('suspand', models.BooleanField(default=False)),
                ('password', models.CharField(blank=True, max_length=200, null=True)),
                ('age', models.CharField(blank=True, choices=[('under 15', 'under 15'), ('from 15 to 20', 'from 15 to 20'), ('from 21 to 25', 'from 21 to 25'), ('from 26 to 32', 'from 26 to 32'), ('from 33 to 36', 'from 33 to 36'), ('from 37 to 42', 'from 37 to 42'), ('from 43 to 47', 'from 43 to 47'), ('more than 48', 'more than 48')], max_length=200, null=True)),
                ('study', models.CharField(blank=True, choices=[('school_student', [('elementry school', 'elemebtary school'), ('high school', 'high school'), ('other', 'other')]), ('college_student', [('medical colleges', 'medical colleges'), ('engineering colleges', 'engineering colleges'), ('literary colleges', 'litrary colleges'), ('science colleges', 'science colleges'), ('other', 'other')])], max_length=200, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], max_length=200, null=True)),
                ('work_field', models.CharField(blank=True, choices=[('governmental employee', [('work in government department', 'work in government department'), ('teacher', 'teacher'), ('other', 'other')]), ('free_work', [('clothes dealer', 'clothes dealer'), ('electronics dealer', 'electronics dealer'), ('librarian', 'librarian'), ('not_working', 'not_working')]), ('other', 'other')], max_length=200, null=True)),
                ('info_updated', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('category', models.CharField(choices=[('Mobiles', 'Mobiles'), ('Electronic', 'Electronic'), ('Home', 'Home'), ('Fashion', 'Fashion'), ('Book', 'Book'), ('EGIFT Card', 'EGIFT Card'), ('Market', 'Market'), ('watch', 'watch'), ('shoes', 'shoes'), ('clothes', 'clothes'), ('other', 'other')], max_length=200, null=True)),
                ('num_views', models.IntegerField(blank=True, null=True)),
                ('short_desc', models.TextField(blank=True, null=True)),
                ('tall_desc', models.TextField(blank=True, null=True)),
                ('date_upload', models.DateTimeField(auto_now_add=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('extra_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('extra_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.customer')),
                ('customer_store_name', models.ManyToManyField(to='prjapp.customer_store_name')),
                ('product_brand_tag', models.ManyToManyField(to='prjapp.brand')),
                ('product_tag', models.ManyToManyField(to='prjapp.tag')),
            ],
        ),
        migrations.CreateModel(
            name='InboxEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=20000)),
                ('time_send', models.CharField(max_length=200)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Location_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=200, null=True)),
                ('city_name', models.CharField(max_length=200, null=True)),
                ('lat', models.FloatField(max_length=200, null=True)),
                ('lon', models.FloatField(max_length=200, null=True)),
                ('customer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prjapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_orderd', models.DateTimeField(auto_now=True)),
                ('complete', models.BooleanField(default=False)),
                ('delevered', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('state', models.CharField(blank=True, choices=[('Rejected', 'Rejected'), ('Processing', 'Processing'), ('Complate', 'Complate')], max_length=200)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Prd_image_customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prds_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('prd_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prjapp.customerproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.IntegerField(blank=True, default=0, null=True)),
                ('offer', models.FloatField()),
                ('revenue', models.IntegerField(blank=True, default=0, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('category', models.CharField(blank=True, choices=[('Amazon', 'Amazon'), ('Amazon-UK', 'Amazon-UK'), ('Amazon-German', 'Amazon-German'), ('Itunes', 'Itunes'), ('Razer-Gold', 'Razer-Gold'), ('Razer-Gold-Global', 'Razer-Gold-Global'), ('Master-Card', 'Master-Card'), ('Wolmart', 'Wolmart'), ('Uber', 'Uber'), ('XBOX', 'XBOX'), ('FreeFire', 'FreeFire'), ('Pubg', 'Pubg'), ('clothes', 'clothes'), ('other', 'other')], max_length=200)),
                ('short_desc', models.TextField(blank=True)),
                ('tall_desc', models.TextField(blank=True)),
                ('num_views', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('extra_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('extra_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('date_upload', models.DateTimeField(auto_now_add=True, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.customer')),
                ('customer_store_name', models.ManyToManyField(blank=True, to='prjapp.customer_store_name')),
                ('product_brand_tag', models.ManyToManyField(blank=True, to='prjapp.brand')),
                ('product_tag', models.ManyToManyField(blank=True, to='prjapp.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Prd_image_store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prds_img', models.ImageField(blank=True, null=True, upload_to='')),
                ('prd_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prjapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Orderitem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Shippingadd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('total_price', models.FloatField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prjapp.order')),
            ],
        ),
        migrations.CreateModel(
            name='userpreferance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('prefer', models.CharField(blank=True, max_length=255, null=True)),
                ('unique', models.CharField(blank=True, max_length=10, null=True)),
                ('old_step', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
