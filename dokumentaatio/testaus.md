# Testausdokumentti
Ohjelman testaus keskittyy kolmeen osa-alueeseen:
- tietokantaintegraation testaus
- pakettien parsinnan testaus
- analyysien testaus

Testikattavuus on noin 85%

## Tietokantaintegraatio
Integraatiota testataan parsimalla todellinen PCAP-tiedosto samoin kuin ohjelmaa ajettaessa,
jonka jälkeen sitä kirjoitetaan ja luetaan tietokannasta, varmistaen että tieto ei vääristy missään vaiheessa.

## Pakettien parsinnan testaus
Kaikista paketeista parsitaan muutamat yleistiedot, kuten koko ja saapumisaika.
DNS- ja DHCP-paketeista parsitaan kattavammin protokollakohtaisia tietoja.

Samoin kuin tietokantaintegraation testauksessa, tässäkin parsitaan todellinen PCAP-tiedosto, ja tarkistetaan,
että valittujen pakettien tietyt arvot on tallennettu ohjelman tietorakenteisiin oikein.

# Analyysin testaus
Aloitetaan samoin kun parsinnan testauksessa, eli luetaan PCAP-tiedosto ohjelman tietorakenteisiin.
Tämän jälkeen pyydetään ohjelmalta statistiikkaa paketeista, ja tarkistetaan, että ne vastaavat odotettua.