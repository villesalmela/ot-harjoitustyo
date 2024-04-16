# Ohjelmistotekniikka, harjoitustyö
Harjoitustyönä teen sovelluksen, joka **visualisoi** yhteenvedon verkkoliikenteestä, käyttäen syötteenä _PCAP-tiedostoa_.

## Status
Ohjelma kykenee parsimaan DNS- ja DHCP-paketteja. Tekstimuodossa voi tarkastella tietoa kaikista paketeista,
graafimuodossa tarjolla on yhteenveto yleisimmistä nimistä nimipalvelukyselyissä.

## Dokunentaatio
[Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)  
[Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)  
[Changelog](dokumentaatio/changelog.md)

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

## Peruskäyttö
1. Avaa valitsemasi PCAP-tiedosto
    - Näppäinkomennolla Ctrl+O tai valikosta File -> Open File
    - "assets" kansiossa on pari esimerkkitiedostoa
2. Tarkasta tiedot kummallakin välilehdellä
3. Resetoi ohjelma alkutilanteeseen
    - Näppäinkomennolla Ctrl+R tai valikosta File -> Reset
4. Poistu ohjelmasta
    - Näppäinkomennolla Ctrl+Q tai valikosta File -> Exit