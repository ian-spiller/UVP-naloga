import csv
import bottle
import requests
import glob
import os
from yahoo_fin.stock_info import*

# FUNKCIJE

def izberi_seznam(seznam,ime):
    for x in seznam:
        if ime in x[0]:
            return x

#TA FUNKCIJA SE ZNEBI TTM-ja(seznam za eno krajsi)       

def odstrani_vejice(seznam):
    nov_seznam=[seznam[0]]
    for x in seznam[1:11]:
        if not x=="":
            stevilo=(float(x.replace(",","")))
            nov_seznam=nov_seznam+[stevilo]
        else:
            nov_seznam=nov_seznam+["NI ELEMENTA"]
    return (nov_seznam)

def povprecje(urejen_seznam,leta=1):
    vsota=0
    brez_vrednosti=urejen_seznam[(11-leta):12].count("NI ELEMENTA")
    negativne_vrednosti=0
    for x in urejen_seznam[11-leta:12]:
        if x=="NI ELEMENTA":
            vsota=vsota
        elif x>=0:
            vsota=vsota+x
        else:
            vsota=vsota+x
            negativne_vrednosti=negativne_vrednosti+1
    if leta==brez_vrednosti:
        povprecna_vrednost=round(vsota/(leta),2)
    else:
        povprecna_vrednost=round(vsota/(leta-brez_vrednosti),2)
    rezultat=[povprecna_vrednost,brez_vrednosti,negativne_vrednosti]
    return(rezultat)

def rast(seznam):
    indeksi=[]
    indeks=0
    for x in seznam:
        if x=="NI ELEMENTA":
            indeks=indeks+1
            indeksi=indeksi+[indeks]
        else:
            indeks=indeks+1
    if seznam[1]=="NI ELEMENTA":
        mesto=indeksi[-1]
        if seznam[mesto]<0 or seznam[mesto]<0:
            return ["Negativna vrednost",10]
        else:
            rast=round((((seznam[10]/seznam[mesto])**(1/(9-indeksi[-1]))-1)*100),2)
            koliko_letno_rast=10-indeksi[-1]
            rezultat=[rast,koliko_letno_rast]
            return rezultat
    elif seznam[1]<0 or seznam[10]<0:
        return ["Negativna vrednost",10]
    elif len(indeksi)==8:
        return ["Podatki so samo za eno leto",10]
    elif indeksi==[] and seznam[1]==0:
        return "Deljenje z nic."
    elif indeksi==[]:
        rast=round((((seznam[10]/seznam[1])**(1/9))-1)*100,2)
        rezultat=[rast,10]
        return rezultat

#ZACETEK

pot_do_fila = os.path.dirname(os.path.realpath(__file__))
seznam_file=glob.glob(("{}\*.csv").format(pot_do_fila))
seznam_firm=[]
for x in seznam_file:
    koscki=x.split("\\")
    for y in koscki:
        if "csv" in y:
            ime_podjetja=(y.split("."))[0]
            if "Key Ratios" in ime_podjetja:
                ime_podjetja=y.split()
                seznam_firm=seznam_firm+[ime_podjetja[0]]
            else:
                 ime_podjetja=(y.split("."))
                 seznam_firm=seznam_firm+[ime_podjetja[0]]

@bottle.get("/")
def osnovna_stran():
    return bottle.template("Internet-dostop.tpl",seznam_firm=seznam_firm)

@bottle.get("/delnice/")
def sestej():
    kratica = bottle.request.query["Company"]
    leta = int(bottle.request.query["Years"])

