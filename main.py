import requests
from bs4 import BeautifulSoup as soup
import json

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

final = []

temp = {}

urls = {
"entree":"https://www.marmiton.org/recettes/?type=entree",
"plat_principal":"https://www.marmiton.org/recettes/?type=platprincipal",
"dessert":"https://www.marmiton.org/recettes/?type=dessert",
"amuse_gueule":"https://www.marmiton.org/recettes/?type=amusegueule",
"sauce":"https://www.marmiton.org/recettes/?type=sauce",
"accompagnement":"https://www.marmiton.org/recettes/?type=accompagnement",
"boisson":"https://www.marmiton.org/recettes/?type=boisson"
}

for recette_type in urls:
    temp[recette_type] = GetAllReciepe( urls[recette_type] )

with open("test.json","w",encoding="utf8") as file:
    file.write(json.dumps(temp))


