# Vaatimusmäärittely
## Sovelluksen tarkoitus
Sovellus analysoi annetun PCAP-tiedoston ja tuottaa yhteenvedon tallennetun verkkoliikenteen sisällöstä.
## Käyttäjät
Sovelluksella on vain yhdenlaisia käyttäjiä, joten käyttäjänhallintaa ei toteuteta.
## Perusversion tarjoama toiminnallisuus
- Käyttäjä voi valita analysoitavan tiedoston paikalliselta koneelta käyttäen tiedostonvalitsinta
    - Tiedoston on oltava kooltaan enintään 100 MB
    - Tiedoston on oltava yhteensopiva libpcap -kirjaston kanssa
    - Käyttäjälle ilmoitetaan, mikäli tiedoston luku epäonnistuu tai tiedosto ei kelpaa
- Käyttäjä voi tarkastella analyysin tuloksia taulukkomuodossa
    - Perustiedot
        - Tallennuksen ajanjakso
        - Pakettien kokonaismäärä
        - Datan kokonaismäärä
        - Osoitteiden kokonaismäärä
        - Liikenteen jakautuminen protokollittain
    - Protokollakohtaiset tiedot
        - DHCP
            - Lista tunnistetuista DHCP-palvelimista
            - Lista tunnistetuista reitittimistä
            - Lista tunnistetuista asiakkaista
        - DNS
            - Lista tunnistetuista DNS-palvelimista
            - Lista yleisimmistä verkkotunnuksista
        - HTTP/S
            - Lista yleisimmistä HTTP-palvelimista
            - Liikenteen jakautuminen salattuun ja salaamattomaan
- Käyttäjä voi tyhjentää analyysin ja aloittaa alusta
- Käyttäjä voi tallentaa analyysin
- Käyttäjä voi avata aiemmin tallennettun analyysin
## Jatkokehitysideoita
- Käyttäjä voi rajata analyysin koskemaan tiettyjä osoitteita
- Käyttäjä voi täydentää analyysiä valitsemalla seuraavan tiedoston
- Käyttäjä voi tarkastella analyysin tuloksia erilaisten visualisointien avulla
    - Viivadiagrammi: Datan määrä ajan suhteen
    - Ympyrädiagrammi: Liikenteen jakautuminen protokollittain
    - Verkkokaavio: Sisäverkon laitteiden väliset yhteydet
- Käyttäjä voi tarkastella tietoturvapoikkeamia
    - Mahdollinen porttiskannaus
    - Mahdollinen DNS-tunnelointi
    - Mahdollinen ARP-väärennös
- Käyttäjä voi viedä analyysin PDF-muodossa
