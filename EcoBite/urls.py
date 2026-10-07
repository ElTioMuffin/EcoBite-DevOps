"""
URL configuration for EcoBite project.

The `urlpatterns` list routes URLs to Store. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function Store
    1. Add an import:  from my_app import Store
    2. Add a URL to urlpatterns:  path('', Store.home, name='home')
Class-based Store
    1. Add an import:  from other_app.Store import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,re_path,include
import Login.views as Login
import Store.views as Store
from Store.views import newProduct
import cart.views as Cart

def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    #path('admin/', admin.site.urls),
    
    #Login
    path('health/', health_check, name='health-check'),
    path('', Login.mainPage,name="Main"),
    path('login/auth', Login.auth,name="auth"),
    path('login/', Login.loginView,name="Login"),
    path('login/deauth', Login.deauth,name="deauth"),
    path('login/update/<int:pk>', Login.updateUser.as_view(),name="UpdateUser"),
    path('register/', Login.Registro.as_view(),name="Register"),

    #Store
    path('store/',Store.landingPage,name="Landing"),
    ##Products Store
    path('store/products/all',Store.myProducts,name="ProductsView"),
    path('store/newproduct',newProduct.as_view() ,name="NewProduct"),
    path('store/product/<int:pk>',Store.productDetails ,name="ProductDetails"),
    path('store/product/edit/<int:pk>',Store.editProduct.as_view() ,name="ProductEdit"),
    path('store/product/delete/<int:pk>',Store.removeProduct.as_view() ,name="ProductDelete"),
    ##StoreViews
    path('store/add',Store.newStore.as_view() ,name="NewStore"),
    path('store/edit/<int:pk>',Store.editStore.as_view() ,name="EditStore"),
    path('store/remove/<int:pk>',Store.removeStore.as_view() ,name="DeleteStore"),
    path('store/<int:pk>',Store.storePage ,name="StorePage"),

    #Cart
    path('cart/add/',Cart.cartAdd ,name="CartAdd"), 
    path('cart/delete/<int:id>',Cart.cartDelete ,name="CartDelete"),
    path('cart/clean/',Cart.cartClean ,name="CartClean"),
    path('cart/update/<int:id>',Cart.cartUpdate ,name="CartUpdate"),
    path('cart/',Cart.cart ,name="CartDetails"),
    ##CheckOut
    path('checkout/',Cart.checkOut,name="Checkout"),
    path('processPayment/',Cart.processPayment,name="ProcessPayment"),
    path('paymentfailed/<uuid:order_id>',Cart.payment_failed,name="PaymentFailed"),
    path('checkout/success/<uuid:order_id>',Cart.payment_success,name="PaymentSuccess"),

    #OrderProccess
    path('order/<uuid:order_id>',Cart.viewOrder,name="Order"),
    path('user/order/<uuid:order_id>',Cart.userOrder,name="UserOrder"),
    path('user/order/list',Cart.orderList,name="Orders"),
    path('order/pickup/<uuid:order_id>/<int:item_id>',Cart.confirmPickup,name="PickUp"),

    #Api 
    path('location/update',Login.updateLocation ,name="locationUpdate"),

    path('dashboard/', Store.dashboard_view, name='dashboard'),
    path('dashboard/pedidos/', Store.orders_report, name='orders_report'),
    path('dashboard/pedidos/<uuid:order_id>/', Store.order_detail, name='order_detail'),
    path('dashboard/productos/', Store.products_report, name='products_report'),
    path('dashboard/tiendas/', Store.stores_report, name='stores_report'),
    path('dashboard/tiendas/<int:store_id>/', Store.store_detail, name='store_detail'),
    path('dashboard/analytics/', Store.analytics_view, name='analytics'),

    #Admin Site
    path('admin/store/', Store.store_list, name='admin_store_list'),
    path("admin/stores/<int:pk>/edit/", Store.store_edit, name="store_edit"),
    path("admin/stores/<int:pk>/disable/", Store.store_disable, name="store_disable"),
    path("admin/stores/<int:pk>/enable/", Store.store_enable, name="store_enable"),
    
    # Exportar datos
    path('dashboard/exportar/', Store.export_dashboard_csv, name='export_csv'),
    path('dashboard/exportar/pedidos/', Store.export_orders_csv, name='export_orders_csv'),
    path('dashboard/exportar/productos/', Store.export_products_csv, name='export_products_csv'),

    path('termsofservice/', Store.termsofservice, name="terms"),
    path('guide/', Store.guide, name="guide"),

    path('chaining/', include('smart_selects.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