#NEOBVEZNE SPREMENLJIVKE

    try:
        rast_prodaja = bottle.request.query["prodaja"]
    except:
        rast_prodaja="Ni zahteve"
    try:
        rast_operating = bottle.request.query["operativni"]
    except:
        rast_operating="Ni zahteve"
    try:
        rast_net = bottle.request.query["net"]
    except:
        rast_net="Ni zahteve"
    try:
        rast_OCF = bottle.request.query["OCF"]
    except:
        rast_OCF = "Ni zahteve"
    
    neobvezne_spremenljivke=[rast_prodaja,rast_operating,rast_net,rast_OCF]

    try:
        P_E = bottle.request.query["P/E"]
    except:
        P_E = "Ni zahteve"
    try:
        P_B = bottle.request.query["P/B"]
    except:
        P_B = "Ni zahteve"
    try:
        P_OCF = bottle.request.query["P/OCF"]
    except:
        P_OCF = "Ni zahteve"
    try:
        Dividenda_1 = bottle.request.query["Dividenda"]
    except:
        Dividenda_1 = "Ni zahteve"
        
#CENA IZ YAHOO FINANCE    

    cena=round(float(get_live_price("{}".format(kratica))),2)
    
    path="{}\\{} Key Ratios.csv".format(pot_do_fila,kratica)
    with open(path,"r") as vhodna:
        vsi_podatki=csv.reader(vhodna,delimiter=",")
        seznam=[]
        for x in vsi_podatki:
            seznam=seznam+[x]
        for x in seznam:
            if x==[]:
                indeks=seznam.index(x)
        podatki=[]
        for x in seznam[0:indeks]:
            podatki=podatki+[x]

#IZARCUNAMO TECAJNO RAZLIKO

    vrstica_revenue=izberi_seznam(podatki,"Revenue")
    valuta=((vrstica_revenue[0]).split())[1]
    if valuta=="USD":
        tecajna_razlika=1
    else:
        tecajna_razlika=""
        url = 'http://www.floatrates.com/daily/usd.xml'
        response = requests.get(url)
        podatki_internet=response.text
        x=podatki_internet.split("<item>")
        for y in x:
            if valuta in y:
                vrstice=y.splitlines()
                for vrstica in vrstice:
                    if "inverseRate" in vrstica:
                        for crka in vrstica:
                            if crka.isdigit()==True or crka==".":
                                tecajna_razlika=tecajna_razlika+crka
        tecajna_razlika=float(tecajna_razlika)

#OBDELAVA PODATKOV:

#P/E
    vrstica_earinig=izberi_seznam(podatki,"Earnings")
    obdelano_vrstico_earning=odstrani_vejice(vrstica_earinig)
    povprecen_earning_seznam=povprecje(obdelano_vrstico_earning,leta)
    povprecen_earning=((povprecen_earning_seznam[0])*tecajna_razlika)
    PRICE_EARNING=round(cena/povprecen_earning,1)
    BREZ_VREDOSTI_EPS=povprecen_earning_seznam[1]
    NEGATIVNE_VREDNOSTI_EPS=povprecen_earning_seznam[2]

#P/OCF
#PODATKI MORAJO BITI V MILJONIH
    vrstica_OCF=izberi_seznam(podatki,"Operating Cash Flow")
    obdelano_vrstico_OCF=odstrani_vejice(vrstica_OCF)
    povprecen_OCF_seznam=povprecje(obdelano_vrstico_OCF,leta)
    povprecen_OCF=((povprecen_OCF_seznam[0])*tecajna_razlika)
    vrstica_stevilodelnic=izberi_seznam(podatki,"Shares")
    obdelano_vrstico_stevilodelnic=(odstrani_vejice(vrstica_stevilodelnic))[10]
    PRICE_OCF=round(cena/(povprecen_OCF/obdelano_vrstico_stevilodelnic),1)
    BREZ_VREDOSTI_OCF=povprecen_OCF_seznam[1]
    NEGATIVNE_VREDNOSTI_OCF=povprecen_OCF_seznam[2]

#P/B
    problem1=""
    PRICE_BOOK="0"
    vrstica_book_value=izberi_seznam(podatki,"Book Value")
    obdelano_vrstico_book=odstrani_vejice(vrstica_book_value)
    if obdelano_vrstico_book[10]==0:
        problem1="Deljenje z nic"
    elif obdelano_vrstico_book[10]<0:
        problem1="Negativna vrednost"
    elif obdelano_vrstico_book[10]=="NI ELEMENTA":
        problem1="NI ELEMENTA"
    else:
        vrednost_book=(obdelano_vrstico_book[10])*tecajna_razlika
        PRICE_BOOK=round(cena/vrednost_book,1)

