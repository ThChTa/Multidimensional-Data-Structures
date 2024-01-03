import re
import string
import requests
import pandas as pd
from bs4 import BeautifulSoup

import os




#get scientist dblp awards from dblp site 
def get_dblp_records(dblp_url):
    dblp_records = 0
    dblp_data = requests.get(dblp_url)
    dblp_soup = BeautifulSoup(dblp_data.text, 'html.parser')

    dblp_section = dblp_soup.find('div', id='publ-section' , class_= 'section')
    if dblp_section.find_all('li'):
        dblp_records = len(dblp_section.find_all('li', class_=lambda c: c and 'toc' in c.split()))

    return dblp_records



#get scientist's data from url

def get_scientist_data(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    #get last name 
    fullName = re.sub(r'\([^)]*\)', '', soup.find('span', class_='mw-page-title-main').text.strip())
    lastName = fullName.rsplit(maxsplit=1)[-1]

    #get total awards number
    awards = 0
    first_awards = 0 #awards found in the wiki text
    second_awards = 0 #awards found in the infobox

    #find awards from wiki text
    awards_in_text = soup.find('span', string=lambda text: text and 'awards' in text.lower()) #find awards in wikipedia text

    if awards_in_text:
        awards_list = awards_in_text.find_next('ul').find_all('li')
        first_awards += len(awards_list)

    #find awards from infobox
    infobox = soup.find('table', class_='infobox biography vcard')

    if infobox and infobox.find('th', string='Awards'):
        awards_th = infobox.find('th', string='Awards')
        awards_tr = awards_th.find_parent('tr')
        awards_td = awards_tr.find('td')
        if awards_td.find_all('li'):
            second_awards = len(awards_td.find_all('li'))
        else:
            second_awards = len(awards_td.find_all('a', attrs={'title': True}))

    awards = max(first_awards, second_awards)


    #get education
    education = ''
    education_in_text = soup.find('span', string=lambda text: text and 'education' in text.lower(), attrs={'id': True})

    if education_in_text:
        education_list = []
        next = education_in_text.find_next()
        while next and next.name not in ['h2', 'h3']:
            if next.name == 'p':
                education_list.append(next.text.strip())
            next = next.find_next()
        education = ' '.join(education_list)

    

    #get dblp_records
    dblp_records = 0 
    authority_control_box = soup.find('div', class_='navbox authority-control')

    if authority_control_box and authority_control_box.find('a', string='DBLP'):
        dblp_anchor = authority_control_box.find('a', string='DBLP')
        dblp_url = dblp_anchor.get('href')
        dblp_records = get_dblp_records(dblp_url)




    return lastName, awards, education, dblp_records





def get_scientist_urls():
    url = "https://en.wikipedia.org/wiki/List_of_computer_scientists"
    data = requests.get(url)
    soup = BeautifulSoup(data.content, "html.parser")

    scientist_urls = []

    #get Capital Letter of List
    letters = soup.find_all("span", string=lambda text: text and text in list(string.ascii_uppercase))

    for letter in letters:
        ul = letter.find_next("ul")
        if ul:
            list_data = ul.find_all("li")
            for data in list_data:
                a_href = data.find_next("a")     #first a_href in li contains scientist name
                if a_href:
                    scientist_url = 'https://en.wikipedia.org' + a_href.get("href")
                    scientist_urls.append(scientist_url)

    return scientist_urls                


print ("Extracting urls")
scientists = get_scientist_urls()
print("Done")

data = []
count = 0

print ("Extracting scientists data")

for scientist in scientists:
    lastName, awards, education, dblp_records = get_scientist_data(scientist)
    count += 1
    print(count)

    if education and (dblp_records > 0):
        data.append([lastName, awards, education, dblp_records])
print("Done")

df = pd.DataFrame(data, columns=['lastName', 'awards', 'education', 'dblp_records'])

csv_file_path = 'D:\Multidimensional-Data-Structures\Multidimensional-Data-Structures\data\scientists_data_complete.csv' # need to change for your specific file path in your pc

try:
    # Attempt to save the DataFrame to a CSV file
    df[['lastName', 'awards', 'education', 'dblp_records']].to_csv(csv_file_path, index=False)
    print("CSV file created successfully")
except Exception as e:
    print("Error occurred while saving CSV file:", e)

print(df)