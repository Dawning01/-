"""mm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from login import views as user_views
from toke import views as btoken_views
from payment import views as payment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/login',user_views.UsersView.as_view()),
    path('v1/tokens',csrf_exempt(btoken_views.TokenView.as_view())),
    path('v1/login/',include('login.urls')),
    path('v1/users/',include('user.urls')),
    path('v1/change/',include('change.urls')),
    path('payment/', include('payment.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.ALIPAY_RETURN_URL, document_root=settings.ALIPAY_KEY_DIR)
# urlpatterns += static(settings.ALIPAY_NOTIFY_URL, document_root=settings.ALIPAY_KEY_DIR)