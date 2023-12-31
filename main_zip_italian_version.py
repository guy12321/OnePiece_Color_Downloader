import re
import os
import requests
import tempfile
from bs4 import BeautifulSoup
from shutil import rmtree, make_archive


# Questa classe gestisce l'eccezione per cui viene immesso un capitolo non valido
class VolumeNotFoundError(Exception):
    def __init__(self, chapter) -> None:
        self.chapter = chapter
        super().__init__(f"The volume for the chapter {chapter} does not exists")


# Questa funzione effettua una get all'url indicato sotto e ottiene una lista di elementi dal codice sorgente della pagina e li converte in un dizionario volume-capitoli
def get_chapters_and_volumes():
    def list_to_dict(list_to_convert: list) -> dict:
        result = {}
        for item in list_to_convert:
            if item[0].lower() == "v":
                result[item] = {}
                last_volume = item
                continue

            elif item[0].lower() == "c":
                result[last_volume][item] = int(item.split(" ")[1])
                continue

        return result

    url = "https://onepiecepower.com/manga8/onepiece/volumiSpeciali/volumiColored/lista-capitoli"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    tr_elements = list(soup.find_all("tr"))

    volumes_chapters = str(tr_elements[5])
    volumes_chapters = volumes_chapters.replace('<br/><h2 align="center" style="margin-top:0;color:red">', "")
    volumes_chapters = volumes_chapters.replace('</h2>', "")
    volumes_chapters_list = volumes_chapters.split("\n")

    regex = r'<a href="reader\/\d+">(Capitolo \d+).+'

    result = []

    for row in volumes_chapters_list:
        first_letter = row[0]
        if first_letter == "V":
            result.append(row)

        else:
            regex_result = re.findall(regex, row)
            if regex_result:
                result.append(regex_result[0])

    return list_to_dict(result)


# Questa funzione prende in input il dizionario creato con la funzione precedente e dato il numero di un capitolo capisce il volume di riferimento
def find_father(input_dict, value_to_find):
    for volume, chapters in input_dict.items():
        if any(value_to_find == chapter_number for chapter_number in chapters.values()):
            return volume.split(" ")[-1]

    return None


# Questa funzione stampa una linea vuota nel terminale
def newline():
    print("")


if __name__ == "__main__":
    try:
        volumes_and_chapters = get_chapters_and_volumes()  # Dizionario contente le informazioni necessarie
        starting_chapter = int(input("Inserisci il numero del capitolo da scaricare: "))  # Capitolo dal quale iniziare a scaricare
        chapters_to_download = int(input("Quanti capitoli vuoi scaricare? "))  # Capitoli da scaricare successivamente a quello scelto (incluso lo stesso capitolo scritto precedentemente)
        # Ottengo la cartella temporanea del sistema in uso e creo una cartella da utilizzare
        temp_path = os.path.join(tempfile.gettempdir(), "OnePieceDownloader_TempDir")

        # Provo a creare la cartella, se la cartella è già presente salto il processo
        try:
            newline()
            os.mkdir(temp_path)
            print(f"Cartella: {temp_path} creata correttamente")

        except FileExistsError:
            print(f"Cartella: {temp_path} già esistente")

        # Eseguo un iterazione sul numero di capitoli da scaricare
        for delta_chapter in range(0, chapters_to_download):
            chapter = str(starting_chapter + delta_chapter).zfill(3)  # Numero del capitolo in download attuale
            volume = find_father(volumes_and_chapters, int(chapter))  # Numero del volume del capitolo
            if volume is None:
                raise VolumeNotFoundError(chapter)

            # Genero il path per il salvataggio del capitolo
            chapter_path = os.path.join(temp_path, f"chapter_{chapter}")
            try:
                # Provo a creare la cartella generata in precedenza
                os.mkdir(chapter_path)

            except FileExistsError:
                pass  # Non creo la cartella

            actual_chapter = starting_chapter + delta_chapter
            final_chapter = starting_chapter + chapters_to_download - 1
            chapters_downloaded = delta_chapter + 1
            completed_download_percentage = round((chapters_downloaded - 1) / chapters_to_download * 100, 2)

            newline()
            print(f"Scaricando il capitolo: {actual_chapter}/{final_chapter} ({chapters_downloaded} di {chapters_to_download}) {completed_download_percentage}%")

            # Itero e scarico ogni pagina sino ad ottenere un codice diverso da 200
            starting_page = 1
            while True:
                actual_page = str(starting_page).zfill(2)
                print(f"Scaricando la pagina: {actual_page}")
                page_download = requests.get(f"https://onepiecepower.com/manga8/onepiece/volumiSpeciali/volumiColored/volume{volume}/{chapter}/{actual_page}.jpg")
                if page_download.status_code == 200:
                    print("Fatto")
                    # Scrivo l'immagine scaricata in un file JPG
                    image_path = os.path.join(chapter_path, f"image_{actual_page}.jpg")
                    with open(image_path, "wb") as f:
                        f.write(page_download.content)
                    starting_page += 1

                else:
                    print("Impossibile scaricare l'immagine")
                    print("Scrivo le immagini scaricate in uno ZIP...")
                    break

            # Genero il path di output del capitolo scaricato
            output_path = os.path.join(os.path.dirname(__file__), "output", f"Capitolo {chapter}")
            # Genero il file zip del capitolo scaricato e lo salvo nel path precedentemente creato
            make_archive(output_path, "zip", chapter_path)
            print(f"ZIP: {output_path} creato correttamente")

    # Gestione delle eccezioni
    except Exception as err:
        print(f"Something went wrong: {err}")

    except KeyboardInterrupt:
        print("Something went wrong: KeyboardInterrupt")

    # In caso di errore o meno rimuovo la cartella temporanea creata all'inizio
    finally:
        try:
            rmtree(temp_path)
            newline()
            print(f"Cartella: {temp_path} cancellata correttamente")

        except Exception:
            pass  # Se per qualche motivo la cartella temporanea non dovesse esistere procedo a non cancellarla
