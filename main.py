import requests
from bs4 import BeautifulSoup as soup
import json

##-------------------------------------------------------------------------- Page Scanner ------------------------------
def Scan(url):
    r = requests.get(url)
    req_soup = soup(r.text, 'html5lib')
    out = []

    # Debugging
    print("GET : " + url)

    # Recupération de l'url
    out.append(url)

    # Recupération du Titre
    out.append(req_soup.findAll(attrs={"property": "og:title"})[0].get("content"))

    # Récupération des Ingredients
    out.append(req_soup.findAll(attrs={"property": "og:description"})[0].get("content").split(", "))

    return out

##-------------------------------------------------------------------------- List Scanner ------------------------------
def GetAllReciepe(url):
    run = True
    page = 1
    out = []
    last = []
    now = []
    while(run):
        #
        out += now
        last = now
        now = []

        # Chargement de la page
        print("Scanning Page " + str(page) + ".")
        req = requests.get(url + "&page=" + str(page)).text
        req_soup = soup(req, 'html.parser')


        # Analyse de la page
        for link in req_soup.find_all("a",{"class":"recipe-card-link"}):
            now.append(link.get('href'))


        # Stop detection
        if last == now:
            run = False
        else:
            page += 1

    return(out)



##-------------------------------------------------------------------------- Main Code ---------------------------------

# Paramètres
UpLib = True
UpData = False

# Variables
Data = {}
Lib = {}

urls = {
    "entree": "https://www.marmiton.org/recettes/?type=entree",
    "plat_principal": "https://www.marmiton.org/recettes/?type=platprincipal",
    "dessert": "https://www.marmiton.org/recettes/?type=dessert",
    "amuse_gueule": "https://www.marmiton.org/recettes/?type=amusegueule",
    "sauce": "https://www.marmiton.org/recettes/?type=sauce",
    "accompagnement": "https://www.marmiton.org/recettes/?type=accompagnement",
    "boisson": "https://www.marmiton.org/recettes/?type=boisson"
}

# Code

# Update de la Bibliothèque de recettes
if UpLib:
    for recette_type in urls:
        Lib[recette_type] = GetAllReciepe(urls[recette_type])

    with open("Lib.csv", "w", encoding="utf8") as file:
        file.write(json.dumps(Lib))

else:
    try:
        with open("Lib.json", "r", encoding="utf8") as file:
            Lib = json.loads(file.read())
    except FileNotFoundError:
        print("The Lib file coulnd't be found change the UpLib variable to vreate a new library.")

#Update des données de recettes.
if UpData:
    for recette_type in Lib:
        out = []
        for url in Lib[recette_type]:
            out.append(Scan(url))
        Data[recette_type] = out

    with open("test2.csv", "w", encoding="utf8") as file:
        file.write(json.dumps(Data))

print("Your Actions Have been Done !!! :)")
