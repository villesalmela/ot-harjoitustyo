## Peruskäyttö
0. Katso ohjeet ohjelman asentamiseen ja käynnistämiseen [readmestä](/README.md)
1. Avaa valitsemasi PCAP-tiedosto
    - Näppäinkomennolla Ctrl+N tai valikosta File -> Add New Capture
    - "assets" kansiossa on pari esimerkkitiedostoa
2. Tarkastele tietoja eri välilehdillä
3. Voit lisätä analyysiin lisää tiedostoja, samalla lailla kuin ensimmäisen
4. Voit tallentaa ja ladata tallennetun analyysin "Save" (Ctrl-S) ja "Load" (Ctrl-O) -napeilla
5. Voit poistaa tallennetun analyysin "Delete" (Ctrl+D) -napilla.
6. Resetoi ohjelma alkutilanteeseen
    - Näppäinkomennolla Ctrl+R tai valikosta File -> Reset
7. Poistu ohjelmasta
    - Näppäinkomennolla Ctrl+Q tai valikosta File -> Exit

## Konfigurointi
Voit konfiguroida ohjelman asetuksia [.env tiedostossa](/.env)

### DB_PATH
Tietokannan polku

### TIMEOUT_SECONDS
Kuinka kauan yritetään tiedoston avaamista, ennen kuin luovutetaan

### FILESIZE_LIMIT_BYTES
Tiedostokoon rajoitin