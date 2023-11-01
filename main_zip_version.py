import re
import os
from shutil import rmtree, make_archive
import requests
from bs4 import BeautifulSoup


def get_chapters_and_volumes():
    def list_to_dict(lista: list) -> dict:
        result = {}
        for item in lista:
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


def find_father(dizionario, numero):
    for volume, capitoli in dizionario.items():
        if any(numero == numero_capitolo for numero_capitolo in capitoli.values()):
            return volume.split(" ")[-1]
    return None


volumes_and_chapters = get_chapters_and_volumes()
starting_chapter = int(input("Inserisci il numero del capitolo da scaricare: "))
chapters_to_download = int(input("Quanti capitoli vuoi scaricare? "))
temp_path = os.path.join(os.getenv("TEMP"), "onepiece_test")

try:
    os.mkdir(temp_path)
    print(f"Folder: {temp_path} created successfully")
except FileExistsError:
    print(f"Folder: {temp_path} not created: already exists")
    pass

for delta_chapter in range(0, chapters_to_download):
    chapter = str(starting_chapter + delta_chapter).zfill(3)
    volume = find_father(volumes_and_chapters, int(chapter))
    chapter_path = os.path.join(temp_path, f"chapter_{chapter}")
    try:
        os.mkdir(chapter_path)
    except FileExistsError:
        pass

    for page in [str(x).zfill(2) for x in range(1, 30)]:
        print(f"Volume: {volume}, Capitolo: {chapter}, Pagina: {page}")
        page_download = requests.get(f"https://onepiecepower.com/manga8/onepiece/volumiSpeciali/volumiColored/volume{volume}/{chapter}/{page}.jpg")
        if page_download.status_code == 200:
            print("OK")
            image_path = os.path.join(chapter_path, f"image_{page}.jpg")
            with open(image_path, "wb") as f:
                f.write(page_download.content)
        else:
            break
    output_path = os.path.join("output", f"Capitolo {chapter}")
    make_archive(output_path, "zip", chapter_path)
    print(f"ZIP: {output_path} created successfully")

rmtree(temp_path)
print(f"Folder: {temp_path} deleted successfully")
