from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.gis.db import models

class userType(models.Model):
    name = models.TextField(verbose_name="Nombre")
    desc = models.TextField(verbose_name="Descripción")

    def __str__(self):
        return self.name
    
class Users(AbstractBaseUser):
    name = models.TextField(verbose_name="Nombre")
    lastname = models.TextField(verbose_name="Apellido")
    email = models.EmailField(verbose_name="Email",unique=True)
    password = models.TextField(verbose_name="Contraseña")
    usertype = models.ForeignKey("userType", verbose_name="", on_delete=models.CASCADE)
    userlocation = models.PointField(verbose_name='',blank=True,null=True)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
