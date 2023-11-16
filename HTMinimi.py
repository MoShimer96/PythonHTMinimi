import time
import os
import sys
######################################################################
# CT60A0203 Ohjelmoinnin perusteet
# Tekijä: Mohamed Shimer
# Opiskelijanumero: 000524560
# Päivämäärä: 16.11.2023
# Kurssin oppimateriaalien lisäksi työhön ovat vaikuttaneet seuraavat
# lähteet ja henkilöt, ja se näkyy tehtävässä seuraavalla tavalla:
#
# Mahdollisen vilppiselvityksen varalta vakuutan, että olen tehnyt itse
# tämän tehtävän ja vain yllä mainitut henkilöt sekä lähteet ovat
# vaikuttaneet siihen yllä mainituilla tavoilla.
######################################################################
# Tehtävä Harjoitustyö perustaso
# eof
def valikko():
    print('Valitse haluamasi toiminto:\n1) Lue tiedosto\n2) Analysoi\n3) Kirjoita tiedosto\n0) Lopeta')
    try:
        valinta = int(input('Anna valintasi: '))
    except ValueError:
        pass
    
    return valinta


def kysy_tiedoston_nimi(luettava = False, kirjoitettava = False):
    tiedoston_nimi = ''

    if luettava == True:
        tiedoston_nimi = input('Anna luettavan tiedoston nimi: ')     

    if kirjoitettava == True:
        tiedoston_nimi = input('Anna kirjoitettavan tiedoston nimi: ')
         
    return tiedoston_nimi

def suurin_ja_pienin_arvo(new_dict):
    max_key = max(new_dict, key=new_dict.get)
    min_key = min(new_dict, key=new_dict.get)

    return max_key, min_key
       
    
def kavijamaara_analyysi(lst):
    dict = {}
    palautettava_lst = []
    lst_ilman_ensimmaista_rivia = lst[1:]
    
    for row in lst_ilman_ensimmaista_rivia:
        key = time.strptime(row[0], '%d.%m.%Y')
        if key not in dict:
            dict[key] = 0
    
    for row in lst_ilman_ensimmaista_rivia:
        key = time.strptime(row[0], '%d.%m.%Y')
        row_ilman_aikaleima = row[1:]
        for value in row_ilman_aikaleima:
            dict[key] += int(value)
    
    kokovuosi = 0
    for key, value in dict.items():
        kokovuosi += value
    paivittain = round((kokovuosi/len(lst_ilman_ensimmaista_rivia)),1)
    
    #avain_1 antaa meille suurin päivittäinen kävijämäärä ja avain_2 antaa meille vähiten kävijämäärä    
    avain_1, avain_2 = suurin_ja_pienin_arvo(dict)

    palautettava_lst.append(kokovuosi)
    palautettava_lst.append(paivittain)
    palautettava_lst.append(time.strftime('%d.%m.%Y', avain_1)) 
    palautettava_lst.append(dict[avain_1])
    palautettava_lst.append(time.strftime('%d.%m.%Y', avain_2))
    palautettava_lst.append(dict[avain_2])

    return palautettava_lst


def kuukausittainen_kavijamaara(lst):
    dict = {}
    
    lst_ilman_ensimmaista_rivia = lst[1:]
    for row in lst_ilman_ensimmaista_rivia:
        key = time.strptime(row[0], '%d.%m.%Y')
        key_kuukausi = key.tm_mon
        if key_kuukausi not in dict:
            dict[key_kuukausi] = 0
    
    for row in lst_ilman_ensimmaista_rivia:
        key = time.strptime(row[0], '%d.%m.%Y')
        key_kuukausi = key.tm_mon
        row_ilman_aikaleima = row[1:]
        for value in row_ilman_aikaleima:
            dict[key_kuukausi] += int(value)
    
    return dict

