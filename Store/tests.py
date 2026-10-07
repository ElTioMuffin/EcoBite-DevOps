from django.test import SimpleTestCase
from Store.models import Region, State, Store, Products, Order


class StoreModelContractTests(SimpleTestCase):
    def test_store_models_are_registered(self):
        self.assertEqual(Region._meta.model_name, "region")
        self.assertEqual(State._meta.model_name, "state")
        self.assertEqual(Store._meta.model_name, "store")
        self.assertEqual(Products._meta.model_name, "products")

    def test_order_uses_uuid_primary_key(self):
        self.assertTrue(Order._meta.get_field("id").primary_key)
        self.assertEqual(Order._meta.get_field("id").get_internal_type(), "UUIDField")
