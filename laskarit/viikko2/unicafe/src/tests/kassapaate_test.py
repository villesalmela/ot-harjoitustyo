import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self) -> None:
        self.kassapaate = Kassapaate()

    def test_oikea_aloitusraha(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_oikea_lounasmaara(self):
        self.assertEqual(self.kassapaate.edulliset + self.kassapaate.maukkaat, 0)

    def test_kateinen_edullinen_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(300), 60)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateinen_edullinen_ei_riittava(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100), 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateinen_maukas_riittava(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(1000), 600)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateinen_maukas_ei_riittava(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(100), 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kortti_edullinen_riittava(self):
        kortti = Maksukortti(1000)
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(kortti))
        self.assertEqual(kortti.saldo, 760)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kortti_edullinen_ei_riittava(self):
        kortti = Maksukortti(100)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(kortti))
        self.assertEqual(kortti.saldo, 100)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kortti_maukas_riittava(self):
        kortti = Maksukortti(1000)
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(kortti.saldo, 600)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kortti_maukas_ei_riittava(self):
        kortti = Maksukortti(100)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(kortti.saldo, 100)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kortti_lataa(self):
        kortti = Maksukortti(100)
        self.kassapaate.lataa_rahaa_kortille(kortti, 100)
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_kortti_lataa_neg(self):
        kortti = Maksukortti(100)
        self.kassapaate.lataa_rahaa_kortille(kortti, -100)
        self.assertEqual(kortti.saldo, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassa_saldo(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)