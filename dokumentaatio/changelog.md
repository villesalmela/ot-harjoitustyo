# Viikko 3
- Lisätty luokkia pakettien esittämiseen
    - Packet
    - Ethernet
    - IP
    - TCP
    - UDP
    - DNS
- Lisätty Enum-tyyppiset luokat numeraalisten arvojen tallentamiseen
    - DNS Query Type
    - DNS Op Code
    - DNS Direction
    - LAYER TYPE
- DNS paketeista parsitaan onnistuneesti link, network, transport ja application -kerroksien tiedot
- Lisätty yksikkötestejä
    - DNS-pakettien parsiminen
- Lisätty kaksi toiminnallisuutta
    - Käyttäjä voi listata parsitut paketit tietoineen
    - Käyttäjä voi tarkistaa yhteenvedon, joka sisältää
        - Onnistuneesti parsittujen pakettien määrä
        - DNS-kyselyjen määrä per FQDN (fully qualified domain name)
- Konfiguroitu invoke-taskit
    - käynnistys: invoke start
    - yksikkötestaus: invoke test
    - testikattavuusraportti: invoke coverage-report

# Viikko 4
- Lisätty luokkia pakettien esittämiseen
    - DHCP
- Lisätty Enum-tyyppiset luokat numeraalisten arvojen tallentamiseen
    - BOOTP Op Code
    - DHCP Message Type
- Lisätty transaction-id kenttä DNS-paketteihin
- Lisätty graafinen käyttöliittymä
    - Pakettien tiedot ja yhteenveto esitetään tekstinä yhdellä välilähdellä
    - DNS-kyselyjen määrä per 2LD (second level domain) esitetään graafina toisella välilehdellä
    - Lisätty valikkoon toiminnot näppäinkomentoineen
        - Ctrl+O: Open file
        - Ctrl+R: Reset
        - Ctrl+Q: Exit
- Data esikäsitellään
    - Byte-tyyppinen objekti pyritään dekoodaamaan tekstiksi tai esittämään hexana
    - Erilaiset numerotyypit normalisoidaan int- ja float-muotoisiksi
    - Nolla-arvoinen padding riisutaan ennen tallennusta
- Lisätty yksikkötestejä
    - Yleinen paketin parsiminen
    - 2LD-parsiminen
    - DHCP-pakettien parsiminen
- Konfiguroitu invoke-taskit 
    - linttaus pylintillä: invoke lint
    - formatointi autopep8 ja docformatterilla: invoke format

# Viikko 5 & 6
- Lisätty luokkia pakettien esittämiseen
    - ICMP
    - IPv6
    - ICMPv6
    - SLL (Linux cooked-mode capture)
    - ARP
    - RAW (esittää raakaa dataa, jonka tyyppiä ei ole tunnistettu)
- Lisätty Enum-tyyppiset luokat numeraalisten arvojen tallentamiseen
    - ARP Op Code
    - Cooked Packet Type
    - Hardware Type
    - ICMPv4 Type & Code
    - ICMPv6 Type & Code
    - IP Version
- Analyzer-komponenteissa käyttöön pandas datan käsittelyssä
- Lisätty toiminnallisuuksia
    - Käyttäjä voi tarkistaa yhteenvedon, joka sisältää
        - Yleisimmät asiakkaat DHCP paketeista
        - Yleisimmät domainit DHCP paketeista
        - Yleisimmät palvelimet DHCP paketeista
    - Käyttäjä näkee dashboard-tyylisistä indikaattoreista
        - Pakettien määrän
        - Siirretyn datan määrän
        - Tallennuksen ajankohdan ja keston
    - Käyttäjä voi katsoa graafista
        - Yleisimmät DNS-palvelimet DNS paketeista
        - Tiedonsiirron nopeus
    - Käyttäjä voi tallentaa analyysin tietokantaan
    - Käyttäjä voi ladata analyysin tietokannasta
    - Käyttäjä voi lisätä analyysiin monta tiedostoa
- Parannettu pakettien parsintaa
    - Lisätty virheenkäsittelyä
    - Lisätty lokitusta
        - support-loki: tuen vuoksi parsimatta jääneet kerrokset
        - error-loki: yllättävän virheen vuoksi parsimatta jääneet kerrokset
        - checksum-loki: mahdollisesti korruptoituneet paketit
- Ehostettu käyttöliitymää
    - Siiretty tiedoston prosessointi omaan säikeeseen, jotta käyttöliittymä ei jumita
    - Lisätty latausindikaattori
    - Estetty tulosteen muokkaminen
    - Tiedostovalinnan virheet esitetään viestillä käyttäjälle

# Viikko 7
- Lisätty toiminnallisuuksia
    - Käyttäjä voi tarkastella protokollajakaumaa neljällä eri tasolla
        - application
        - transport
        - network
        - link
- Ehostettu käyttöliittymää
    - Selkeytetty värejä
    - Ryhmitelty nappuloita
    - Lisätty graafeja
- Parannettu lokitusta
    - Kaikki stdout tai stderr viestit viedään app.log lokitiedostoon