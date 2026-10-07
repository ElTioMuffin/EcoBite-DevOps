from django.test import SimpleTestCase


class CartModuleTests(SimpleTestCase):
    def test_cart_module_can_be_imported(self):
        from cart.cart import Cart
        self.assertTrue(callable(Cart))
