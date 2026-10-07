from .cart import Cart
from Store.models import TestCards, Order,OrderItem,Store

import io
import os
import qrcode
import base64
import socket
#Django
from django.core.paginator import Paginator
from Store.models import Products
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404, redirect
import time
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def cart(request):

    cart = Cart(request)
    cartProducts = cart.get_cart()
    total = 0
    for item in cartProducts:
        if item.is_sale:
            total += item.sale_price*item.quantity_in_cart
        else:
            total += item.price*item.quantity_in_cart
    if total == 0:
        messages.warning(request,"Tu carrito está vacío")
    else:
        total += 600
        messages.warning(request,"Esta Transacción tiene una comisión de $600")

    return render(request,'cart.html',{'cartProducts':cartProducts,'total':total})

@login_required
def cartAdd(request):
    cart = Cart(request)
    if request.method == 'POST':
        try:
            productID = int(request.POST.get('product_id'))
            print(request.POST.get('product_id'))
            product = get_object_or_404(Products,id=productID)
            cart.add(product=product)

            cartQuantity = cart.__len__()

            return JsonResponse({'qty':cartQuantity})
        
        except Exception as e:
            print(e)
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

@login_required
def cartUpdate(request,id):

    cart = Cart(request)
    quantity = int(request.POST.get('quantity',1))

    success = cart.update(id,quantity)
    print(success)

    if not success:
        messages.warning(request,'No se pudo actualizar su carrito')
        return redirect(reverse_lazy('CartDetails'))

    else:
        messages.success(request,'Carrito actualizado con exito')
        return redirect(reverse_lazy('CartDetails'))

@login_required
def cartDelete(request,id):
    cart = Cart(request)
    cart.remove(id)
    messages.success(request,f'Eliminado correctamente del carrito')
    return redirect(reverse_lazy('CartDetails'))

@login_required
def cartClean(request):
    cart = Cart(request)
    cart.clear()

    messages.success(request,"Carrito Vaciado con exito")

    return redirect(reverse_lazy('CartDetails'))

@login_required
def checkOut(request):
    cart = Cart(request)
    cartProducts = cart.get_cart()

    test_cards = TestCards.objects.all()

    if not cartProducts:
        messages.warning(request,"Tu carrito esta vacio")
        return redirect(reverse_lazy("CartDetails"))
    
    total = 0
    for item in cartProducts:
        if item.is_sale:
            total += item.sale_price*item.quantity_in_cart
        else:
            total += item.price*item.quantity_in_cart

    total += 600
    return render(request,'checkout.html',{'total':total,'test_cards':test_cards, 'cart_products':cartProducts})

