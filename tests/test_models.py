######################################################################
# Test Cases for Product Model
######################################################################

import logging
from unittest import TestCase
from service.models import Product, DataValidationError
from .factories import ProductFactory

from service import app
from service.models import db

DATABASE_URI = "sqlite:///:memory:"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductModel(TestCase):
    """ Test Cases for Product Model """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)

    def setUp(self):
        """ Run before each test """
        db.create_all()

    def tearDown(self):
        """ Run after each test """
        db.session.remove()
        db.drop_all()

    ######################################################################
    # READ
    ######################################################################
    def test_read_a_product(self):
        """ It should Read a Product """
        product = ProductFactory()
        logging.debug(product)

        product.id = None
        product.create()

        self.assertIsNotNone(product.id)

        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    ######################################################################
    # UPDATE
    ######################################################################
    def test_update_a_product(self):
        """ It should Update a Product """
        product = ProductFactory()
        product.id = None
        product.create()

        self.assertIsNotNone(product.id)

        product.description = "Updated Description"
        product.update()

        found_product = Product.find(product.id)
        self.assertEqual(found_product.description, "Updated Description")

        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, product.id)

    ######################################################################
    # DELETE
    ######################################################################
    def test_delete_a_product(self):
        """ It should Delete a Product """
        product = ProductFactory()
        product.create()

        self.assertEqual(len(Product.all()), 1)

        product.delete()
        self.assertEqual(len(Product.all()), 0)

    ######################################################################
    # LIST ALL
    ######################################################################
    def test_list_all_products(self):
        """ It should List all Products """
        self.assertEqual(len(Product.all()), 0)

        for _ in range(5):
            product = ProductFactory()
            product.create()

        products = Product.all()
        self.assertEqual(len(products), 5)

    ######################################################################
    # FIND BY NAME
    ######################################################################
    def test_find_by_name(self):
        """ It should Find Products by Name """
        products = ProductFactory.create_batch(5)

        for product in products:
            product.create()

        name = products[0].name
        count = len([p for p in products if p.name == name])

        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)

        for product in found:
            self.assertEqual(product.name, name)

    ######################################################################
    # FIND BY CATEGORY
    ######################################################################
    def test_find_by_category(self):
        """ It should Find Products by Category """
        products = ProductFactory.create_batch(10)

        for product in products:
            product.create()

        category = products[0].category
        count = len([p for p in products if p.category == category])

        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)

        for product in found:
            self.assertEqual(product.category, category)

    ######################################################################
    # FIND BY AVAILABILITY
    ######################################################################
    def test_find_by_availability(self):
        """ It should Find Products by Availability """
        products = ProductFactory.create_batch(10)

        for product in products:
            product.create()

        availability = products[0].available
        count = len([p for p in products if p.available == availability])

        found = Product.find_by_availability(availability)
        self.assertEqual(found.count(), count)

        for product in found:
            self.assertEqual(product.available, availability)
