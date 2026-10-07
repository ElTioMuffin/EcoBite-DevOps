# yourapp/management/commands/attach_pexels_images.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from Store.models import Store, Products
import requests
import time
import os

class Command(BaseCommand):
    help = 'Download and attach real images from Pexels API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-key',
            type=str,
            help='Pexels API key (get free at https://www.pexels.com/api/)',
            default=os.environ.get('PEXELS_API_KEY', '')
        )
        parser.add_argument(
            '--stores-only',
            action='store_true',
            help='Only download images for stores',
        )
        parser.add_argument(
            '--products-only',
            action='store_true',
            help='Only download images for products',
        )

    def handle(self, *args, **options):
        api_key = options['api_key']
        
        if not api_key:
            self.stdout.write(self.style.ERROR(
                '❌ Error: Se requiere una API key de Pexels\n'
                '   Obtén una gratis en: https://www.pexels.com/api/\n'
                '   Uso: python manage.py attach_pexels_images --api-key YOUR_KEY\n'
                '   O configura: export PEXELS_API_KEY=your_key'
            ))
            return
        
        self.api_key = api_key
        self.headers = {'Authorization': api_key}
        
        stores_only = options.get('stores_only', False)
        products_only = options.get('products_only', False)
        
        if not products_only:
            self.stdout.write(self.style.WARNING('\n📸 Descargando imágenes para tiendas...'))
            self.attach_store_images()
        
        if not stores_only:
            self.stdout.write(self.style.WARNING('\n🛍️  Descargando imágenes para productos...'))
            self.attach_product_images()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Proceso completado exitosamente!'))

    def search_pexels(self, query, per_page=1):
        """Search Pexels for images"""
        url = 'https://api.pexels.com/v1/search'
        params = {
            'query': query,
            'per_page': per_page,
            'orientation': 'landscape'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['photos']:
                    # Return medium quality image URL
                    return data['photos'][0]['src']['large']
            return None
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  ⚠️  Error en búsqueda: {str(e)}'))
            return None

    def download_image(self, url, retries=3):
        """Download image with retry logic"""
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    return response.content
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Intento {attempt + 1} error: {str(e)}'))
            time.sleep(1)
        return None

    def attach_store_images(self):
        """Attach images to stores"""
        store_queries = {
            'CAF': 'coffee shop interior',
            'PAN': 'bakery bread display',
            'FRU': 'fruit vegetable market',
            'NAT': 'organic health food store',
        }
        
        stores = Store.objects.filter(logo__isnull=True) | Store.objects.filter(logo='')
        total = stores.count()
        
        self.stdout.write(f'  📊 Total tiendas sin imagen: {total}')
        
        for index, store in enumerate(stores, 1):
            store_type = store.storetype.categorycode
            query = store_queries.get(store_type, 'store front')
            
            self.stdout.write(f'  [{index}/{total}] {store.name}... (buscando: {query})')
            
            # Search for image
            image_url = self.search_pexels(query)
            
            if image_url:
                # Download image
                image_data = self.download_image(image_url)
                
                if image_data:
                    filename = f'store_logo_{store.id}_{store_type.lower()}.jpg'
                    store.logo.save(filename, ContentFile(image_data), save=True)
                    self.stdout.write(self.style.SUCCESS(f'    ✅ Imagen guardada'))
                else:
                    self.stdout.write(self.style.ERROR(f'    ❌ Error descargando imagen'))
            else:
                self.stdout.write(self.style.ERROR(f'    ❌ No se encontró imagen'))
            
            time.sleep(1)  # Respect API rate limits

    def attach_product_images(self):
        """Attach images to products"""
        
        product_queries = {
            # Panadería
            'marraqueta': 'french bread',
            'hallulla': 'round bread',
            'pan de molde': 'sliced bread loaf',
            'dobladitas': 'sweet pastry',
            'empanadas': 'empanada',
            'torta': 'chocolate cake slice',
            'coliza': 'cream pastry',
            'pan amasado': 'artisan bread',
            'sopaipillas': 'fried pastry',
            'kuchen': 'apple pie',
            'alfajores': 'sandwich cookie',
            'pan de pascua': 'fruitcake',
            'berlines': 'cream filled donut',
            'pan integral': 'whole wheat bread',
            'baguette': 'french baguette',
            'ciabatta': 'ciabatta bread',
            'medialunas': 'croissant',
            'queque': 'pound cake',
            
            # Café
            'café americano': 'americano coffee cup',
            'café latte': 'latte coffee art',
            'capuccino': 'cappuccino coffee',
            'croissant': 'butter croissant',
            'brownie': 'chocolate brownie',
            'sandwich': 'fresh sandwich',
            'muffin': 'blueberry muffin',
            'expresso': 'espresso shot',
            'té verde': 'green tea cup',
            'jugo': 'fresh orange juice',
            'tostadas': 'avocado toast',
            'café moka': 'mocha coffee',
            'té chai': 'chai latte',
            'cheesecake': 'cheesecake slice',
            'panini': 'grilled panini',
            'cookies': 'chocolate chip cookies',
            
            # Frutas y Verduras
            'tomates': 'fresh red tomatoes',
            'lechuga': 'green lettuce',
            'manzanas': 'red apples',
            'plátanos': 'yellow bananas',
            'papas': 'potatoes',
            'cebollas': 'onions',
            'pimentones': 'bell peppers',
            'zanahorias': 'fresh carrots',
            'naranjas': 'oranges',
            'peras': 'pears',
            'uvas': 'green grapes',
            'sandía': 'watermelon',
            'frutillas': 'strawberries',
            'limones': 'lemons',
            'melón': 'cantaloupe melon',
            'kiwis': 'kiwi fruit',
            'duraznos': 'peaches',
            'ciruelas': 'plums',
            'choclos': 'corn cob',
            'apio': 'celery stalks',
            'brócoli': 'broccoli',
            'pepinos': 'cucumbers',
            'repollo': 'cabbage',
            'betarragas': 'beets',
            'ajo': 'garlic cloves',
            'cilantro': 'fresh cilantro',
            'perejil': 'parsley',
            
            # Productos Naturales
            'quinoa': 'quinoa grain bowl',
            'leche de almendras': 'almond milk',
            'aceite de coco': 'coconut oil jar',
            'granola': 'granola bowl',
            'té matcha': 'matcha green tea powder',
            'barritas energéticas': 'energy bars',
            'miel': 'honey jar',
            'chía': 'chia seeds',
            'pasta integral': 'whole wheat pasta',
            'barras de cereal': 'granola bars',
            'mantequilla de maní': 'peanut butter jar',
            'linaza': 'flax seeds',
            'avena': 'oatmeal',
            'arroz integral': 'brown rice',
            'lentejas': 'lentils',
            'garbanzos': 'chickpeas',
            'almendras': 'almonds',
            'nueces': 'walnuts',
            'proteína': 'protein powder',
            'spirulina': 'spirulina powder',
            'cúrcuma': 'turmeric powder',
            'jengibre': 'fresh ginger',
            'cacao': 'cocoa powder',
            'pan sin gluten': 'gluten free bread',
            'leche de coco': 'coconut milk',
            'tofu': 'tofu block',
            'tempeh': 'tempeh',
            'kombucha': 'kombucha bottle',
            'snacks de kale': 'kale chips',
        }
        
        products = Products.objects.filter(photo__isnull=True) | Products.objects.filter(photo='')
        total = products.count()
        
        self.stdout.write(f'  📊 Total productos sin imagen: {total}')
        
        for index, product in enumerate(products, 1):
            # Find matching query
            query = 'fresh food'
            product_name_lower = product.name.lower()
            
            for keyword, search_term in product_queries.items():
                if keyword in product_name_lower:
                    query = search_term
                    break
            
            self.stdout.write(f'  [{index}/{total}] {product.name[:40]}...')
            
            # Search for image
            image_url = self.search_pexels(query)
            
            if image_url:
                image_data = self.download_image(image_url)
                
                if image_data:
                    clean_name = ''.join(c for c in product.name[:30] if c.isalnum() or c in (' ', '-', '_'))
                    clean_name = clean_name.replace(' ', '_')
                    filename = f'product_{product.id}_{clean_name}.jpg'
                    
                    product.photo.save(filename, ContentFile(image_data), save=True)
                    self.stdout.write(self.style.SUCCESS(f'    ✅ OK'))
                else:
                    self.stdout.write(self.style.ERROR(f'    ❌ Error descarga'))
            else:
                self.stdout.write(self.style.ERROR(f'    ❌ No encontrada'))
            
            # Rate limiting
            if index % 15 == 0:
                self.stdout.write(self.style.WARNING(f'  ⏸️  Pausa (15 descargas)...'))
                time.sleep(3)
            else:
                time.sleep(0.8)  # Pexels allows 200 requests/hour