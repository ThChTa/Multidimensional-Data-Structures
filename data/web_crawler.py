import re
import string
import requests
import pandas as pd
from bs4 import BeautifulSoup

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

    return lastName, awards, education



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



# lastName, awards, education = get_scientist_data("https://en.wikipedia.org/wiki/Scott_Aaronson")
print ("Extracting urls")
scientists = get_scientist_urls()
print("Done")

data = []

print ("Extracting scientists data")

for scientist in scientists:
    lastName, awards, education = get_scientist_data(scientist)

    if education:
        data.append([lastName, awards, education])
print("Done")

df = pd.DataFrame(data, columns=['lastName', 'awards', 'education'])

df[['lastName', 'awards', 'education']].to_csv('scientist_data.txt', index=False)

print(df)

