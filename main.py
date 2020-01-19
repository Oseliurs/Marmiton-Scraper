import requests
from bs4 import BeautifulSoup as soup

##-------------------------------------------------------------------------- Page Scanner ------------------------------
def Scan(url):
    r = requests.get(url)
    req_soup = soup(r.text, 'html5lib')
    out = []

    # Recupération de l'url
    out.append(url)

    # Recupération du Titre
    out.append(req_soup.findAll(attrs={"property": "og:title"})[0].get("content"))

    # Récupération des Ingredients
    out.append(req_soup.findAll(attrs={"property": "og:description"})[0].get("content").split(", "))

    return out

##-------------------------------------------------------------------------- List Scanner ------------------------------
def GetAllReciepe(n):
    out = []
    for i in range(1, n + 1):
        print("Scanning Page " + str(i) + " out of " + str(n) + ".")
        r = requests.get("https://www.marmiton.org/recettes/?type=entree=" + str(i))
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a'):
            if link.get('class') == ['recipe-card-link']:
                print("Now Scanning " + link.get('href') + " ...")
                out.append(ScanReciepe(link.get('href')))

    return out


def WriteToFile(OList):
    out = ""
    for reciepe in OList:
        out = out + reciepe[0] + "," + reciepe[1] + ",[" + reciepe[2] + "]\n"

    print("Writing to File ...")
    with open("/content/drive/My Drive/Colab Notebooks/750g Web Scraper/Final.txt", "w", encoding="utf8") as file:
        file.write(out)
    print("File Written")


print(Scan("https://www.marmiton.org/recettes/recette_nouilles-sautees-aux-legumes-et-poulet-chine_23507.aspx"))
