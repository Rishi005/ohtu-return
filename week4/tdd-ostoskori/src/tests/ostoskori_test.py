import unittest
from ostoskori import Ostoskori
from tuote import Tuote

class TestOstoskori(unittest.TestCase):
    def setUp(self):
        self.kori = Ostoskori()
        self.maito = Tuote("Maito", 3)
        self.leipa = Tuote("Leipä", 2)

    def test_ostoskorin_hinta_ja_tavaroiden_maara_alussa(self):
        self.assertEqual(self.kori.hinta(), 0)
        self.assertEqual(self.kori.tavaroita_korissa(), 0)

    def test_yhden_tuotteen_lisaamisen_jalkeen_korissa_yksi_tavara(self):
        self.kori.lisaa_tuote(self.maito)
        self.assertEqual(self.kori.tavaroita_korissa(), 1)

    def test_after_adding_one_item_price_of_cart_is_same_as_product_price(self):
        self.kori.lisaa_tuote(self.maito)
        self.assertEqual(self.kori.hinta(), 3)

    def test_adding_two_different_products_cart_has_two_items(self):
        self.kori.lisaa_tuote(self.maito)
        self.kori.lisaa_tuote(self.leipa)
        self.assertEqual(self.kori.tavaroita_korissa(), 2)

    def test_adding_two_different_products_cart_price_is_sum_of_product_prices(self):
        self.kori.lisaa_tuote(self.maito)
        self.kori.lisaa_tuote(self.leipa)
        self.assertEqual(self.kori.hinta(), 5)

    def test_adding_two_same_products_cart_has_two_items(self):
        self.kori.lisaa_tuote(self.maito)
        self.kori.lisaa_tuote(self.maito)
        self.assertEqual(self.kori.tavaroita_korissa(), 2)

    def test_adding_two_same_products_cart_price_is_sum_of_product_prices(self):
        self.kori.lisaa_tuote(self.maito)
        self.kori.lisaa_tuote(self.maito)
        self.assertEqual(self.kori.hinta(), 6)

    def test_after_adding_one_product_cart_contains_one_purchase(self):
        self.kori.lisaa_tuote(self.maito)
        self.assertEqual(len(self.kori.ostokset()), 1)

    def test_after_adding_one_product_purchase_has_name_and_quantity_one(self):
        self.kori.lisaa_tuote(self.maito)
        ostos = self.kori.ostokset()[0]
        self.assertEqual(ostos.tuotteen_nimi(), "Maito")
        self.assertEqual(ostos.lukumaara(), 1)

    def test_after_adding_two_different_products_cart_contains_two_purchases(self):
        self.kori.lisaa_tuote(self.maito)
        self.kori.lisaa_tuote(self.leipa)
        self.assertEqual(len(self.kori.ostokset()), 2)