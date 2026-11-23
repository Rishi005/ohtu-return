import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_payment_for_one_product_in_stock(self):
        bank_mock = Mock()
        reference_generator_mock = Mock()
        reference_generator_mock.uusi.return_value = 42

        inventory_mock = Mock()
        inventory_mock.saldo.side_effect = lambda product_id: 10
        inventory_mock.hae_tuote.side_effect = (
            lambda product_id: Tuote(product_id, "milk", 5)
        )

        kauppa = Kauppa(
            inventory_mock, bank_mock, reference_generator_mock
        )

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        bank_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_payment_for_two_different_products_in_stock(self):
        bank_mock = Mock()
        reference_generator_mock = Mock()
        reference_generator_mock.uusi.return_value = 42

        inventory_mock = Mock()
        inventory_mock.saldo.side_effect = lambda product_id: 10
        inventory_mock.hae_tuote.side_effect = lambda product_id: (
            Tuote(1, "milk", 5) if product_id == 1
            else Tuote(2, "bread", 7)
        )

        kauppa = Kauppa(
            inventory_mock, bank_mock, reference_generator_mock
        )

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        bank_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 12
        )

    def test_payment_for_two_of_the_same_product_in_stock(self):
        bank_mock = Mock()
        reference_generator_mock = Mock()
        reference_generator_mock.uusi.return_value = 42

        inventory_mock = Mock()
        inventory_mock.saldo.side_effect = lambda product_id: 10
        inventory_mock.hae_tuote.side_effect = (
            lambda product_id: Tuote(product_id, "milk", 5)
        )

        kauppa = Kauppa(
            inventory_mock, bank_mock, reference_generator_mock
        )

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        bank_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 10
        )

    def test_payment_for_one_in_stock_and_one_out_of_stock_product(self):
        bank_mock = Mock()
        reference_generator_mock = Mock()
        reference_generator_mock.uusi.return_value = 42

        inventory_mock = Mock()
        inventory_mock.saldo.side_effect = lambda product_id: (
            10 if product_id == 1 else 0
        )
        inventory_mock.hae_tuote.side_effect = lambda product_id: (
            Tuote(1, "milk", 5) if product_id == 1
            else Tuote(2, "bread", 7)
        )

        kauppa = Kauppa(
            inventory_mock, bank_mock, reference_generator_mock
        )

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        bank_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )
