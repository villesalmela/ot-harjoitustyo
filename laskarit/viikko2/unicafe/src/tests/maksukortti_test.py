import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 15.0)

    def test_saldo_vahenee_oikein_jos_rahaa_tarpeeksi(self):
        self.assertTrue(self.maksukortti.ota_rahaa(500))
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)

    def test_saldo_ei_muutu_jos_rahaa_ei_tarpeeksi(self):
        self.assertFalse(self.maksukortti.ota_rahaa(1500))
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_saldo_tulostuu_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")