from bs4 import BeautifulSoup
import pandas as pd
from requests import get
from re import sub
from time import sleep
import csv



def main():
    
    # open the csv for recording
    filename = "data/allmunicipalities_allbarangays_households.csv"
    fieldnames = ["Barangay", "Year", "Month", "Day", "Household population", "Number of households", "Average household size"]
    month_num = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6,
        "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
    with open(filename, 'w') as csvfile:
        # csv writer
        csvwriter = csv.writer(csvfile)

        # writing fields
        csvwriter.writerow(fieldnames)
    
    brgy_urls = get_urls()
    print(brgy_urls)
    print(brgy_urls[0])
    print(f"Number of requests will be: {len(brgy_urls)}")
    find_id = "households-table"
    find_class = "chart-table"
    num_of_brgys = len(brgy_urls)
    for i in range(170, num_of_brgys): # 170 is before osmeña
        # begin appending to csv file
        iteration += 1
        with open(filename, 'a', newline="") as csvfile:
            # create the csv writer class
            csvwriter = csv.writer(csvfile)
            
            request = get(brgy_urls[i])
            soup = BeautifulSoup(request.content, 'html.parser')

            # Get the relevant data for each barangay
            # search for the relevant table
            table = soup.find('table', id=find_id)

            # read the barangay name for later recording onto csv
            barangay = sub(" Profile – PhilAtlas", "", soup.title.text.strip())
            for row in table.find_all('tr'):
                # read the columns
                columns = row.find_all('td')
                # read the headings of the found table
                heading = row.find('th', scope='row')
                if (len(columns) >= 2) and (heading is not None):
                    # record population for each year FOR INTERPOLATION
                    population = columns[0].text.strip()
                    # record household for each year REQUIRED
                    num_households = columns[1].text.strip()
                    ave_household_size = columns[2].text.strip()
                    datum = heading.find('time').text.strip()
                    year = (int(datum[:4]))
                    month = (str(datum[5:8]))
                    day = (int(datum[9]))
                    add_row_csv = [barangay, year, month_num[month], day, population, num_households, ave_household_size]
                    # write the new row
                    csvwriter.writerow(add_row_csv)
            
        print(f"last row added: {add_row_csv}")
        print(f"Begining sleep ({i}/{num_of_brgys})...")
        sleep(5)


# START USER INPUT
brgys_staignacia = ["Baldios", "Botbotones", "Caanamongan", 
        "Cabaruan", "Cabugbugan", "Caduldulaoan", "Calipayan", 
        "Macaguing", "Nambalan", "Padapada", "Pilpila", "Pinpinas", 
        "Poblacion East", "Poblacion West", "Pugo-Cecilio", 
        "San Francisco", "San Sotero", "San Vicente", "Santa Ines Centro", 
        "Santa Ines East", "Santa Ines West", "Taguiporo", "Timmaguab", 
        "Vargas"]
brgys_sanclemente = ["Balloc", "Bamban", "Casipo", "Catagudingan", 
    "Daldalayap", "Doclong 1", "Doclong 2", "Maasin", "Nagsabaran", 
    "Pit-ao", "Poblacion Norte", "Poblacion Sur"]
brgys_bayambang = ["Alinggan", "Amamperez", "Amancosiling Norte", 
    "Amancosiling Sur", "Ambayat I", "Ambayat II", "Apalen", "Asin", 
    "Ataynan", "Bacnono", "Balaybuaya", "Banaban", "Bani", "Batangcawa", 
    "Beleng", "Bical Norte", "Bical Sur", "Bongato East", "Bongato West", 
    "Buayaen", "Buenlag 1st", "Buenlag 2nd", "Cadre Site", "Carungay", 
    "Caturay", "Darawey", "Duera", "Dusoc", "Hermoza", "Idong", "Inanlorenzana", 
    "Inirangan", "Iton", "Langiran", "Ligue", "M. H. del Pilar", "Macayocayo", 
    "Magsaysay", "Maigpa", "Malimpec", "Malioer", "Managos", "Manambong Norte", 
    "Manambong Parte", "Manambong Sur", "Mangayao", "Nalsian Norte", "Nalsian Sur", 
    "Pangdel", "Pantol", "Paragos", "Poblacion Sur", "Pugo", "Reynado", "San Gabriel 1st", 
    "San Gabriel 2nd", "San Vicente", "Sangcagulis", "Sanlibo", "Sapang", "Tamaro", "Tambac", 
    "Tampog", "Tanolong", "Tatarao", "Telbang", "Tococ East", "Tococ West", 
    "Warding", "Wawa", "Zone I", "Zone II", "Zone III", "Zone IV", "Zone V", 
    "Zone VI", "Zone VII"]