#DIVIDENDA
    vrstica_dividenda=izberi_seznam(podatki,"Dividends")
    obdelano_vrstico_dividenda=odstrani_vejice(vrstica_dividenda)
    if obdelano_vrstico_dividenda[10]==0:
        problem2="Deljenje z nic"
    elif obdelano_vrstico_dividenda[10]=="NI ELEMENTA":
        vrednost_dividenda=0
        DIVIDENDA=(round((vrednost_dividenda*tecajna_razlika)/cena,2))*100
    else:
        vrednost_dividenda=(obdelano_vrstico_dividenda[10])*tecajna_razlika
        DIVIDENDA=round((vrednost_dividenda/cena)*100,1)

#RAST
    rast_koncno=[]
    for x in neobvezne_spremenljivke:
        if not x=="Ni zahteve":
            vrstica_rast=izberi_seznam(podatki,x)
            obdelano_vrstico_rast1=odstrani_vejice(vrstica_rast)
            rast_seznam=rast(obdelano_vrstico_rast1)
            rast_koncno=rast_koncno+[rast_seznam]
        else:
            rast_koncno=rast_koncno+[x]
    
    seznam_rast={}
    imena=[["RAST_PRODAJA","KOLIKO_LETNA_RAST_PRODAJA"],["RAST_OPERATING","KOLIKO_LETNA_RAST_OPERATING"],
    ["RAST_NET","KOLIKO_LETNA_RAST_NET"],["RAST_OCF","KOLIKO_LETNA_RAST_OCF"]]
    for x in range(0,len(imena)):
        if not rast_koncno[x]=="Ni zahteve":
            for y in range(0,2):
                seznam_rast[imena[x][y]]=rast_koncno[x][y]
        else:
            for y in range(0,2):
                seznam_rast[imena[x][y]]="Ni zahteve"

    RAST_PRODAJA=seznam_rast.get("RAST_PRODAJA")
    KOLIKO_LETNA_RAST_PRODAJA=seznam_rast.get("KOLIKO_LETNA_RAST_PRODAJA")
    RAST_OPERATING=seznam_rast.get("RAST_OPERATING")
    KOLIKO_LETNA_RAST_OPERATING=seznam_rast.get("KOLIKO_LETNA_RAST_OPERATING")
    RAST_NET=seznam_rast.get("RAST_NET")
    KOLIKO_LETNA_RAST_NET=seznam_rast.get("KOLIKO_LETNA_RAST_NET")
    RAST_OCF=seznam_rast.get("RAST_OCF")
    KOLIKO_LETNA_RAST_OCF=seznam_rast.get("KOLIKO_LETNA_RAST_OCF")

    return bottle.template("Internet-izstop.tpl",leta=leta,kratica=kratica,cena=cena,
    price_earning=PRICE_EARNING,brez_vrednosti_eps=BREZ_VREDOSTI_EPS,
    negativne_vrednosti_eps=NEGATIVNE_VREDNOSTI_EPS,rast_net=RAST_NET,koliko_letna_rast_net=KOLIKO_LETNA_RAST_NET,P_E=P_E,
    price_OCF=PRICE_OCF,brez_vrednosti_OCF=BREZ_VREDOSTI_OCF,negativne_vrednosti_OCF=NEGATIVNE_VREDNOSTI_OCF,
    rast_OCF=RAST_OCF,koliko_letna_rast_OCF=KOLIKO_LETNA_RAST_OCF,P_OCF=P_OCF,price_book=PRICE_BOOK,problem_P_B=problem1,P_B=P_B,
    dividenda=DIVIDENDA,Dividenda_1=Dividenda_1,rast_operating=RAST_OPERATING,koliko_letna_rast_operating=KOLIKO_LETNA_RAST_OPERATING,
    rast_prodaja=RAST_PRODAJA,koliko_letna_rast_prodaja=KOLIKO_LETNA_RAST_PRODAJA)

bottle.run(debug=True,reloader=True)


