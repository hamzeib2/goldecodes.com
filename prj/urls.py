"""
URL configuration for prj project.

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
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('prjapp.urls')),

    path('reset_password/' , auth_views.PasswordResetView.as_view(template_name = 'auth/forget_password.html') , name = 'reset_password'),
    path('reset_password_sent/' , auth_views.PasswordResetDoneView.as_view(template_name = 'auth/reset_password_sent.html') , name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(template_name = 'auth/reset_password.html') , name = 'password_reset_confirm'),
    path('reset_password_complete/' , auth_views.PasswordResetCompleteView.as_view(template_name = 'auth/reset_password_complete.html') , name = 'password_reset_complete'),

]

handler404 = 'prjapp.views.page_not_found'

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)#هون يلي عملناه انو ربطنا الميديا يو ار ال بال ميديا روت فصار وقت منكتب الميديا يو ار ال بياخدنا عملف الميديا روت هالعملية مشان نجيب الصور
urlpatterns+= static(settings.STATIC_URL, document_root = settings.STATIC_URL)
#ما بعرف ليش حط ستاتيك

