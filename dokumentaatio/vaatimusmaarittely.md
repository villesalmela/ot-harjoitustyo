# Vaatimusmäärittely
## Sovelluksen tarkoitus
Sovellus analysoi annetun PCAP-tiedoston ja tuottaa yhteenvedon tallennetun verkkoliikenteen sisällöstä.
## Käyttäjät
Sovelluksella on vain yhdenlaisia käyttäjiä, joten käyttäjänhallintaa ei toteuteta.
## Perusversion tarjoama toiminnallisuus
- [x] Käyttäjä voi valita analysoitavan tiedoston paikalliselta koneelta käyttäen tiedostonvalitsinta
    - [x] Tiedoston on oltava kooltaan enintään 100 MB
    - [x] Tiedoston on oltava päätteltään ".pcap" tai ".pcapng"
    - [x] Käyttäjälle ilmoitetaan, mikäli tiedoston luku epäonnistuu tai tiedosto ei kelpaa
- [x] Käyttäjä voi tarkastella analyysin tuloksia tekstimuodossa
    - [x] Perustiedot
        - [x] Tallennuksen ajanjakso
        - [x] Pakettien kokonaismäärä
        - [x] Datan kokonaismäärä
    - [x] Yksityiskohdat
        - Kerroksittainen tarkastelu
            - application
            - transport
            - network
            - link
        - Lähde- ja kohdeosoitteet
        - Paketin koko
        - Paketin saapumisaika
        - Kerroksen protokolla
        - Kerroksen koko
        - DNS ja DHCP protokollissa valitut yksityiskohdat

- [x] Käyttäjä voi tyhjentää analyysin ja aloittaa alusta
- [x] Käyttäjä voi tallentaa analyysin
- [x] Käyttäjä voi avata aiemmin tallennettun analyysin
- [x] Käyttäjä voi poistaa aiemmin tallennetun analyysin
- [x] Käyttäjä voi täydentää analyysiä valitsemalla seuraavan tiedoston
- [x] Käyttäjä voi tarkastella analyysin tuloksia erilaisten visualisointien avulla
    - [x] Aluediagrammi: Tiedonsiirron nopeus ajan suhteen
    - [x] Ympyrädiagrammi: Liikenteen jakautuminen protokollittain
- [x] Protokollakohtaiset tiedot
    - [x] DHCP
        - [x] Graafi yleisimmistä DHCP-palvelimista
        - [x] Graafi yleisimmistä verkkotunnuksista
        - [x] Graafi yleisimmistä asiakkaista
    - [x] DNS
        - [x] Graafi yleisimmistä DNS-palvelimista
        - [x] Graafi yleisimmistä verkkotunnuksista