brgys_mangatarem = ["Andangin", "Arellano Street", "Bantay", "Bantocaling", 
"Baracbac", "Bogtong Bolo", "Bogtong Bunao", "Bogtong Centro", "Bogtong Niog", 
"Bogtong Silag", "Buaya", "Buenlag", "Bueno", "Bunagan", "Bunlalacao", 
"Burgos Street", "Cabaluyan 1st", "Cabaluyan 2nd", "Cabarabuan", "Cabaruan", 
"Cabayaoasan", "Cabayugan", "Cacaoiten", "Calumboyan Norte", "Calumboyan Sur", 
"Calvo", "Casilagan", "Catarataraan", "Caturay Norte", "Caturay Sur", "Caviernesan", 
"Dorongan Ketaket", "Dorongan Linmansangan", "Dorongan Punta", "Dorongan Sawat", 
"Dorongan Valerio", "General Luna", "Historia", "Lawak Langka", "Linmansangan", 
"Lopez", "Mabini", "Macarang", "Malabobo", "Malibong", "Malunec", "Maravilla", 
"Maravilla-Arellano Ext.", "Muelang", "Naguilayan East", "Naguilayan West", "Nancasalan", 
"Niog-Cabison-Bulaney", "Olegario-Caoile", "Olo Cacamposan", "Olo Cafabrosan", 
"Olo Cagarlitan", "Osmeña", "Pacalat", "Pampano", "Parian", "Paul", "Peania Pedania", 
"Pogon-Aniat", "Pogon-Lomboy", "Ponglo-Baleg", "Ponglo-Muelag", "Quetegan", "Quezon", 
"Salavante", "Sapang", "Sonson Ongkit", "Suaco", "Tagac", "Takipan", "Talogtog", 
"Tococ Barikir", "Torre 1st", "Torre 2nd", "Torres Bugallon", "Umangan", "Zamora"]
# END   USER INPUT

def list_to_urls(base_url:str, brgys:list):
    urls = []
    for brgy in brgys:
        brgy = sub(' ', '-', brgy.lower())
        brgy = sub('\.', '', brgy)
        brgy = sub('ñ', 'n', brgy)
        urls.append(base_url + brgy + ".html")
    return urls

def get_urls():
    all_urls = []

    # Sta. Ignacia
    url_staignacia = "https://www.philatlas.com/luzon/r03/tarlac/santa-ignacia/"
    all_urls.extend(list_to_urls(url_staignacia, brgys_staignacia))

    # Sta. Clemente
    url_sanclamente = "https://www.philatlas.com/luzon/r03/tarlac/san-clemente/"
    all_urls.extend(list_to_urls(url_sanclamente, brgys_sanclemente))

    # Bayambang
    url_bayambang = "https://www.philatlas.com/luzon/r01/pangasinan/bayambang/"
    all_urls.extend(list_to_urls(url_bayambang, brgys_bayambang))

    # Mangatarem
    url_mangatarem = "https://www.philatlas.com/luzon/r01/pangasinan/mangatarem/"
    all_urls.extend(list_to_urls(url_mangatarem, brgys_mangatarem))

    return all_urls



if __name__ == "__main__":
    main()