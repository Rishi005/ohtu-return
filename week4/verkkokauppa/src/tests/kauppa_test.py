import unittest
from unittest.mock import Mock
from kauppa import Kauppa
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()
        self.kauppa = Kauppa(
            self.varasto_mock,
            self.pankki_mock,
            self.viitegeneraattori_mock,
        )

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        self.varasto_mock.saldo.side_effect = lambda product_id: 10
        self.varasto_mock.hae_tuote.side_effect = (
            lambda product_id: Tuote(1, "maito", 5)
        )

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_payment_for_one_product_in_stock(self):
        self.varasto_mock.saldo.side_effect = lambda product_id: 10
        self.varasto_mock.hae_tuote.side_effect = (
            lambda product_id: Tuote(product_id, "milk", 5)
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_payment_for_two_different_products_in_stock(self):
        self.varasto_mock.saldo.side_effect = lambda product_id: 10
        self.varasto_mock.hae_tuote.side_effect = lambda product_id: (
            Tuote(1, "milk", 5) if product_id == 1
            else Tuote(2, "bread", 7)
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 12
        )

    def test_payment_for_two_of_the_same_product_in_stock(self):
        self.varasto_mock.saldo.side_effect = lambda product_id: 10
        self.varasto_mock.hae_tuote.side_effect = (
            lambda product_id: Tuote(product_id, "milk", 5)
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 10
        )

    def test_payment_for_one_in_stock_and_one_out_of_stock_product(self):
        self.varasto_mock.saldo.side_effect = lambda product_id: (
            10 if product_id == 1 else 0
        )
        self.varasto_mock.hae_tuote.side_effect = lambda product_id: (
            Tuote(1, "milk", 5) if product_id == 1
            else Tuote(2, "bread", 7)
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_aloita_asiointi_resets_previous_purchase_data(self):
        self.varasto_mock.saldo.side_effect = lambda product_id: 10
        self.varasto_mock.hae_tuote.side_effect = lambda product_id: (
            Tuote(1, "milk", 5) if product_id == 1
            else Tuote(2, "bread", 7)
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("first customer", "11111")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("second customer", "22222")

        self.pankki_mock.tilisiirto.assert_called_with(
            "second customer", 42, "22222", "33333-44455", 7
        )

    def test_new_reference_is_requested_for_each_payment(self):
        self.varasto_mock.saldo.side_effect = lambda product_id: 10
        self.varasto_mock.hae_tuote.side_effect = (
            lambda product_id: Tuote(product_id, "product", 5)
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("first customer", "11111")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("second customer", "22222")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_removing_product_from_cart_returns_it_to_inventory(self):
        milk = Tuote(1, "milk", 5)
        bread = Tuote(2, "bread", 7)

        self.varasto_mock.saldo.side_effect = lambda product_id: 10
        self.varasto_mock.hae_tuote.side_effect = lambda product_id: (
            milk if product_id == 1 else bread
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(1)

        self.kauppa.tilimaksu("pekka", "12345")

        self.varasto_mock.palauta_varastoon.assert_called_once_with(milk)
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 7
        )

    def test_product_identity_hash_and_string_representation(self):
        first_milk = Tuote(1, "milk", 5)
        second_milk = Tuote(1, "other milk", 5)
        bread = Tuote(2, "bread", 7)

        self.assertEqual(hash(first_milk), hash(second_milk))
        self.assertEqual(first_milk, second_milk)
        self.assertNotEqual(first_milk, bread)
        self.assertEqual(str(first_milk), "milk")
