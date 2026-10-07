from .forms import ProductsForm,StoreForm,Stores
from .models import (
    Region, State, StoreType, Store, productState, 
    Products, TestCards, Order, OrderItem
)
from Login.models import Users,userType
#Django Imports
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, F, Q
from datetime import timedelta
from django.db.models.functions import TruncDate
import csv
import json
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.gis.db.models.functions import Distance
from django.contrib import messages
from django.contrib.gis.measure import D
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

# Create your views here.
@login_required
def landingPage(request):
    if request.user.usertype.id == 3:
        return render(request,'admin/panel.html')
    
    if not request.user.userlocation:
        productos = Products.objects.all().exclude(state__id=99).exclude(quantity=0)
        paginator = Paginator(productos,8)

        page = request.GET.get('page')
        num = paginator.get_page(page)
        return render(request,"landing.html",{'productos_ordenados':num})
    
    else:
        products = Products.objects.annotate(
            distance=Distance('store__gps', request.user.userlocation)
            ).select_related('store').order_by('distance').exclude(state__id=99).exclude(quantity=0)
        productos = []
        for product in products:
            productos.append(product)

        paginator = Paginator(productos,8)

        page = request.GET.get('page')
        num = paginator.get_page(page)
        return render(request,"landing.html",{'productos_ordenados':num})

class newProduct(LoginRequiredMixin,CreateView):
    template_name = "newProduct.html"
    form_class = ProductsForm
    model = Products
    success_url = reverse_lazy("NewProduct")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        stores = Store.objects.filter(owner=user)
        context['stores'] = stores
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        store = self.request.POST.get('store')
        self.object.store = Store.objects.get(pk=store)
        self.object.save()  # Save and capture the object
        return super().form_valid(form)

@login_required
def myProducts(request):
    stores = Store.objects.filter(owner__id=request.user.id)
    selected_store = None
    products = []

    store_id = request.GET.get("store")

    if store_id:
        selected_store = Store.objects.get(pk=store_id)
        products = Products.objects.filter(store=selected_store).exclude(state__id=99)

    return render(request, "listProducts.html", {
        "stores": stores,
        "selected_store": selected_store,
        "products": products,
    })

class editProduct(LoginRequiredMixin,UpdateView):
    template_name = 'editProduct.html'
    form_class = ProductsForm
    model = Products
    success_url = reverse_lazy('ProductsView')

class removeProduct(LoginRequiredMixin,DeleteView):
    model = Products
    template_name = 'contents/deleteProduct.html'
    success_url = reverse_lazy('ProductsView')

@login_required
def productDetails(request,pk):
    product = Products.objects.get(pk=pk)
    related = Products.objects.filter(store_id=product.store.id)
    data = {'product':product,'related':related}
    return render(request,'productView.html',data)

class newStore(LoginRequiredMixin,CreateView):
    template_name = "newStore.html"
    form_class = Stores
    model = Store
    success_url = reverse_lazy("NewStore")
    
    def form_valid(self, form):
        store = form.save(commit=False)

        ownerEmail = form.cleaned_data.get('emailowner')
        ownerName = form.cleaned_data.get('ownername')
        ownerLastName = form.cleaned_data.get('ownerlastname')

        usertype = userType.objects.get(id=2)

        user, created = Users.objects.get_or_create(email=ownerEmail, defaults={
            'email': ownerEmail,
            'name': ownerName,
            'lastname': ownerLastName,
            'usertype': usertype,
        })

        if created:
            user.set_password("pass123!")
            user.save()

        if not store.owner:
            store.owner = user

        store.save()
        return super().form_valid(form)

class editStore(LoginRequiredMixin,UpdateView):
    template_name = "editStore.html"
    form_class = Stores
    model = Store
    success_url = reverse_lazy('admin_store_list')

class removeStore(LoginRequiredMixin,DeleteView):
    model = Store
    template_name = 'contents/deleteStore.html'
    success_url = reverse_lazy('admin_store_list')

@login_required
def storePage(request,pk):
    store = Store.objects.get(id=pk)
    products = Products.objects.filter(store=store)

    paginator = Paginator(products,10)

    page = request.GET.get('page')
    num = paginator.get_page(page)

    return render(request,'storePage.html',{'productos_ordenados':num,'store':store})

