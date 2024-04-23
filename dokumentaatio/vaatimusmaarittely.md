# Vaatimusmäärittely
## Sovelluksen tarkoitus
Sovellus analysoi annetun PCAP-tiedoston ja tuottaa yhteenvedon tallennetun verkkoliikenteen sisällöstä.
## Käyttäjät
Sovelluksella on vain yhdenlaisia käyttäjiä, joten käyttäjänhallintaa ei toteuteta.
## Perusversion tarjoama toiminnallisuus
- [x] Käyttäjä voi valita analysoitavan tiedoston paikalliselta koneelta käyttäen tiedostonvalitsinta
    - [x] Tiedoston on oltava kooltaan enintään 100 MB
    - [x] Tiedoston on oltava päätteltään ".pcap"
    - [x] Käyttäjälle ilmoitetaan, mikäli tiedoston luku epäonnistuu tai tiedosto ei kelpaa
- [ ] Käyttäjä voi tarkastella analyysin tuloksia tekstimuodossa
    - [ ] Perustiedot
        - [x] Tallennuksen ajanjakso
        - [x] Pakettien kokonaismäärä
        - [x] Datan kokonaismäärä
        - [ ] Osoitteiden kokonaismäärä
        - [ ] Liikenteen jakautuminen protokollittain
    - [ ] Protokollakohtaiset tiedot
        - [ ] DHCP
            - [ ] Lista tunnistetuista DHCP-palvelimista
            - [ ] Lista tunnistetuista reitittimistä
            - [x] Lista tunnistetuista asiakkaista
        - [x] DNS
            - [x] Graafi tunnistetuista DNS-palvelimista
            - [x] Graafi yleisimmistä verkkotunnuksista
        - [ ] HTTP/S
            - [ ] Lista yleisimmistä HTTP-palvelimista
            - [ ] Liikenteen jakautuminen salattuun ja salaamattomaan
- [x] Käyttäjä voi tyhjentää analyysin ja aloittaa alusta
- [ ] Käyttäjä voi tallentaa analyysin
- [ ] Käyttäjä voi avata aiemmin tallennettun analyysin
## Jatkokehitysideoita
- [ ] Käyttäjä voi rajata analyysin koskemaan tiettyjä osoitteita
- [ ] Käyttäjä voi täydentää analyysiä valitsemalla seuraavan tiedoston
- [ ] Käyttäjä voi tarkastella analyysin tuloksia erilaisten visualisointien avulla
    - [x] Aluediagrammi: Tiedonsiirron nopeus ajan suhteen
    - [ ] Ympyrädiagrammi: Liikenteen jakautuminen protokollittain
    - [ ] Verkkokaavio: Sisäverkon laitteiden väliset yhteydet
- [ ] Käyttäjä voi tarkastella tietoturvapoikkeamia
    - [ ] Mahdollinen porttiskannaus
    - [ ] Mahdollinen DNS-tunnelointi
    - [ ] Mahdollinen ARP-väärennös
- [ ] Käyttäjä voi viedä analyysin PDF-muodossa
