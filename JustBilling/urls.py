from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('master/',include('master.urls')),
    path('product/',include('products.urls')),
    path('billing/',include('billing.urls')),
    path('vendor/',include('vendor.urls')),
    path('po/',include('po.urls')),
    path('inventory/',include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