@login_required
def dashboard_view(request):
    """
    Vista principal del dashboard con todas las métricas del sistema
    """
    cache_key = 'dashboard_metrics'
    context = cache.get(cache_key)

    if not context:
    # Rangos de fecha
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        last_7_days = today - timedelta(days=7)

        # ============ MÉTRICAS DE PEDIDOS ============
        total_orders = Order.objects.count()
        paid_orders = Order.objects.filter(paymentStatus='paid').count()
        pending_orders = Order.objects.filter(paymentStatus='pending').count()
        failed_orders = Order.objects.filter(paymentStatus='failed').count()
        cancelled_orders = Order.objects.filter(paymentStatus='cancelled').count()
        
        # ============ MÉTRICAS DE INGRESOS ============
        total_revenue = Order.objects.filter(
            paymentStatus='paid'
        ).aggregate(total=Sum('total'))['total'] or 0
        
        revenue_last_30_days = Order.objects.filter(
            paymentStatus='paid',
            created_at__gte=last_30_days
        ).aggregate(total=Sum('total'))['total'] or 0

        revenue_last_7_days = Order.objects.filter(
            paymentStatus='paid',
            created_at__gte=last_7_days
        ).aggregate(total=Sum('total'))['total'] or 0

        avg_order_value = Order.objects.filter(
            paymentStatus='paid'
        ).aggregate(avg=Avg('total'))['avg'] or 0

        # ============ MÉTRICAS DE PRODUCTOS ============
        total_products = Products.objects.count()
        products_in_stock = Products.objects.filter(quantity__gt=0).count()
        products_out_of_stock = Products.objects.filter(quantity=0).count()
        products_on_sale = Products.objects.filter(is_sale=True).count()
        
        # Productos que vencen pronto (próximos 30 días)
        products_expiring_soon = Products.objects.filter(
            expdate__lte=today + timedelta(days=30),
            expdate__gte=today
        ).count()

        # ============ MÉTRICAS DE TIENDAS ============
        total_stores = Store.objects.count()
        
        # Top 5 tipos de tienda
        stores_by_type = StoreType.objects.annotate(
            store_count=Count('store')
        ).order_by('-store_count')[:5]

        # Top 5 regiones
        stores_by_region = Region.objects.annotate(
            store_count=Count('store')
        ).order_by('-store_count')[:5]

        # ============ TOP PRODUCTOS VENDIDOS ============
        top_products = OrderItem.objects.values(
            'product__name', 'product__store__name'
        ).annotate(
            total_sold=Sum('quantity'),
            revenue=Sum(F('price') * F('quantity'))
        ).order_by('-total_sold')[:10]

        # ============ PEDIDOS RECIENTES ============
        recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]

        # ============ PEDIDOS POR DÍA (últimos 30 días) ============
        orders_by_day = Order.objects.filter(
            created_at__gte=last_30_days
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id'),
            revenue=Sum('total', filter=Q(paymentStatus='paid'))
        ).order_by('date')

        # Convertir a formato JSON para Chart.js
        orders_by_day_json = json.dumps([
            {
                'date': item['date'].isoformat(),
                'count': item['count'],
                'revenue': float(item['revenue']) if item['revenue'] else 0
            }
            for item in orders_by_day
        ])

        # ============ ANÁLISIS DE ESCENARIOS DE PAGO ============
        payment_scenarios = Order.objects.exclude(
            paymentScenario=''
        ).values('paymentScenario').annotate(
            count=Count('id')
        ).order_by('-count')

        # ============ TASA DE ÉXITO ============
        total_attempts = Order.objects.exclude(paymentStatus='pending').count()
        success_rate = (paid_orders / total_attempts * 100) if total_attempts > 0 else 0

        # ============ MÉTRICAS ADICIONALES ============
        # Productos con bajo stock (menos de 10 unidades)
        low_stock_count = Products.objects.filter(
            quantity__lte=10,
            quantity__gt=0
        ).count()

        # Total de items vendidos
        total_items_sold = OrderItem.objects.filter(
            order__paymentStatus='paid'
        ).aggregate(total=Sum('quantity'))['total'] or 0

        # Productos más caros
        most_expensive_products = Products.objects.order_by('-price')[:5]

        # Tiendas con más productos
        stores_with_most_products = Store.objects.annotate(
            product_count=Count('products')
        ).order_by('-product_count')[:5]

        # Preparar contexto
        context = {
            # Métricas de pedidos
            'total_orders': total_orders,
            'paid_orders': paid_orders,
            'pending_orders': pending_orders,
            'failed_orders': failed_orders,
            'cancelled_orders': cancelled_orders,
            'success_rate': round(success_rate, 2),
            
            # Métricas de ingresos
            'total_revenue': total_revenue,
            'revenue_last_30_days': revenue_last_30_days,
            'revenue_last_7_days': revenue_last_7_days,
            'avg_order_value': round(avg_order_value, 2),
            
            # Métricas de productos
            'total_products': total_products,
            'products_in_stock': products_in_stock,
            'products_out_of_stock': products_out_of_stock,
            'products_on_sale': products_on_sale,
            'products_expiring_soon': products_expiring_soon,
            'low_stock_count': low_stock_count,
            'total_items_sold': total_items_sold,
            
            # Métricas de tiendas
            'total_stores': total_stores,
            'stores_by_type': stores_by_type,
            'stores_by_region': stores_by_region,
            'stores_with_most_products': stores_with_most_products,
            
            # Datos detallados
            'top_products': top_products,
            'recent_orders': recent_orders,
            'orders_by_day': orders_by_day_json,  # JSON para Chart.js
            'payment_scenarios': payment_scenarios,
            'most_expensive_products': most_expensive_products,
        }
        # Cachear el contexto por 2 minutos
        cache.set(cache_key, context, 120)

    return render(request, 'admin/dashboard.html', context)