def valinta_yksi_lue_tiedosto():
    luettava_tiedoston_nimi = kysy_tiedoston_nimi(luettava=True)
    
    puhdistettu_lista = []
    index_of_temp_lst = 0
    try:   
        tiedosto_avattu = open(luettava_tiedoston_nimi, 'r', encoding='UTF-8')

        for line in tiedosto_avattu.readlines():
            #lisätään tyhjä lista palautettavaan listaan
            puhdistettu_lista.append([])
            
            #Tämä muodostaa uuden listan 
            line_split = line.split(';')

            for item in line_split:
                #Puhdistetaan ylimääräiset merkkit pois!
                puhdistettu_lista[index_of_temp_lst].append(item.strip())
            #Siirrytään seuraavaan slottiin listassa.
            index_of_temp_lst+=1
        tiedosto_avattu.close()
        print('Tiedostosta \'{}\' lisättiin listaan {} datariviä.\n'.format(luettava_tiedoston_nimi, len(puhdistettu_lista)-1))
        return puhdistettu_lista
    except FileNotFoundError:
        print('Tiedoston\'{}\'  käsittelyssä virhe, lopetetaan.'.format(luettava_tiedoston_nimi))
        print('')
        sys._exit(0)

def valinta_kaksi_analysoi(lista):
    dict_kavijamaarat_kuukausittain = {}
    
    dict_kavijamaarat_kuukausittain =  kuukausittainen_kavijamaara(lista)
    lista_muu = kavijamaara_analyysi(lista)
    print('Tilastotietojen analyysi suoritettu.\nKuukausittaiset summat laskettu.\n')
    return dict_kavijamaarat_kuukausittain, lista_muu, (len(lista)-1)


def valinta_kolme_kirjoita(mun_dict, lst, num):
    
    tiedoston_nimi = kysy_tiedoston_nimi(kirjoitettava=True)
    try:
        uusi_tiedosto = open(tiedoston_nimi, 'w', encoding='UTF-8')
        
        uusi_tiedosto.write('Analyysin tulokset {} päivältä ovat seuraavat:\n'.format(num))
        uusi_tiedosto.write('Kävijämäärä koko vuonna yhteensä oli {}.\n'.format(lst[0]))
        uusi_tiedosto.write('Päivittäinen kävijämäärä oli keskimäärin {}.\n'.format(lst[1])) 
        uusi_tiedosto.write('Eniten kävijöitä oli {}, {} kpl.\n'.format(lst[2], lst[3]))
        uusi_tiedosto.write('Vähiten kävijöitä oli {}, {} kpl.\n'.format(lst[4],lst[5]))
        uusi_tiedosto.write('\n')
        uusi_tiedosto.write('Kuukausittaiset kävijämäärät (Kk;Lukumäärä):\n')
        for key, value in mun_dict.items():
            if key == 10 or key == 11 or key == 12:
                uusi_tiedosto.write('Kk {};{}\n'.format(key, value))
            else:
                uusi_tiedosto.write('Kk 0{};{}\n'.format(key, value))

        print('Tiedosto \'{}\' kirjoitettu.\n'.format(tiedoston_nimi))
        return None
    except OSError:
        print('Tiedoston\'{}\'  käsittelyssä virhe, lopetetaan.'.format(tiedoston_nimi))
        print('')
        os._exit(0)




def paaohjelma():
    analyysi_paivien_maara = 0
    lista_analyysia_varten = []
    lista_tiedoston_kirjoittamiseen = []
    dict_kuukausittain = {}
    while True:
        valinta = valikko()
        if valinta == 1:
            lista_analyysia_varten = valinta_yksi_lue_tiedosto()
            continue 
        elif valinta == 2:
            if not lista_analyysia_varten:
                print("Ei tietoja analysoitavaksi, lue tiedot ennen analyysiä.\n")
                continue
            else:
                dict_kuukausittain, lista_tiedoston_kirjoittamiseen, analyysi_paivien_maara = valinta_kaksi_analysoi(lista_analyysia_varten) 
                continue
        elif valinta == 3:
            if not lista_tiedoston_kirjoittamiseen:
                print("Ei tietoja tallennettavaksi, analysoi tiedot ennen tallennusta.\n")
                continue
            else:
                valinta_kolme_kirjoita(dict_kuukausittain, lista_tiedoston_kirjoittamiseen, analyysi_paivien_maara)
                continue 
        elif valinta == 0:
            print('Lopetetaan.\n')
            print('Kiitos ohjelman käytöstä.')
            break
        else:
            print('Väärä valinta')
            continue
    lista_analyysia_varten.clear()
    lista_tiedoston_kirjoittamiseen.clear()    
    return None

paaohjelma()