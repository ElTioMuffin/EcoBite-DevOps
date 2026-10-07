from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from Login.models import userType, Users
from Store.models import Region, State, StoreType, Store, productState, Products, TestCards, Order, OrderItem
from datetime import datetime, timedelta, time
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Generate extended test data for the application'
       
    def handle(self, *args, **kwargs):
        print("Limpiando Base de datos ...")
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Products.objects.all().delete()
        productState.objects.all().delete()
        Store.objects.all().delete()
        State.objects.all().delete()
        Region.objects.all().delete()
        Users.objects.all().delete()
        userType.objects.all().delete()
        StoreType.objects.all().delete()
        TestCards.objects.all().delete()

        print("Creando Regiones y Comunas...")

        data = {
            "regions": [
                {"name": "Arica y Parinacota", "romanNumber": "XV", "communes": ["Arica", "Camarones", "General Lagos", "Putre"]},
                {"name": "Tarapacá", "romanNumber": "I", "communes": ["Alto Hospicio", "Camiña", "Colchane", "Huara", "Iquique", "Pica", "Pozo Almonte"]},
                {"name": "Antofagasta", "romanNumber": "II", "communes": ["Antofagasta", "Calama", "María Elena", "Mejillones", "Ollagüe", "San Pedro de Atacama", "Sierra Gorda", "Taltal", "Tocopilla"]},
                {"name": "Atacama", "romanNumber": "III", "communes": ["Alto del Carmen", "Caldera", "Chañaral", "Copiapó", "Diego de Almagro", "Freirina", "Huasco", "Tierra Amarilla", "Vallenar"]},
                {"name": "Coquimbo", "romanNumber": "IV", "communes": ["Andacollo", "Canela", "Combarbalá", "Coquimbo", "Illapel", "La Higuera", "La Serena", "Los Vilos", "Monte Patria", "Ovalle", "Paiguano", "Punitaqui", "Río Hurtado", "Salamanca", "Vicuña"]},
                {"name": "Valparaíso", "romanNumber": "V", "communes": ["Algarrobo", "Cabildo", "Calera", "Calle Larga", "Cartagena", "Casablanca", "Catemu", "Concón", "El Quisco", "El Tabo", "Hijuelas", "Isla de Pascua", "Juan Fernández", "La Cruz", "La Ligua", "Limache", "Llaillay", "Los Andes", "Nogales", "Olmué", "Panquehue", "Papudo", "Petorca", "Puchuncaví", "Putaendo", "Quillota", "Quilpué", "Quintero", "Rinconada", "San Antonio", "San Esteban", "San Felipe", "Santa María", "Santo Domingo", "Valparaíso", "Villa Alemana", "Viña del Mar", "Zapallar"]},
                {"name": "Metropolitana de Santiago", "romanNumber": "XIII", "communes": ["Alhué", "Buin", "Calera de Tango", "Cerrillos", "Cerro Navia", "Colina", "Conchalí", "Curacaví", "El Bosque", "El Monte", "Estación Central", "Huechuraba", "Independencia", "Isla de Maipo", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Lampa", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú", "María Pinto", "Melipilla", "Ñuñoa", "Padre Hurtado", "Paine", "Pedro Aguirre Cerda", "Peñaflor", "Peñalolén", "Pirque", "Providencia", "Pudahuel", "Puente Alto", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Bernardo", "San Joaquín", "San José de Maipo", "San Miguel", "San Pedro", "San Ramón", "Santiago", "Talagante", "Tiltil", "Vitacura"]},
                {"name": "Libertador Gral. Bernardo O’Higgins", "romanNumber": "VI", "communes": ["Chimbarongo", "Chépica", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "La Estrella", "Las Cabras", "Litueche", "Lolol", "Machalí", "Malloa", "Marchihue", "Nancagua", "Navidad", "Olivar", "Palmilla", "Paredones", "Peralillo", "Peumo", "Pichidegua", "Pichilemu", "Placilla", "Pumanque", "Quinta de Tilcoco", "Rancagua", "Rengo", "Requínoa", "San Fernando", "San Francisco de Mostazal", "San Vicente de Tagua Tagua", "Santa Cruz"]},
                {"name": "Maule", "romanNumber": "VII", "communes": ["Cauquenes", "Chanco", "Colbún", "Constitución", "Curepto", "Curicó", "Empedrado", "Hualañé", "Licantén", "Linares", "Longaví", "Maule", "Molina", "Parral", "Pelarco", "Pelluhue", "Pencahue", "Rauco", "Retiro", "Romeral", "Río Claro", "Sagrada Familia", "San Clemente", "San Javier de Loncomilla", "San Rafael", "Talca", "Teno", "Vichuquén", "Villa Alegre", "Yerbas Buenas"]},
                {"name": "Ñuble", "romanNumber": "XVI", "communes": ["Bulnes", "Chillán Viejo", "Chillán", "Cobquecura", "Coelemu", "Coihueco", "El Carmen", "Ninhue", "Ñiquén", "Pemuco", "Pinto", "Portezuelo", "Quillón", "Quirihue", "Ránquil", "San Carlos", "San Fabián", "San Ignacio", "San Nicolás", "Treguaco", "Yungay"]},
                {"name": "Biobío", "romanNumber": "VIII", "communes": ["Alto Biobío", "Antuco", "Arauco", "Cabrero", "Cañete", "Chiguayante", "Concepción", "Contulmo", "Coronel", "Curanilahue", "Florida", "Hualpén", "Hualqui", "Laja", "Lebu", "Los Álamos", "Los Ángeles", "Lota", "Mulchén", "Nacimiento", "Negrete", "Penco", "Quilaco", "Quilleco", "San Pedro de la Paz", "San Rosendo", "Santa Bárbara", "Santa Juana", "Talcahuano", "Tirúa", "Tomé", "Tucapel", "Yumbel"]},
                {"name": "Araucanía", "romanNumber": "IX", "communes": ["Angol", "Carahue", "Cholchol", "Collipulli", "Cunco", "Curacautín", "Curarrehue", "Ercilla", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Lonquimay", "Los Sauces", "Lumaco", "Melipeuco", "Nueva Imperial", "Padre las Casas", "Perquenco", "Pitrufquén", "Pucón", "Purén", "Renaico", "Saavedra", "Temuco", "Teodoro Schmidt", "Toltén", "Traiguén", "Victoria", "Vilcún", "Villarrica"]},
                {"name": "Los Ríos", "romanNumber": "XIV", "communes": ["Corral", "Futrono", "La Unión", "Lago Ranco", "Lanco", "Los Lagos", "Mariquina", "Máfil", "Paillaco", "Panguipulli", "Río Bueno", "Valdivia"]},
                {"name": "Los Lagos", "romanNumber": "X", "communes": ["Ancud", "Calbuco", "Castro", "Chaitén", "Chonchi", "Cochamó", "Curaco de Vélez", "Dalcahue", "Fresia", "Frutillar", "Futaleufú", "Hualaihué", "Llanquihue", "Los Muermos", "Maullín", "Osorno", "Palena", "Puerto Montt", "Puerto Octay", "Puerto Varas", "Puqueldón", "Purranque", "Puyehue", "Queilén", "Quellón", "Quemchi", "Quinchao", "Río Negro", "San Juan de la Costa", "San Pablo"]},
                {"name": "Aisén del Gral. Carlos Ibáñez del Campo", "romanNumber": "XI", "communes": ["Aisén", "Chile Chico", "Cisnes", "Cochrane", "Coyhaique", "Guaitecas", "Lago Verde", "O’Higgins", "Río Ibáñez", "Tortel"]},
                {"name": "Magallanes y de la Antártica Chilena", "romanNumber": "XII", "communes": ["Antártica", "Cabo de Hornos (Ex Navarino)", "Laguna Blanca", "Natales", "Porvenir", "Primavera", "Punta Arenas", "Río Verde", "San Gregorio", "Timaukel", "Torres del Paine"]}
            ]
        }

        for region_data in data["regions"]:
            # Create Region
            region = Region.objects.create(name=region_data["name"], roman=region_data["romanNumber"])

            # Create States (Communes)
            for commune_name in region_data["communes"]:
                State.objects.create(name=commune_name, region=region)

        self.stdout.write(self.style.SUCCESS('Regiones y Comunas Agregadas exitosamente.'))



        # Crear Tipos de Usuario
        print("Creando Tipo de Usuarios...")
        userType.objects.create(id=1, name="Usuario", desc="Usuario Normal")
        userType.objects.create(id=2, name="Dueño", desc="Dueño de Comercios")
        userType.objects.create(id=3, name="Admin", desc="Admin")
        userType.objects.create(id=99, name="Desactivado", desc="Usuario Desactivado")

        usuario_type = userType.objects.get(pk=1)
        dueno_type = userType.objects.get(pk=2)
        admin_type = userType.objects.get(pk=3)

        print("Creando Usuarios...")
        user_credentials = []
        owner_password = "pass123!"
        customer_password = "pass123!"
        admin_password = "admin123!"

        admin = Users.objects.create(email="admin@ecobite.cl", name="Admin", lastname="EcoBite", usertype=admin_type)
        admin.set_password(admin_password)
        admin.save()


        # Dueños de tiendas
        owner_data = [
            ("maria.gonzalez@email.cl", "María", "González", Point(-70.6506, -33.4372)),
            ("juan.perez@email.cl", "Juan", "Pérez", Point(-70.6693, -33.4569)),
            ("carla.silva@email.cl", "Carla", "Silva", Point(-70.6408, -33.4372)),
            ("roberto.munoz@email.cl", "Roberto", "Muñoz", Point(-70.6550, -33.4420)),
            ("sofia.ramirez@email.cl", "Sofía", "Ramírez", Point(-70.6380, -33.4510)),
            ("diego.castro@email.cl", "Diego", "Castro", Point(-70.6620, -33.4380)),
            ("valentina.lopez@email.cl", "Valentina", "López", Point(-70.6470, -33.4450)),
            ("andres.morales@email.cl", "Andrés", "Morales", Point(-70.6580, -33.4520)),
            ("fernanda.torres@email.cl", "Fernanda", "Torres", Point(-70.6410, -33.4490)),
            ("martin.vargas@email.cl", "Martín", "Vargas", Point(-70.6530, -33.4410)),
        ]

        owners = []
        for email, name, lastname, location in owner_data:
            owner = Users.objects.create(
                email=email,
                name=name,
                lastname=lastname,
                usertype=dueno_type,
                userlocation=location
            )
            owner.set_password(owner_password)
            owner.save()
            owners.append(owner)
            user_credentials.append({
                'email': email,
                'password': owner_password,
                'name': f"{name} {lastname}",
                'type': 'Dueño'
            })

        region_rm = Region.objects.get(name="Metropolitana de Santiago")
        san_bernardo = State.objects.get(name="San Bernardo")

        # Clientes
        customer_data = [
            ("pedro.martinez@email.cl", "Pedro", "Martínez", Point(-70.6506, -33.4489)),
            ("ana.rodriguez@email.cl", "Ana", "Rodríguez", Point(-70.6400, -33.4500)),
            ("luis.fernandez@email.cl", "Luis", "Fernández", Point(-70.6600, -33.4400)),
            ("carolina.herrera@email.cl", "Carolina", "Herrera", Point(-70.6520, -33.4460)),
            ("miguel.sanchez@email.cl", "Miguel", "Sánchez", Point(-70.6430, -33.4480)),
            ("isabel.mendez@email.cl", "Isabel", "Méndez", Point(-70.6560, -33.4430)),
            ("jorge.rojas@email.cl", "Jorge", "Rojas", Point(-70.6490, -33.4470)),
            ("patricia.gutierrez@email.cl", "Patricia", "Gutiérrez", Point(-70.6540, -33.4440)),
            ("ricardo.diaz@email.cl", "Ricardo", "Díaz", Point(-70.6450, -33.4500)),
            ("laura.vega@email.cl", "Laura", "Vega", Point(-70.6570, -33.4420)),
            ("carlos.ponce@email.cl", "Carlos", "Ponce", Point(-70.6420, -33.4510)),
            ("monica.flores@email.cl", "Mónica", "Flores", Point(-70.6590, -33.4390)),
            ("felipe.nunez@email.cl", "Felipe", "Núñez", Point(-70.6460, -33.4520)),
            ("andrea.soto@email.cl", "Andrea", "Soto", Point(-70.6510, -33.4450)),
            ("sebastian.rios@email.cl", "Sebastián", "Ríos", Point(-70.6440, -33.4470)),
            ("daniela.aguirre@email.cl", "Daniela", "Aguirre", Point(-70.6550, -33.4490)),
            ("pablo.ortiz@email.cl", "Pablo", "Ortiz", Point(-70.6480, -33.4440)),
            ("camila.parra@email.cl", "Camila", "Parra", Point(-70.6600, -33.4460)),
            ("eduardo.bravo@email.cl", "Eduardo", "Bravo", Point(-70.6390, -33.4480)),
            ("gabriela.reyes@email.cl", "Gabriela", "Reyes", Point(-70.6610, -33.4410)),
        ]

        customers = []
        for email, name, lastname, location in customer_data:
            customer = Users.objects.create(
                email=email,
                name=name,
                lastname=lastname,
                usertype=usuario_type,
                userlocation=location
            )
            customer.set_password(customer_password)
            customer.save()
            customers.append(customer)
            user_credentials.append({
                'email': email,
                'password': customer_password,
                'name': f"{name} {lastname}",
                'type': 'Usuario'
            })

        print("Creando Tipos de tienda...")
        StoreType.objects.create(id=1, name="Cafeteria", description='Local dedicado a la venta de café, té y productos de panadería/pastelería', categorycode='CAF')
        StoreType.objects.create(id=2, name="Panadería", description='Venta de pan, masas, pasteles y productos horneados', categorycode='PAN')
        StoreType.objects.create(id=3, name="Frutería", description='Venta de frutas y verduras frescas', categorycode='FRU')
        StoreType.objects.create(id=4, name="Tienda Natural", description='Venta de productos orgánicos o saludables', categorycode='NAT')

        store_types = {}
        for st in StoreType.objects.all():
            store_types[st.categorycode.lower()] = st

        print("Creando Tiendas...")
        stores = [
            # Panaderías
            Store.objects.create(
                name="Panadería Don Pan",
                rut="76123456-7",
                storetype=store_types['pan'],
                emailowner=owners[0].email,
                ownername=owners[0].name,
                ownerlastname=owners[0].lastname,
                rutowner="12345678-9",
                owner=owners[0],
                openhr=time(7, 0),
                closehr=time(20, 0),
                phone="987654321",
                address="Av. Eyzaguirre 710, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7011, -33.5928)
            ),
            Store.objects.create(
                name="Panadería El Horno Dorado",
                rut="76123457-5",
                storetype=store_types['pan'],
                emailowner=owners[1].email,
                ownername=owners[1].name,
                ownerlastname=owners[1].lastname,
                rutowner="12345679-7",
                owner=owners[1],
                openhr=time(6, 30),
                closehr=time(21, 0),
                phone="987654322",
                address="Av. Portales 2450, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7089, -33.5856)
            ),
            Store.objects.create(
                name="Panadería Artesanal",
                rut="76123458-3",
                storetype=store_types['pan'],
                emailowner=owners[2].email,
                ownername=owners[2].name,
                ownerlastname=owners[2].lastname,
                rutowner="12345680-0",
                owner=owners[2],
                openhr=time(7, 0),
                closehr=time(19, 30),
                phone="987654323",
                address="Av. Los Morros 3567, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.6845, -33.6012)
            ),
            # Cafeterías
            Store.objects.create(
                name="Café Aroma",
                rut="76123459-1",
                storetype=store_types['caf'],
                emailowner=owners[3].email,
                ownername=owners[3].name,
                ownerlastname=owners[3].lastname,
                rutowner="12345681-8",
                owner=owners[3],
                openhr=time(8, 0),
                closehr=time(22, 0),
                phone="987654324",
                address="Av. Colón 456, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.6998, -33.5945)
            ),
            Store.objects.create(
                name="Café Express",
                rut="76123460-5",
                storetype=store_types['caf'],
                emailowner=owners[4].email,
                ownername=owners[4].name,
                ownerlastname=owners[4].lastname,
                rutowner="12345682-6",
                owner=owners[4],
                openhr=time(7, 30),
                closehr=time(20, 30),
                phone="987654325",
                address="Av. Freire 890, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7023, -33.5902)
            ),
            Store.objects.create(
                name="Café del Centro",
                rut="76123461-3",
                storetype=store_types['caf'],
                emailowner=owners[5].email,
                ownername=owners[5].name,
                ownerlastname=owners[5].lastname,
                rutowner="12345683-4",
                owner=owners[5],
                openhr=time(8, 0),
                closehr=time(21, 0),
                phone="987654326",
                address="Av. Eyzaguirre 1234, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7045, -33.5915)
            ),
            # Fruterías
            Store.objects.create(
                name="Verdulería Fresh",
                rut="76123462-1",
                storetype=store_types['fru'],
                emailowner=owners[6].email,
                ownername=owners[6].name,
                ownerlastname=owners[6].lastname,
                rutowner="12345684-2",
                owner=owners[6],
                openhr=time(8, 0),
                closehr=time(19, 0),
                phone="934567890",
                address="Av. Ramón Freire 567, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7015, -33.5890)
            ),
            Store.objects.create(
                name="Frutería El Huerto",
                rut="76123463-K",
                storetype=store_types['fru'],
                emailowner=owners[7].email,
                ownername=owners[7].name,
                ownerlastname=owners[7].lastname,
                rutowner="12345685-0",
                owner=owners[7],
                openhr=time(7, 0),
                closehr=time(20, 0),
                phone="934567891",
                address="Av. Portales 3120, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7102, -33.5823)
            ),
            Store.objects.create(
                name="Frutería La Cosecha",
                rut="76123464-8",
                storetype=store_types['fru'],
                emailowner=owners[8].email,
                ownername=owners[8].name,
                ownerlastname=owners[8].lastname,
                rutowner="12345686-8",
                owner=owners[8],
                openhr=time(8, 30),
                closehr=time(19, 30),
                phone="934567892",
                address="Av. Los Morros 2890, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.6867, -33.6001)
            ),
            Store.objects.create(
                name="Verduras Frescas",
                rut="76123465-6",
                storetype=store_types['fru'],
                emailowner=owners[9].email,
                ownername=owners[9].name,
                ownerlastname=owners[9].lastname,
                rutowner="12345687-6",
                owner=owners[9],
                openhr=time(7, 30),
                closehr=time(20, 0),
                phone="934567893",
                address="Av. Colón 789, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7008, -33.5958)
            ),
            # Tiendas Naturales
            Store.objects.create(
                name="Natural Life",
                rut="76123466-4",
                storetype=store_types['nat'],
                emailowner=owners[0].email,
                ownername=owners[0].name,
                ownerlastname=owners[0].lastname,
                rutowner="12345678-9",
                owner=owners[0],
                openhr=time(10, 0),
                closehr=time(20, 0),
                phone="967890123",
                address="Av. Eyzaguirre 1890, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7067, -33.5898)
            ),
            Store.objects.create(
                name="Orgánico y Sano",
                rut="76123467-2",
                storetype=store_types['nat'],
                emailowner=owners[1].email,
                ownername=owners[1].name,
                ownerlastname=owners[1].lastname,
                rutowner="12345679-7",
                owner=owners[1],
                openhr=time(9, 30),
                closehr=time(19, 30),
                phone="967890124",
                address="Av. Portales 1567, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7078, -33.5878)
            ),
            Store.objects.create(
                name="Vida Verde",
                rut="76123468-0",
                storetype=store_types['nat'],
                emailowner=owners[2].email,
                ownername=owners[2].name,
                ownerlastname=owners[2].lastname,
                rutowner="12345680-0",
                owner=owners[2],
                openhr=time(10, 0),
                closehr=time(21, 0),
                phone="967890125",
                address="Av. Freire 1234, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7034, -33.5885)
            ),
            Store.objects.create(
                name="Salud Natural",
                rut="76123469-9",
                storetype=store_types['nat'],
                emailowner=owners[3].email,
                ownername=owners[3].name,
                ownerlastname=owners[3].lastname,
                rutowner="12345681-8",
                owner=owners[3],
                openhr=time(9, 0),
                closehr=time(20, 0),
                phone="967890126",
                address="Av. Los Morros 4120, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.6823, -33.6034)
            ),
            Store.objects.create(
                name="Bio Market",
                rut="76123470-2",
                storetype=store_types['nat'],
                emailowner=owners[4].email,
                ownername=owners[4].name,
                ownerlastname=owners[4].lastname,
                rutowner="12345682-6",
                owner=owners[4],
                openhr=time(10, 30),
                closehr=time(19, 0),
                phone="967890127",
                address="Av. Colón 1345, San Bernardo",
                region=region_rm,
                state=san_bernardo,
                gps=Point(-70.7020, -33.5932)
            ),
        ]

        print("Creando Estado de productos...")
        productState.objects.create(id=1, name="Abierto", description="El envase ha sido abierto y el producto está en uso")
        productState.objects.create(id=2, name="A punto de expirar", description="El producto está dentro del período cercano a su fecha de expiración")
        productState.objects.create(id=3, name="Cerrado", description="El producto está sellado y sin uso")
        productState.objects.create(id=4, name="En buen estado", description="El producto está apto para consumo sin signos de deterioro")
        productState.objects.create(id=5, name="Deteriorado", description="El producto presenta signos de daño o mala conservación")
        productState.objects.create(id=99, name="Vendido", description="El producto ha sido Vendido.")

        product_states = {}
        for ps in productState.objects.all():
            product_states[ps.name.lower()] = ps

        print("Creando Productos...")
        today = timezone.now().date()
        products = []

        # Definir productos por tienda
        product_definitions = [
            # Panadería Don Pan (store 0)
            {"name": "Marraqueta (unidad)", "desc": "Pan tradicional chileno, fresco del día", "days": 1, "qty": 80, "price": 150, "store": 0},
            {"name": "Hallulla (unidad)", "desc": "Pan redondo tradicional", "days": 1, "qty": 60, "price": 200, "store": 0},
            {"name": "Pan de Molde Integral", "desc": "Pan de molde integral, 500g", "days": 5, "qty": 30, "price": 1490, "store": 0, "sale": 1190},
            {"name": "Dobladitas (6 unidades)", "desc": "Pan dulce tradicional", "days": 2, "qty": 40, "price": 1200, "store": 0},
            {"name": "Empanadas de Queso (6 unidades)", "desc": "Empanadas caseras de queso", "days": 2, "qty": 15, "price": 3500, "store": 0, "sale": 2800},
            {"name": "Torta de Chocolate", "desc": "Torta de chocolate casera, 1kg", "days": 3, "qty": 5, "price": 8990, "store": 0},
            {"name": "Coliza (unidad)", "desc": "Pan dulce con manjar", "days": 2, "qty": 25, "price": 600, "store": 0},
            
            # Panadería El Horno Dorado (store 1)
            {"name": "Pan Amasado (unidad)", "desc": "Pan amasado artesanal", "days": 1, "qty": 50, "price": 300, "store": 1},
            {"name": "Sopaipillas (6 unidades)", "desc": "Sopaipillas recién hechas", "days": 1, "qty": 30, "price": 1500, "store": 1},
            {"name": "Kuchen de Manzana", "desc": "Kuchen alemán de manzana", "days": 4, "qty": 8, "price": 6990, "store": 1},
            {"name": "Alfajores (4 unidades)", "desc": "Alfajores con manjar", "days": 7, "qty": 20, "price": 2500, "store": 1, "sale": 1990},
            {"name": "Pan de Pascua", "desc": "Pan de pascua tradicional", "days": 30, "qty": 10, "price": 4990, "store": 1},
            {"name": "Berlines (6 unidades)", "desc": "Berlines con crema", "days": 1, "qty": 35, "price": 2800, "store": 1},
            
            # Panadería Artesanal (store 2)
            {"name": "Pan Integral Centeno", "desc": "Pan integral de centeno", "days": 3, "qty": 25, "price": 1890, "store": 2},
            {"name": "Baguette", "desc": "Baguette francesa", "days": 1, "qty": 40, "price": 1200, "store": 2},
            {"name": "Pan Ciabatta", "desc": "Pan ciabatta italiano", "days": 2, "qty": 20, "price": 1590, "store": 2},
            {"name": "Medialunas (6 unidades)", "desc": "Medialunas de mantequilla", "days": 1, "qty": 50, "price": 2200, "store": 2},
            {"name": "Queque Inglés", "desc": "Queque inglés tradicional", "days": 7, "qty": 12, "price": 3990, "store": 2},
            
            # Café Aroma (store 3)
            {"name": "Café Americano", "desc": "Café americano 250ml", "days": 1, "qty": 100, "price": 1500, "store": 3},
            {"name": "Café Latte", "desc": "Café latte 350ml", "days": 1, "qty": 100, "price": 2500, "store": 3},
            {"name": "Capuccino", "desc": "Capuccino 300ml", "days": 1, "qty": 100, "price": 2800, "store": 3},
            {"name": "Croissant", "desc": "Croissant de mantequilla", "days": 1, "qty": 40, "price": 1800, "store": 3},
            {"name": "Brownie", "desc": "Brownie de chocolate", "days": 3, "qty": 25, "price": 2200, "store": 3},
            {"name": "Sandwich de Pollo", "desc": "Sandwich de pollo con vegetales", "days": 1, "qty": 20, "price": 4500, "store": 3},
            {"name": "Muffin Chocolate", "desc": "Muffin de chocolate", "days": 2, "qty": 30, "price": 1900, "store": 3},
            
            # Café Express (store 4)
            {"name": "Expresso", "desc": "Café expresso 60ml", "days": 1, "qty": 150, "price": 1200, "store": 4},
            {"name": "Muffin de Arándanos", "desc": "Muffin con arándanos", "days": 2, "qty": 30, "price": 1900, "store": 4},
            {"name": "Té Verde", "desc": "Té verde 300ml", "days": 1, "qty": 80, "price": 1500, "store": 4},
            {"name": "Jugo Natural Naranja", "desc": "Jugo natural de naranja 400ml", "days": 1, "qty": 50, "price": 2500, "store": 4},
            {"name": "Tostadas con Palta", "desc": "Tostadas con palta y huevo", "days": 1, "qty": 25, "price": 3990, "store": 4},
            
            # Café del Centro (store 5)
            {"name": "Café Moka", "desc": "Café moka con chocolate", "days": 1, "qty": 80, "price": 3200, "store": 5},
            {"name": "Té Chai Latte", "desc": "Té chai latte 350ml", "days": 1, "qty": 60, "price": 2900, "store": 5},
            {"name": "Cheesecake", "desc": "Cheesecake de frutos rojos", "days": 3, "qty": 15, "price": 3500, "store": 5},
            {"name": "Panini Jamón y Queso", "desc": "Panini caliente", "days": 1, "qty": 30, "price": 4200, "store": 5},
            {"name": "Cookies (3 unidades)", "desc": "Cookies de chocolate", "days": 5, "qty": 40, "price": 2500, "store": 5},
            
            # Verdulería Fresh (store 6)
            {"name": "Tomates (1kg)", "desc": "Tomates frescos", "days": 5, "qty": 40, "price": 1990, "store": 6},
            {"name": "Lechuga (unidad)", "desc": "Lechuga fresca", "days": 4, "qty": 30, "price": 990, "store": 6},
            {"name": "Manzanas (1kg)", "desc": "Manzanas rojas premium", "days": 10, "qty": 50, "price": 2490, "store": 6, "sale": 1990},
            {"name": "Plátanos (1kg)", "desc": "Plátanos maduros", "days": 3, "qty": 20, "price": 1490, "store": 6, "sale": 990},
            {"name": "Papas (1kg)", "desc": "Papas blancas", "days": 15, "qty": 60, "price": 1290, "store": 6},
            {"name": "Cebollas (1kg)", "desc": "Cebollas blancas", "days": 20, "qty": 45, "price": 990, "store": 6},
            {"name": "Pimentones (1kg)", "desc": "Pimentones verdes", "days": 7, "qty": 25, "price": 2990, "store": 6},
            {"name": "Zanahorias (1kg)", "desc": "Zanahorias frescas", "days": 10, "qty": 35, "price": 1490, "store": 6},
            
            # Frutería El Huerto (store 7)
            {"name": "Naranjas (1kg)", "desc": "Naranjas para jugo", "days": 7, "qty": 50, "price": 1790, "store": 7},
            {"name": "Peras (1kg)", "desc": "Peras chilenas", "days": 10, "qty": 40, "price": 2290, "store": 7},
            {"name": "Uvas (1kg)", "desc": "Uvas verdes sin semilla", "days": 5, "qty": 30, "price": 3990, "store": 7, "sale": 2990},
            {"name": "Sandía (unidad)", "desc": "Sandía entera", "days": 7, "qty": 15, "price": 4990, "store": 7},
            {"name": "Frutillas (500g)", "desc": "Frutillas frescas", "days": 3, "qty": 20, "price": 2990, "store": 7},
            {"name": "Limones (1kg)", "desc": "Limones de pica", "days": 15, "qty": 35, "price": 1990, "store": 7},
            {"name": "Melón (unidad)", "desc": "Melón calameño", "days": 7, "qty": 18, "price": 3990, "store": 7},
            
            # Frutería La Cosecha (store 8)
            {"name": "Kiwis (1kg)", "desc": "Kiwis verdes", "days": 10, "qty": 30, "price": 2990, "store": 8},
            {"name": "Duraznos (1kg)", "desc": "Duraznos de temporada", "days": 5, "qty": 25, "price": 2790, "store": 8},
            {"name": "Ciruelas (1kg)", "desc": "Ciruelas rojas", "days": 5, "qty": 20, "price": 2490, "store": 8},
            {"name": "Choclos (4 unidades)", "desc": "Choclos tiernos", "days": 3, "qty": 40, "price": 1990, "store": 8},
            {"name": "Apio (atado)", "desc": "Apio fresco", "days": 7, "qty": 25, "price": 1290, "store": 8},
            {"name": "Brócoli (unidad)", "desc": "Brócoli fresco", "days": 5, "qty": 30, "price": 1790, "store": 8},
            
            # Verduras Frescas (store 9)
            {"name": "Pepinos (1kg)", "desc": "Pepinos verdes", "days": 7, "qty": 35, "price": 1490, "store": 9},
            {"name": "Repollo (unidad)", "desc": "Repollo blanco", "days": 10, "qty": 20, "price": 1290, "store": 9},
            {"name": "Betarragas (1kg)", "desc": "Betarragas cocidas", "days": 15, "qty": 25, "price": 1990, "store": 9},
            {"name": "Ajo (500g)", "desc": "Ajo chileno", "days": 30, "qty": 40, "price": 2490, "store": 9},
            {"name": "Cilantro (atado)", "desc": "Cilantro fresco", "days": 3, "qty": 50, "price": 590, "store": 9},
            {"name": "Perejil (atado)", "desc": "Perejil fresco", "days": 3, "qty": 45, "price": 590, "store": 9},
            
            # Natural Life (store 10)
            {"name": "Quinoa Orgánica (500g)", "desc": "Quinoa orgánica certificada", "days": 365, "qty": 40, "price": 4990, "store": 10},
            {"name": "Leche de Almendras (1L)", "desc": "Bebida de almendras sin azúcar", "days": 90, "qty": 30, "price": 3990, "store": 10},
            {"name": "Aceite de Coco (500ml)", "desc": "Aceite de coco virgen", "days": 730, "qty": 25, "price": 6990, "store": 10},
            {"name": "Granola Artesanal (500g)", "desc": "Granola con frutos secos", "days": 180, "qty": 35, "price": 4990, "store": 10},
            {"name": "Té Matcha (100g)", "desc": "Té matcha japonés", "days": 365, "qty": 20, "price": 8990, "store": 10},
            {"name": "Barritas Energéticas (6 unidades)", "desc": "Barritas de frutos secos", "days": 180, "qty": 45, "price": 3990, "store": 10},
            
            # Orgánico y Sano (store 11)
            {"name": "Miel Orgánica (500g)", "desc": "Miel de abeja orgánica", "days": 730, "qty": 30, "price": 7990, "store": 11},
            {"name": "Chía (500g)", "desc": "Semillas de chía", "days": 365, "qty": 40, "price": 3990, "store": 11},
            {"name": "Pasta Integral (500g)", "desc": "Pasta integral de trigo", "days": 365, "qty": 45, "price": 2990, "store": 11},
            {"name": "Barras de Cereal (6 unidades)", "desc": "Barras energéticas", "days": 180, "qty": 50, "price": 3490, "store": 11},
            {"name": "Mantequilla de Maní (500g)", "desc": "Mantequilla de maní natural", "days": 365, "qty": 30, "price": 4990, "store": 11},
            {"name": "Linaza Molida (500g)", "desc": "Linaza molida orgánica", "days": 180, "qty": 35, "price": 2990, "store": 11},
            
            # Vida Verde (store 12)
            {"name": "Avena Integral (1kg)", "desc": "Avena sin procesar", "days": 365, "qty": 50, "price": 2490, "store": 12},
            {"name": "Arroz Integral (1kg)", "desc": "Arroz integral orgánico", "days": 365, "qty": 45, "price": 2790, "store": 12},
            {"name": "Lentejas Orgánicas (500g)", "desc": "Lentejas orgánicas", "days": 365, "qty": 40, "price": 1990, "store": 12},
            {"name": "Garbanzos (500g)", "desc": "Garbanzos secos", "days": 365, "qty": 35, "price": 1790, "store": 12},
            {"name": "Almendras (250g)", "desc": "Almendras naturales", "days": 180, "qty": 30, "price": 4990, "store": 12},
            {"name": "Nueces (250g)", "desc": "Nueces sin sal", "days": 180, "qty": 28, "price": 5490, "store": 12},
            
            # Salud Natural (store 13)
            {"name": "Proteína Vegana (500g)", "desc": "Proteína de arveja", "days": 365, "qty": 25, "price": 12990, "store": 13},
            {"name": "Spirulina en Polvo (100g)", "desc": "Spirulina orgánica", "days": 365, "qty": 20, "price": 8990, "store": 13},
            {"name": "Cúrcuma en Polvo (100g)", "desc": "Cúrcuma orgánica", "days": 365, "qty": 30, "price": 3990, "store": 13},
            {"name": "Jengibre en Polvo (100g)", "desc": "Jengibre orgánico", "days": 365, "qty": 35, "price": 2990, "store": 13},
            {"name": "Cacao Puro (250g)", "desc": "Cacao en polvo 100%", "days": 365, "qty": 28, "price": 5990, "store": 13},
            
            # Bio Market (store 14)
            {"name": "Pan Sin Gluten", "desc": "Pan sin gluten 400g", "days": 7, "qty": 20, "price": 3990, "store": 14},
            {"name": "Leche de Coco (1L)", "desc": "Bebida de coco", "days": 90, "qty": 25, "price": 4490, "store": 14},
            {"name": "Tofu Natural (300g)", "desc": "Tofu orgánico", "days": 15, "qty": 18, "price": 2990, "store": 14},
            {"name": "Tempeh (200g)", "desc": "Tempeh de soja fermentada", "days": 20, "qty": 15, "price": 3490, "store": 14},
            {"name": "Kombucha (500ml)", "desc": "Kombucha de jengibre", "days": 30, "qty": 30, "price": 2990, "store": 14},
            {"name": "Snacks de Kale (50g)", "desc": "Chips de kale horneado", "days": 90, "qty": 40, "price": 2490, "store": 14},
        ]

        # Crear productos
        default_state = product_states.get('en buen estado') or list(product_states.values())[0]
        
        for prod_def in product_definitions:
            state = default_state
            if prod_def.get('days', 30) <= 3:
                state = product_states.get('a punto de expirar') or default_state
            
            product = Products.objects.create(
                name=prod_def['name'],
                desc=prod_def['desc'],
                expdate=today + timedelta(days=prod_def.get('days', 30)),
                quantity=prod_def['qty'],
                state=state,
                price=prod_def['price'],
                store=stores[prod_def['store']],
                is_sale='sale' in prod_def,
                sale_price=prod_def.get('sale', 0) if 'sale' in prod_def else 0
            )
            products.append(product)

        print("Creando Órdenes...")
        
        # Crear órdenes variadas
        payment_methods = ["Tarjeta de Credito", "Tarjeta de Debito", "Efectivo"]
        payment_statuses = ['paid', 'pending', 'failed']
        payment_scenarios = ['success', 'insufficient_funds', 'declined', '']
        
        orders_created = 0
        
        # Crear 40 órdenes con diferentes características
        for i in range(40):
            # Seleccionar cliente aleatorio
            customer = random.choice(customers)
            
            # Seleccionar productos aleatorios (entre 1 y 5 productos por orden)
            num_items = random.randint(1, 5)
            selected_products = random.sample(products, min(num_items, len(products)))
            
            # Calcular total
            total = 0
            order_items = []
            
            for prod in selected_products:
                quantity = random.randint(1, 3)
                price = prod.sale_price if prod.is_sale else prod.price
                total += price * quantity
                order_items.append({
                    'product': prod,
                    'quantity': quantity,
                    'price': price,
                    'isPicked': random.choice([True, False])
                })
            
            # Determinar estado de pago
            if i < 25:  # 25 órdenes pagadas
                status = 'paid'
                scenario = 'success'
            elif i < 35:  # 10 órdenes pendientes
                status = 'pending'
                scenario = ''
            else:  # 5 órdenes fallidas
                status = 'failed'
                scenario = random.choice(['insufficient_funds', 'declined'])
            
            # Crear orden
            order = Order.objects.create(
                user=customer,
                total=total,
                paymentStatus=status,
                paymentMethod=random.choice(payment_methods),
                paymentScenario=scenario
            )
            
            # Crear items de la orden
            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['price'],
                    isPicked=item['isPicked']
                )
            
            orders_created += 1

        print("Almacenando Tarjetas de crédito...")
        TestCards.objects.create(number="4000 0000 0000 0001", expirydate="09/29", cvv="123", scenario="success")
        TestCards.objects.create(number="4000 0000 0000 0002", expirydate="09/29", cvv="123", scenario="insufficient_funds")
        TestCards.objects.create(number="4000 0000 0000 0003", expirydate="09/29", cvv="123", scenario="declined")
        TestCards.objects.create(number="4000 0000 0000 0004", expirydate="09/29", cvv="123", scenario="expired_card")
        TestCards.objects.create(number="4000 0000 0000 0005", expirydate="09/29", cvv="123", scenario="invalid_card")
        TestCards.objects.create(number="4000 0000 0000 0006", expirydate="09/29", cvv="123", scenario="processing_error")

        print("\n" + "="*70)
        print("✅ DATOS DE PRUEBA GENERADOS EXITOSAMENTE")
        print("="*70)
        
        print("\n🔐 CREDENCIALES DE USUARIOS:")
        print("-" * 70)
        
        print("\n👥 DUEÑOS DE TIENDAS:")
        for cred in user_credentials:
            if cred['type'] == 'Dueño':
                print(f"  📧 {cred['email']:35} 🔑 {cred['password']}")
        
        print("\n👤 CLIENTES:")
        for cred in user_credentials:
            if cred['type'] == 'Usuario':
                print(f"  📧 {cred['email']:35} 🔑 {cred['password']}")

        print("\n" + "-" * 70)
        print("\n💳 TARJETAS DE PRUEBA:")
        print("-" * 70)
        for card in TestCards.objects.all():
            print(f"  {card.number} | Exp: {card.expirydate} | CVV: {card.cvv} | {card.scenario}")

        print("\n" + "-" * 70)
        print("\n📊 RESUMEN DE DATOS GENERADOS:")
        print("-" * 70)
        print(f"  🌎 Regiones:             {Region.objects.count()}")
        print(f"  🏘️  Comunas:              {State.objects.count()}")
        print(f"  👥 Tipos de Usuario:     {userType.objects.count()}")
        print(f"  👤 Usuarios Totales:     {Users.objects.count()}")
        print(f"     - Dueños:             {Users.objects.filter(usertype__id=2).count()}")
        print(f"     - Clientes:           {Users.objects.filter(usertype__id=1).count()}")
        print(f"  🏪 Tipos de Tienda:      {StoreType.objects.count()}")
        print(f"  🏬 Tiendas Creadas:      {Store.objects.count()}")
        print(f"  📦 Estados de Producto:  {productState.objects.count()}")
        print(f"  🛍️  Productos Totales:    {Products.objects.count()}")
        print(f"     - En oferta:          {Products.objects.filter(is_sale=True).count()}")
        print(f"  🧾 Órdenes Creadas:      {Order.objects.count()}")
        print(f"     - Pagadas:            {Order.objects.filter(paymentStatus='paid').count()}")
        print(f"     - Pendientes:         {Order.objects.filter(paymentStatus='pending').count()}")
        print(f"     - Fallidas:           {Order.objects.filter(paymentStatus='failed').count()}")
        print(f"  📋 Items de Orden:       {OrderItem.objects.count()}")
        print(f"  💳 Tarjetas de Prueba:   {TestCards.objects.count()}")
        
        print("\n" + "="*70)
        print("🎉 Base de datos poblada completamente")
        print("="*70)
        print("\n💡 Para ejecutar: python manage.py generate_test_data_extended")
        print("\n")