@login_required
def orders_report(request):
    """
    Vista para reporte detallado de pedidos con filtros
    """
    # Obtener parámetros de filtro
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    search = request.GET.get('search')
    
    # Query base
    orders = Order.objects.select_related('user').all()
    
    # Aplicar filtros
    if status:
        orders = orders.filter(paymentStatus=status)
    
    if date_from:
        orders = orders.filter(created_at__gte=date_from)
    
    if date_to:
        orders = orders.filter(created_at__lte=date_to)
    
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    # Ordenar por fecha descendente
    orders = orders.order_by('-created_at')
    
    # Estadísticas de los pedidos filtrados
    filtered_stats = {
        'total': orders.count(),
        'total_revenue': orders.filter(paymentStatus='paid').aggregate(
            total=Sum('total')
        )['total'] or 0,
        'paid_count': orders.filter(paymentStatus='paid').count(),
        'pending_count': orders.filter(paymentStatus='pending').count(),
        'failed_count': orders.filter(paymentStatus='failed').count(),
    }
    
    context = {
        'orders': orders[:100],  # Limitar a 100 resultados
        'status_filter': status,
        'date_from': date_from,
        'date_to': date_to,
        'search': search,
        'filtered_stats': filtered_stats,
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'admin/orders_report.html', context)

@login_required
def order_detail(request, order_id):
    """
    Vista detallada de un pedido específico
    """
    from django.shortcuts import get_object_or_404
    
    order = get_object_or_404(
        Order.objects.select_related('user'),
        id=order_id
    )
    
    # Obtener items del pedido
    order_items = OrderItem.objects.filter(
        order=order
    ).select_related('product', 'product__store')
    
    # Calcular subtotales
    items_with_subtotal = []
    for item in order_items:
        items_with_subtotal.append({
            'item': item,
            'subtotal': item.get_subtotal()
        })
    
    context = {
        'order': order,
        'order_items': items_with_subtotal,
    }
    
    return render(request, 'admin/order_detail.html', context)