@login_required
def processPayment(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number','')

        cart = Cart(request)
        cartProducts = cart.get_cart()

        if not cartProducts:
            messages.error(request,"Tu carrito está Vacio")
            return redirect(reverse_lazy("CartDetails"))
        
        total = 0
        for item in cartProducts:
            if item.is_sale:
                total += item.sale_price*item.quantity_in_cart
            else:
                total += item.price*item.quantity_in_cart

        total += 600
        print(card_number)
        time.sleep(2)

        try:
            test_card = TestCards.objects.get(number=card_number)

            
            print(test_card)

        except TestCards.DoesNotExist:
            messages.error(request,"Tarjeta no válida. Por favor usa una tarjeta de prueba.")
            return redirect(reverse_lazy('Checkout'))
        
        scenario = test_card.scenario

        order = Order.objects.create(user=request.user if request.user.is_authenticated else None,
                                     total=int(total),
                                     paymentScenario=scenario)
        
        for item in cartProducts:
            OrderItem.objects.create(
                order=order,
                product=item,
                quantity=item.quantity_in_cart,
                price=int(item.price)
            )

        if scenario == 'success':
            order.paymentStatus = 'paid'
            order.save()
            cart.clear()
            messages.success(request, f'¡Pago procesado exitosamente! Orden #{order.id}')
            return redirect('PaymentSuccess', order_id=order.id)
        
        elif scenario == 'insufficient_funds':
            order.paymentStatus = 'failed'
            order.save()
            messages.warning(request, 'Fondos insuficientes. Por favor usa otra tarjeta.')
            return redirect('PaymentFailed', order_id=order.id)
        
        elif scenario == 'invalid_card':
            order.paymentStatus = 'failed'
            order.save()
            messages.warning(request, 'Tarjeta inválida. Verifica los datos de tu tarjeta.')
            return redirect('PaymentFailed', order_id=order.id)
        
        elif scenario == 'expired_card':
            order.paymentStatus = 'failed'
            order.save()
            messages.warning(request, 'Tu tarjeta está vencida. Por favor usa otra tarjeta.')
            return redirect('PaymentFailed', order_id=order.id)
        
        elif scenario == 'declined':
            order.paymentStatus = 'failed'
            order.save()
            messages.warning(request, 'Pago rechazado por el banco. Contacta a tu banco.')
            return redirect('PaymentFailed', order_id=order.id)
        
        elif scenario == 'processing_error':
            order.paymentStatus = 'failed'
            order.save()
            messages.warning(request, 'Error de procesamiento. Por favor intenta nuevamente.')
            return redirect('PaymentFailed', order_id=order.id)
    
    return redirect('checkout')

@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('product','product__store')

    items_by_store = {}

    for item in order_items:
        store = item.product.store
        product = Products.objects.get(id=item.product.id)
        if product.quantity >= item.quantity:
            product.quantity -= item.quantity
            product.save()

        if store not in items_by_store:
            items_by_store[store] = {
                'items': [],
                'total': 0
            }
        items_by_store[store]['items'].append(item)
        items_by_store[store]['total'] += item.get_subtotal()
 
    
    ip = "https://ecobite-yvsf.onrender.com/"
    url = ip+'order/'+str(order_id)
    qr = qrcode.make(url)
    buffer = io.BytesIO()
    qr.save(buffer)
    buffer.seek(0)
    img = base64.b64encode(buffer.read()).decode('utf-8')

    return render(request, 'paymentSuccess.html', {'order': order,'qr':img,'items_by_store':items_by_store})

@login_required
def payment_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'paymentFailed.html', {'order': order})

@login_required
def viewOrder(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    
    user_stores = Store.objects.filter(owner=request.user)

    order_items = OrderItem.objects.filter(
        order=order,
        product__store__in=user_stores
    ).select_related('product', 'product__store')
    
    total_count = order_items.count()
    picked_count = order_items.filter(isPicked=True).count()
    
    context = {
        'order': order,
        'order_items': order_items,
        'total_count': total_count,
        'picked_count': picked_count,
    }
    
    return render(request, 'mobile/viewOrder.html', context)

def get_active_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable — no packets are sent
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

@login_required
def userOrder(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    order_items = OrderItem.objects.filter(
        order=order
    ).select_related('product','product__store')

    total_count = order_items.count()
    picked_count = order_items.filter(isPicked=True).count()
    
    items_by_store = {}

    for item in order_items:
        store = item.product.store
        if store not in items_by_store:
            items_by_store[store] = {
                'items': [],
                'total': 0
            }
        items_by_store[store]['items'].append(item)
        items_by_store[store]['total'] += item.get_subtotal()



    ip = "https://ecobite-yvsf.onrender.com/"
    url = ip+'order/'+str(order_id)
    qr = qrcode.make(url)
    buffer = io.BytesIO()
    qr.save(buffer)
    buffer.seek(0)
    img = base64.b64encode(buffer.read()).decode('utf-8')

    context = {'order': order,
               'order_items':order_items,
                'items_by_store':items_by_store,
                'total_count':total_count,
                'picked_count':picked_count
                ,'qr':img}

    return render(request,'contents/userOrderView.html',context)

@login_required
def orderList(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(orders,10)

    page = request.GET.get('page')
    num = paginator.get_page(page)
    return render(request,'contents/userOrderList.html',{'orders':num,})

@login_required
def confirmPickup(request,order_id,item_id):
    item = get_object_or_404(OrderItem,id=item_id)
    if request.method == 'POST':
        item.isPicked = True
        item.save()

        return redirect('Order',order_id=order_id)
