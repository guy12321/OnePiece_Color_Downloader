# OnePiece Downloader

Questo script Python consente di scaricare i capitoli del manga *One Piece* in versione *Digital colored comics* dal sito [onepiecepower.com](https://onepiecepower.com/manga8/onepiece/volumiSpeciali/volumiColored/lista-capitoli) e salvarli in formato ZIP.

## Istruzioni

1. Esegui lo script Python (`onepiece_downloader.py`).
2. Inserisci il numero del capitolo da cui desideri iniziare il download.
3. Specifica quanti capitoli desideri scaricare a partire da quello indicato.

Lo script creerà una cartella temporanea, scaricherà le immagini dei capitoli e le salverà in un file ZIP.

## Requisiti

- Python 3
- Moduli Python: `requests`, `beautifulsoup4`

## Utilizzo

1. **Installazione dei moduli:** Puoi installare i moduli richiesti eseguendo il comando:
```
pip install requests beautifulsoup4
```

2. **Esecuzione dello script:** Dalla console, esegui il comando:
```
python onepiece_downloader.py
```

3. **Input:** Segui le istruzioni fornite per inserire il capitolo di partenza e il numero di capitoli da scaricare.

4. **Output:** Una cartella `output` con i file ZIP dei capitoli scaricati verrà creata nella directory dello script.

## Note

- Se lo script viene interrotto, la cartella temporanea verrà comunque eliminata.
- Il file ZIP di ciascun capitolo sarà nella directory `output` e denominato come "`Capitolo {numero del capitolo}`".

## Attenzione

Questo script è stato progettato per scopi educativi e personali. Assicurati di rispettare i diritti d'autore e le politiche del sito web dal quale stai scaricando i contenuti. L'uso improprio potrebbe violare i termini di servizio del sito.

**Disclaimer:** L'autore di questo script non è responsabile dell'uso improprio o illegale che potrebbe essere fatto con lo stesso.

---

### Versioni disponibili

Il programma è disponibile in due versioni, con output in italiano o inglese.