@login_required
def products_report(request):
    """
    Vista para reporte de productos con múltiples secciones
    """
    today = timezone.now().date()
    
    # Parámetros de filtro
    store_id = request.GET.get('store')
    category = request.GET.get('category')
    
    # Query base para productos
    products_query = Products.objects.select_related('store', 'state', 'store__storetype')
    
    # Aplicar filtros si existen
    if store_id:
        products_query = products_query.filter(store_id=store_id)
    
    if category:
        products_query = products_query.filter(storetype__name=category)
    
    # Productos con bajo stock
    low_stock_threshold = 5
    low_stock_products = products_query.filter(
        quantity__lte=low_stock_threshold,
    ).order_by('quantity')[:20]
    
    # Productos que vencen pronto (próximos 30 días)
    expiring_products = products_query.filter(
        expdate__lte=today + timedelta(days=30),
        expdate__gte=today
    ).order_by('expdate')[:20]
    
    # Productos vencidos
    expired_products = products_query.filter(
        expdate__lt=today
    ).order_by('-expdate')[:20]
    
    # Productos más vendidos
    best_sellers = OrderItem.objects.values(
        'product__id',
        'product__name',
        'product__store__name',
        'product__price'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('price') * F('quantity'))
    ).order_by('-total_quantity')[:20]
    
    # Productos en oferta
    sale_products = products_query.filter(is_sale=True).order_by('-sale_price')[:20]
    
    # Productos sin ventas
    products_with_sales = OrderItem.objects.values_list('product_id', flat=True).distinct()
    products_no_sales = products_query.exclude(
        id__in=products_with_sales
    )[:20]
    
    # Estadísticas generales
    stats = {
        'total_products': products_query.count(),
        'in_stock': products_query.filter(quantity__gt=0).count(),
        'out_of_stock': products_query.filter(quantity=0).count(),
        'low_stock': low_stock_products.count(),
        'expiring_soon': expiring_products.count(),
        'expired': expired_products.count(),
        'on_sale': sale_products.count(),
        'no_sales': products_no_sales.count(),
    }
    
    # Lista de tiendas para filtro
    stores = Store.objects.all().order_by('name')
    
    # Lista de categorías para filtro
    categories = StoreType.objects.all().order_by('name')
    
    context = {
        'low_stock_products': low_stock_products,
        'expiring_products': expiring_products,
        'expired_products': expired_products,
        'best_sellers': best_sellers,
        'sale_products': sale_products,
        'products_no_sales': products_no_sales,
        'low_stock_threshold': low_stock_threshold,
        'stats': stats,
        'stores': stores,
        'categories': categories,
        'selected_store': store_id,
        'selected_category': category,
    }
    
    return render(request, 'admin/products_report.html', context)

@login_required
def stores_report(request):
    """
    Vista para reporte de tiendas con métricas de rendimiento
    """
    # Obtener filtros
    region_id = request.GET.get('region')
    store_type_id = request.GET.get('store_type')
    
    # Query base
    stores_query = Store.objects.all()
    
    # Aplicar filtros
    if region_id:
        stores_query = stores_query.filter(region_id=region_id)
    
    if store_type_id:
        stores_query = stores_query.filter(storetype_id=store_type_id)
    
    # Tiendas con sus métricas
    stores = stores_query.annotate(
        total_products=Count('products'),
        active_products=Count('products', filter=Q(products__quantity__gt=0)),
        out_of_stock_products=Count('products', filter=Q(products__quantity=0)),
        total_sales=Sum(
            'products__orderitem__quantity',
            filter=Q(products__orderitem__order__paymentStatus='paid')
        ),
        revenue=Sum(
            F('products__orderitem__price') * F('products__orderitem__quantity'),
            filter=Q(products__orderitem__order__paymentStatus='paid')
        ),
        pending_orders=Count(
            'products__orderitem__order',
            filter=Q(products__orderitem__order__paymentStatus='pending'),
            distinct=True
        )
    ).select_related('storetype', 'region', 'state', 'owner').order_by('-revenue')
    
    # Top 10 tiendas por ingresos
    top_stores_by_revenue = stores[:10]
    
    # Top 10 tiendas por cantidad de productos
    top_stores_by_products = stores.order_by('-total_products')[:10]
    
    # Estadísticas generales
    total_stores = stores.count()
    total_revenue_all = stores.aggregate(total=Sum('revenue'))['total'] or 0
    avg_products_per_store = stores.aggregate(avg=Avg('total_products'))['avg'] or 0
    
    # Distribución por región
    stores_by_region = Region.objects.annotate(
        store_count=Count('store'),
        total_revenue=Sum(
            F('store__products__orderitem__price') * F('store__products__orderitem__quantity'),
            filter=Q(store__products__orderitem__order__paymentStatus='paid')
        )
    ).order_by('-store_count')
    
    # Distribución por tipo
    stores_by_type = StoreType.objects.annotate(
        store_count=Count('store'),
        total_revenue=Sum(
            F('store__products__orderitem__price') * F('store__products__orderitem__quantity'),
            filter=Q(store__products__orderitem__order__paymentStatus='paid')
        )
    ).order_by('-store_count')
    
    # Listas para filtros
    regions = Region.objects.all().order_by('name')
    store_types = StoreType.objects.all().order_by('name')
    
    context = {
        'stores': stores,
        'top_stores_by_revenue': top_stores_by_revenue,
        'top_stores_by_products': top_stores_by_products,
        'total_stores': total_stores,
        'total_revenue_all': total_revenue_all,
        'avg_products_per_store': round(avg_products_per_store, 2),
        'stores_by_region': stores_by_region,
        'stores_by_type': stores_by_type,
        'regions': regions,
        'store_types': store_types,
        'selected_region': region_id,
        'selected_store_type': store_type_id,
    }
    
    return render(request, 'admin/stores_report.html', context)

@login_required
def store_detail(request, store_id):
    """
    Vista detallada de una tienda específica
    """
    from django.shortcuts import get_object_or_404
    
    store = get_object_or_404(
        Store.objects.select_related('storetype', 'region', 'state', 'owner'),
        id=store_id
    )
    
    # Productos de la tienda
    products = Products.objects.filter(store=store).select_related('state')
    
    # Estadísticas de productos
    product_stats = {
        'total': products.count(),
        'in_stock': products.filter(quantity__gt=0).count(),
        'out_of_stock': products.filter(quantity=0).count(),
        'on_sale': products.filter(is_sale=True).count(),
    }
    
    # Productos más vendidos de esta tienda
    top_products = OrderItem.objects.filter(
        product__store=store
    ).values(
        'product__name',
        'product__price'
    ).annotate(
        total_sold=Sum('quantity'),
        revenue=Sum(F('price') * F('quantity'))
    ).order_by('-total_sold')[:10]
    
    # Ingresos totales
    total_revenue = OrderItem.objects.filter(
        product__store=store,
        order__paymentStatus='paid'
    ).aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    
    context = {
        'store': store,
        'products': products[:50],  # Primeros 50 productos
        'product_stats': product_stats,
        'top_products': top_products,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'admin/store_detail.html', context)

@login_required
def analytics_view(request):
    """
    Vista de análisis avanzado con gráficos
    """
    today = timezone.now().date()
    last_90_days = today - timedelta(days=90)
    
    # Ventas por mes (últimos 6 meses)
    sales_by_month = Order.objects.filter(
        paymentStatus='paid',
        created_at__gte=today - timedelta(days=180)
    ).annotate(
        month=TruncDate('created_at')
    ).values('month').annotate(
        total_orders=Count('id'),
        total_revenue=Sum('total')
    ).order_by('month')
    
    sales_by_month_json = json.dumps([
        {
            'month': item['month'].isoformat(),
            'total_orders': item['total_orders'],
            'total_revenue': float(item['total_revenue'])
        }
        for item in sales_by_month
    ])
    
    # Productos por categoría
    products_by_category = Products.objects.values(
        'store__storetype__name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Ventas por región
    sales_by_region = OrderItem.objects.filter(
        order__paymentStatus='paid'
    ).values(
        'product__store__region__name'
    ).annotate(
        total_revenue=Sum(F('price') * F('quantity')),
        total_orders=Count('order__id', distinct=True)
    ).order_by('-total_revenue')
    
    context = {
        'sales_by_month': sales_by_month_json,
        'products_by_category': products_by_category,
        'sales_by_region': sales_by_region,
    }
    
    return render(request, 'admin/analytics.html', context)

@login_required
def store_list(request):
    store_qs = Store.objects.select_related("owner", "storetype").order_by("name")

    paginator = Paginator(store_qs, 10)  # 10 stores per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin/store_list.html", {
        "page_obj": page_obj
    })

@login_required
def store_disable(request, pk):
    store = get_object_or_404(Store, pk=pk)
    
    disabled_type = userType.objects.get(id=99)

    if store.owner:
        store.owner.usertype = disabled_type
        store.owner.save()

    messages.success(request, f"Cuenta tienda '{store.name}' desactivada.")
    return redirect("admin_store_list")

