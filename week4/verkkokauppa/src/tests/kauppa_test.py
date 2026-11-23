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
        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

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
