from django.db import models
from django.contrib.gis.db import models
from Login.models import Users
import uuid
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
class Region(models.Model):
    name = models.TextField(verbose_name="Nombre de la Región")
    roman = models.TextField(verbose_name="Número Romano de la Región")

    def __str__(self):
        return "Región "+self.roman+" -- "+self.name

class State(models.Model):
    name = models.TextField(verbose_name="Nombre de la Comuna")
    region = models.ForeignKey(Region,on_delete=models.CASCADE, verbose_name="Region a la que Pertenece")

    def __str__(self):
        return self.name+" - "+self.region.name

class StoreType(models.Model):
    name = models.TextField(verbose_name="Categoria de Tienda")
    description = models.TextField(verbose_name="Descripción")
    categorycode = models.TextField(verbose_name="Codigo de Categoria")

    def __str__(self):
        return self.categorycode+" ---- "+self.name

class Store(models.Model):
    name = models.TextField(verbose_name="Razón Social")
    rut = models.CharField(max_length=12, verbose_name="RUT Razón Social")
    storetype = models.ForeignKey(StoreType,on_delete=models.CASCADE, verbose_name="Tipo de Tienda")
    emailowner = models.EmailField(verbose_name="Email Representante Legal")
    ownername = models.TextField(verbose_name="Nombre Representante Legal")
    ownerlastname = models.TextField(verbose_name="Apellido Representante Legal",null=True,blank=True)
    rutowner = models.CharField(max_length=12, verbose_name="RUT Representante Legal")
    owner = models.ForeignKey("Login.Users", verbose_name=("Dueño"), on_delete=models.CASCADE,null=True)
    openhr = models.TimeField(verbose_name="Hora de apertura", auto_now=False, auto_now_add=False)
    closehr = models.TimeField(verbose_name="Hora de cierre", auto_now=False, auto_now_add=False)
    phone = models.CharField(verbose_name="Teléfono")
    logo = models.ImageField(verbose_name="Logo",null=True, blank=True, upload_to='store/logos/')
    address = models.TextField(verbose_name="Dirección")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Región")
    state = ChainedForeignKey(
                                State,
                                chained_field="region",
                                chained_model_field="region",
                                on_delete=models.CASCADE,
                                verbose_name="Comuna"
                            )
    gps = models.PointField(verbose_name='',blank=True, null=True,srid=4326,geography=True)
    

class productState(models.Model):
    name = models.TextField(verbose_name="Estado : ")
    description = models.TextField(verbose_name="Descripción")

    def __str__(self):
        return self.name

class Products(models.Model):
    name = models.TextField(verbose_name="Nombre Producto")
    desc = models.TextField(verbose_name="Descripción")
    expdate = models.DateField(verbose_name="Fecha de Vencimiento")
    photo = models.ImageField(verbose_name="Imagen de Producto",upload_to='products/')
    quantity = models.IntegerField(verbose_name="Cantidad")
    state = models.ForeignKey(productState,on_delete=models.CASCADE,verbose_name="Estado del Producto:")
    price = models.IntegerField(verbose_name="Precio")
    store = models.ForeignKey(Store,on_delete=models.CASCADE,verbose_name="Tienda")
    is_sale = models.BooleanField(default=False,verbose_name="Es Oferta?")
    sale_price = models.IntegerField(default=0,verbose_name="Precio Oferta")
    
class TestCards(models.Model):
    #Cards for demo purposes, not for storing real credit cards.
    SCENARIO_CHOICES = [
        ('success', 'Pago Exitoso'),
        ('insufficient_funds', 'Fondos Insuficientes'),
        ('invalid_card', 'Tarjeta Inválida'),
        ('expired_card', 'Tarjeta Vencida'),
        ('declined', 'Pago Rechazado'),
        ('processing_error', 'Error de Procesamiento'),
    ]
    number = models.CharField(max_length=19,unique=True)
    expirydate = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    scenario = models.CharField(max_length=30,choices=SCENARIO_CHOICES)



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('failed', 'Fallido'),
        ('cancelled', 'Cancelado'),
    ]
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    user = models.ForeignKey("Login.Users", on_delete=models.SET_NULL,null=True,blank=True)
    #PaymentData
    total = models.IntegerField()
    paymentStatus = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    paymentMethod = models.CharField(max_length=50,default="Tarjeta de Credito")
    paymentScenario = models.CharField(max_length=50,blank=True)

    #Time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['paymentStatus']),
        ]



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    isPicked = models.BooleanField(default=False)


    def get_subtotal(self):
        if self.product.is_sale:
            self.price = self.product.sale_price
        return self.price*self.quantity