@login_required
def store_enable(request, pk):
    store = get_object_or_404(Store, pk=pk)

    active_type = userType.objects.get(id=2)  # adjust if needed

    if store.owner:
        store.owner.usertype = active_type
        store.owner.save()

    messages.success(request, f"Cuenta tienda '{store.name}' activada.")
    return redirect("admin_store_list")

@login_required
def store_edit(request, pk):
    store = get_object_or_404(Store, pk=pk)
    form = StoreForm(request.POST or None, instance=store)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Tienda actualizada correctamente.")
            return redirect("store_list")

    return render(request, "admin/store_edit.html", {"form": form, "store": store})

@login_required
def export_dashboard_csv(request):
    """
    Exportar métricas del dashboard a CSV optimizado para análisis de datos
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="dashboard_metricas.csv"'
    
    # Agregar BOM para Excel
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # ============================================
    # SECCIÓN 1: RESUMEN EJECUTIVO
    # ============================================
    writer.writerow(['RESUMEN_EJECUTIVO'])
    writer.writerow(['metrica', 'valor', 'unidad', 'fecha_generacion'])
    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Pedidos
    total_orders = Order.objects.count()
    paid_orders = Order.objects.filter(paymentStatus='paid').count()
    pending_orders = Order.objects.filter(paymentStatus='pending').count()
    failed_orders = Order.objects.filter(paymentStatus='failed').count()
    
    writer.writerow(['total_pedidos', total_orders, 'cantidad', timestamp])
    writer.writerow(['pedidos_pagados', paid_orders, 'cantidad', timestamp])
    writer.writerow(['pedidos_pendientes', pending_orders, 'cantidad', timestamp])
    writer.writerow(['pedidos_fallidos', failed_orders, 'cantidad', timestamp])
    writer.writerow(['tasa_conversion', f'{(paid_orders/total_orders*100) if total_orders > 0 else 0:.2f}', 'porcentaje', timestamp])
    
    # Ingresos
    total_revenue = Order.objects.filter(paymentStatus='paid').aggregate(total=Sum('total'))['total'] or 0
    last_30_days = timezone.now() - timedelta(days=30)
    revenue_30_days = Order.objects.filter(
        paymentStatus='paid',
        created_at__gte=last_30_days
    ).aggregate(total=Sum('total'))['total'] or 0
    
    writer.writerow(['ingresos_totales', total_revenue, 'CLP', timestamp])
    writer.writerow(['ingresos_ultimos_30_dias', revenue_30_days, 'CLP', timestamp])
    writer.writerow(['ticket_promedio', f'{(total_revenue/paid_orders) if paid_orders > 0 else 0:.2f}', 'CLP', timestamp])
    
    # Productos
    total_products = Products.objects.count()
    in_stock = Products.objects.filter(quantity__gt=0).count()
    out_stock = Products.objects.filter(quantity=0).count()
    on_sale = Products.objects.filter(is_sale=True).count()
    
    writer.writerow(['total_productos', total_products, 'cantidad', timestamp])
    writer.writerow(['productos_en_stock', in_stock, 'cantidad', timestamp])
    writer.writerow(['productos_sin_stock', out_stock, 'cantidad', timestamp])
    writer.writerow(['productos_en_oferta', on_sale, 'cantidad', timestamp])
    
    # Tiendas
    total_stores = Store.objects.count()
    writer.writerow(['total_tiendas', total_stores, 'cantidad', timestamp])
    
    writer.writerow([])
    writer.writerow([])
    
    # ============================================
    # SECCIÓN 2: PEDIDOS DETALLADOS
    # ============================================
    writer.writerow(['PEDIDOS_DETALLADOS'])
    writer.writerow([
        'pedido_id', 'fecha_creacion', 'fecha_actualizacion', 'estado_pago',
        'total', 'envio', 'usuario_id', 'email_usuario',
        'cantidad_items'
    ])
    
    # Usar annotate para contar items directamente en la query
    orders = Order.objects.select_related('user').annotate(
        item_count=Count('orderitem')
    ).all()
    
    for order in orders:
        writer.writerow([
            order.id,
            order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else '',
            order.updated_at.strftime('%Y-%m-%d %H:%M:%S') if order.updated_at else '',
            order.paymentStatus,
            order.total or 0,
            order.user.id if order.user else '',
            order.user.email if order.user else '',
            order.item_count or 0
        ])
    
    writer.writerow([])
    writer.writerow([])
    
    # ============================================
    # SECCIÓN 3: PRODUCTOS CON MÉTRICAS
    # ============================================
    writer.writerow(['PRODUCTOS_METRICAS'])
    writer.writerow([
        'producto_id', 'nombre', 'tienda_id', 'tienda_nombre',
        'precio', 'precio_oferta', 'en_oferta', 'cantidad_stock',
        'veces_vendido', 'unidades_vendidas', 'ingresos_generados',
        'fecha_creacion'
    ])
    
    products = Products.objects.select_related('store').annotate(
        times_sold=Count('orderitem'),
        units_sold=Sum('orderitem__quantity'),
        revenue=Sum(F('orderitem__price') * F('orderitem__quantity'))
    ).all()
    
    for product in products:
        writer.writerow([
            product.id,
            product.name or '',
            product.store.id if product.store else '',
            product.store.name if product.store else '',
            product.price or 0,
            product.sale_price if product.is_sale else '',
            'SI' if product.is_sale else 'NO',
            product.quantity or 0,
            product.times_sold or 0,
            product.units_sold or 0,
            product.revenue or 0,
            product.created_at.strftime('%Y-%m-%d') if hasattr(product, 'created_at') and product.created_at else ''
        ])
    
    writer.writerow([])
    writer.writerow([])
    
    # ============================================
    # SECCIÓN 4: ITEMS DE PEDIDOS
    # ============================================
    writer.writerow(['ITEMS_PEDIDOS'])
    writer.writerow([
        'item_id', 'pedido_id', 'producto_id', 'producto_nombre',
        'cantidad', 'precio_unitario', 'subtotal', 'tienda_id', 'tienda_nombre'
    ])
    
    order_items = OrderItem.objects.select_related(
        'order', 'product', 'product__store'
    ).all()
    
    for item in order_items:
        writer.writerow([
            item.id,
            item.order.id if item.order else '',
            item.product.id if item.product else '',
            item.product.name if item.product else '',
            item.quantity or 0,
            item.price or 0,
            (item.price or 0) * (item.quantity or 0),
            item.product.store.id if item.product and item.product.store else '',
            item.product.store.name if item.product and item.product.store else ''
        ])
    
    writer.writerow([])
    writer.writerow([])
    
    # ============================================
    # SECCIÓN 5: VENTAS POR TIENDA
    # ============================================
    writer.writerow(['VENTAS_POR_TIENDA'])
    writer.writerow([
        'tienda_id', 'tienda_nombre', 'total_productos',
        'productos_en_stock', 'total_pedidos', 'ingresos_totales',
        'ticket_promedio'
    ])
    
    stores = Store.objects.annotate(
        total_prods=Count('products'),
        prods_in_stock=Count('products', filter=Q(products__quantity__gt=0)),
        total_orders=Count('products__orderitem__order', distinct=True),
        total_revenue=Sum(
            F('products__orderitem__price') * F('products__orderitem__quantity'),
            filter=Q(products__orderitem__order__paymentStatus='paid')
        )
    ).all()
    
    for store in stores:
        avg_ticket = (store.total_revenue / store.total_orders) if store.total_orders and store.total_revenue else 0
        writer.writerow([
            store.id,
            store.name or '',
            store.total_prods or 0,
            store.prods_in_stock or 0,
            store.total_orders or 0,
            store.total_revenue or 0,
            f'{avg_ticket:.2f}'
        ])
    
    writer.writerow([])
    writer.writerow([])
    
    # ============================================
    # SECCIÓN 6: VENTAS POR DÍA (ÚLTIMOS 90 DÍAS)
    # ============================================
    writer.writerow(['VENTAS_DIARIAS'])
    writer.writerow([
        'fecha', 'total_pedidos', 'pedidos_pagados', 'pedidos_pendientes',
        'pedidos_fallidos', 'ingresos', 'ticket_promedio'
    ])
    
    last_90_days = timezone.now() - timedelta(days=90)
    
    # Usar TruncDate para agrupar por día
    from django.db.models.functions import TruncDate
    
    daily_sales = Order.objects.filter(
        created_at__gte=last_90_days
    ).annotate(
        day=TruncDate('created_at')
    ).values('day').annotate(
        total_orders=Count('id'),
        paid_orders=Count('id', filter=Q(paymentStatus='paid')),
        pending_orders=Count('id', filter=Q(paymentStatus='pending')),
        failed_orders=Count('id', filter=Q(paymentStatus='failed')),
        revenue=Sum('total', filter=Q(paymentStatus='paid'))
    ).order_by('day')
    
    for day in daily_sales:
        avg = (day['revenue'] / day['paid_orders']) if day['paid_orders'] and day['revenue'] else 0
        writer.writerow([
            day['day'].strftime('%Y-%m-%d') if day['day'] else '',
            day['total_orders'],
            day['paid_orders'],
            day['pending_orders'],
            day['failed_orders'],
            day['revenue'] or 0,
            f'{avg:.2f}'
        ])
    
    writer.writerow([])
    writer.writerow([])
    
    # ============================================
    # SECCIÓN 7: TOP PRODUCTOS
    # ============================================
    writer.writerow(['TOP_PRODUCTOS'])
    writer.writerow([
        'ranking', 'producto_id', 'producto_nombre', 'tienda_nombre',
        'unidades_vendidas', 'ingresos_generados', 'precio_promedio',
        'veces_pedido'
    ])
    
    top_products = OrderItem.objects.values(
        'product__id', 'product__name', 'product__store__name'
    ).annotate(
        units_sold=Sum('quantity'),
        revenue=Sum(F('price') * F('quantity')),
        avg_price=Avg('price'),
        times_ordered=Count('order', distinct=True)
    ).order_by('-units_sold')[:50]
    
    for idx, product in enumerate(top_products, 1):
        writer.writerow([
            idx,
            product['product__id'] or '',
            product['product__name'] or '',
            product['product__store__name'] or '',
            product['units_sold'] or 0,
            product['revenue'] or 0,
            f"{product['avg_price']:.2f}" if product['avg_price'] else '0.00',
            product['times_ordered'] or 0
        ])
    
    return response

@login_required
def export_orders_csv(request):
    """
    Exportar pedidos a CSV con filtros aplicados
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'
    
    # Agregar BOM para Excel
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # Aplicar mismos filtros que en orders_report
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    orders = Order.objects.select_related('user').all()
    
    if status:
        orders = orders.filter(paymentStatus=status)
    if date_from:
        orders = orders.filter(created_at__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__lte=date_to)
    
    orders = orders.order_by('-created_at')
    
    # Encabezados
    writer.writerow(['ID Pedido', 'Usuario', 'Email', 'Total', 'Estado', 'Método de Pago', 'Escenario', 'Fecha Creación'])
    
    # Datos
    for order in orders:
        writer.writerow([
            str(order.id),
            order.user.email if order.user else 'N/A',
            order.user.email if order.user else 'N/A',
            order.total,
            order.get_paymentStatus_display(),
            order.paymentMethod,
            order.paymentScenario,
            order.created_at.strftime('%d/%m/%Y %H:%M')
        ])
    
    return response

@login_required
def export_products_csv(request):
    """
    Exportar productos a CSV
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'
    
    # Agregar BOM para Excel
    response.write('\ufeff')
    
    writer = csv.writer(response)
    
    # Encabezados
    writer.writerow([
        'Nombre', 'Tienda', 'Precio', 'Precio Oferta', 'Cantidad', 
        'Estado', 'En Oferta', 'Fecha Vencimiento'
    ])
    
    # Obtener productos
    products = Products.objects.select_related('store', 'state').all()
    
    # Datos
    for product in products:
        writer.writerow([
            product.name,
            product.store.name,
            product.price,
            product.sale_price if product.is_sale else '',
            product.quantity,
            product.state.name,
            'Sí' if product.is_sale else 'No',
            product.expdate.strftime('%d/%m/%Y')
        ])
    
    return response

def termsofservice(request):
    return render(request, 'contents/termsofservice.html')

def guide(request):
    return render(request, 'contents/guide.html')