from Store.models import Products

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if cart is None:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)

        # If not in cart, initialize it
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }

        # Current quantity in cart
        current_qty = self.cart[product_id]['quantity']

        # Maximum allowed quantity (stock)
        max_qty = product.quantity

        # New quantity cannot exceed stock
        new_qty = min(current_qty + quantity, max_qty)

        # Detect if user hit stock limit
        hit_limit = new_qty == current_qty  

        # Update the cart
        self.cart[product_id]['quantity'] = new_qty
        self.session.modified = True

        return not hit_limit

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_cart(self):
        products = self.cart.keys()

        lookup = Products.objects.filter(id__in=products)

        for product in lookup:
            product_id = str(product.id)

            product.quantity_in_cart = self.cart[product_id]['quantity']

        return lookup
    
    def remove(self,product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

    def clear(self):

        self.cart.clear()
        self.session.modified = True

    def update(self, product_id, quantity):
        product_id = str(product_id)
        
        print(f"[UPDATE] Product ID: {product_id}, Quantity: {quantity}")
        print(f"[UPDATE] Cart before: {self.cart}")
        
        if product_id in self.cart:
            try:
                product = Products.objects.get(id=product_id)
                print(f"[UPDATE] Product found: {product.name}, Stock: {product.quantity}")
                
                # Check if quantity is 0 or negative
                if quantity <= 0:
                    print(f"[UPDATE] Quantity <= 0, removing product")
                    self.remove(product_id)
                    return {'status': 'removed', 'hit_limit': False}
                
                # Ensure quantity doesn't exceed stock
                qty = min(quantity, product.quantity)
                print(f"[UPDATE] Adjusted quantity: {qty}")
                
                # Check if we hit the stock limit
                hit_limit = qty < quantity
                print(f"[UPDATE] Hit limit: {hit_limit}")
                
                # Update the cart
                self.cart[product_id]['quantity'] = qty
                self.session.modified = True
                
                print(f"[UPDATE] Cart after: {self.cart}")
                return {'status': 'updated', 'hit_limit': hit_limit}
                
            except Products.DoesNotExist:
                print(f"[UPDATE] Product not found in database, removing")
                self.remove(product_id)
                return {'status': 'not_found', 'hit_limit': False}
        else:
            print(f"[UPDATE] Product not in cart")
            return {'status': 'not_in_cart', 'hit_limit': False}