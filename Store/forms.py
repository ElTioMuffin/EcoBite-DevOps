from django import forms
from .models import Products,productState, Store
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point

class ProductsForm(forms.ModelForm):
    termsofservice = forms.BooleanField(
        required=True,
         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Acepto los términos y condiciones",
        error_messages={'required': 'Debes aceptar los términos y condiciones para continuar.'}
    )
    class Meta:
        model = Products
        fields = [
            'name',
            'desc',
            'expdate',
            'photo',
            'quantity',
            'state',
            'price',
            'is_sale',
            'sale_price'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'login-field mb-2 form-control'}),
            'desc': forms.TextInput(attrs={'class': 'login-field mb-2 form-control'}),
            'expdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'login-field mb-2 form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'login-field mb-2 form-control'}),
            'state': forms.Select(attrs={'class': 'mb-2 form-control form-select'}),
            'price': forms.TextInput(attrs={'class': 'login-field mb-2 form-control'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_is_sale'}),
             'sale_price': forms.NumberInput(attrs={'class': 'login-field mb-2 form-control', 'id': 'id_sale_price'})
        }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].queryset = productState.objects.exclude(id=99)

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'name',
            'storetype',
            'openhr',
            'closehr',
            'phone',
            'logo',
            'address',
            'gps',
            # '',
        ]

        widgets = {
            'name' : forms.TextInput({'class': 'login-field mb-2 form-control' ,'placeholder':'',}),
            'storetype' : forms.Select({'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'openhr' : forms.TimeInput({'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'closehr' : forms.TimeInput({'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'phone' : forms.NumberInput({'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'logo' : forms.FileInput({'class': 'mb-2 form-control form-select' ,'placeholder':'','type':'file'}),
            'address': forms.TextInput({'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'gps': forms.HiddenInput()
        } 
    
    def __init__(self, user=None,gps=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = user

    def save(self, commit=True):
        store = super().save(commit=False)

        loc = Nominatim(user_agent="Geopy Library")
        location = loc.geocode(store.address)

        if location is None:
            raise ValueError(f"Fallo GeoCoding: {store.address}")

        store.gps = Point(location.longitude, location.latitude)

        if self.owner:
            store.owner = self.owner     
        
        try:
            if commit:
                store.save()
                return store
        except Exception as e:
            print(f"Error saving store: {e}")

class Stores(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'name',
            'rut',
            'ownername',
            'ownerlastname',
            'rutowner',
            'emailowner',
            'storetype',
            'openhr',
            'closehr',
            'phone',
            'logo',
            'address',
            'region',
            'state',
        ]

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':'',}),
            'rut' : forms.TextInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'ownername' : forms.TextInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'ownerlastname' : forms.TextInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'rutowner' : forms.TextInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'emailowner' : forms.EmailInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'storetype' : forms.Select(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'openhr' : forms.TimeInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':'','type':'time'},),
            'closehr' : forms.TimeInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':'','type':'time'}),
            'phone' : forms.TextInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
            'logo' : forms.FileInput(attrs={'class': 'mb-2 form-control form-select' ,'placeholder':'','type':'file'}),
            'address': forms.TextInput(attrs={'class': 'login-field mb-2 form-control' ,'placeholder':''}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["region"].widget.attrs.update({"class": "form-control"})
        self.fields["state"].widget.attrs.update({"class": "form-control"})