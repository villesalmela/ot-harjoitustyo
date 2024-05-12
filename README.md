# Ohjelmistotekniikka, harjoitustyö
Harjoitustyönä teen sovelluksen, joka **visualisoi** yhteenvedon verkkoliikenteestä, käyttäen syötteenä _PCAP-tiedostoa_.

## Status
Ohjelma kykenee parsimaan monenlaisia verkkopaketteja. Tekstimuodossa voi tarkastella tietoa kaikista paketeista,
graafimuodossa tarjolla on tilastoja DNS- ja DHCP liikenteestä. Lisäksi etusivulla on dashboard-tyylisesti muutama numeerinen indikaattori (pakettien määrä, tallennuksen kesto, jne.). Tarkastelemaan pääsee myös liikenteen protokollajakaumaa.

## Dokumentaatio
[Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)  
[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)  
[Changelog](dokumentaatio/changelog.md)  
[Release](https://github.com/villesalmela/ot-harjoitustyo/releases/tag/Viikko5)  
[Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)  
[Käyttöohje](dokumentaatio/käyttöohje.md)
[Testausdokumentti](dokumentaatio/testaus.md)


## Asennus
1. Asenna riippuvuudet komennolla:
```bash
poetry install
```

## Komentorivitoiminnot
### Ohjelman suorittaminen
Ohjelma käynnistyy komennolla:
```bash
poetry run invoke start
```

### Testaus
Testit suoritetaan komennolla:
```bash
poetry run invoke test
```

### Testikattavuus
Testikattavuusraportin voi generoida komennolla:
```bash
poetry run invoke coverage-report
```
Raportti generoituu _htmlcov_-hakemistoon.