import requests
from bs4 import BeautifulSoup
from optparse import OptionParser

HOST = "https://www.musica.com/letras.asp?t2="

def conection (url):
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        content = response.text
        content = content.replace('<br>','\n')
        soup = BeautifulSoup(content,'html.parser')
        return soup
    else:
        print("There's not server response")
        exit(0)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n","--name",action="store",type="string",dest="song_name")
    (options,args) = parser.parse_args()
    song_name = options.song_name.replace(" ","+")
    soup = conection(''.join([HOST,song_name]))
    table = soup.find('table',{'class':'rst'})
    songs_table = table.find_all('tr')[3].find('table')
    songs_desc = songs_table.find_all('td')[1:-2:2]

    print('\n\nResults for: "',song_name.replace("+"," "),'"')
    i = 1 
    songs_url = []
    for artist in songs_desc:
        print(i,'.',artist.a.b.text,':',artist.a.get('href'))
        songs_url.append(artist.a.get('href'))
        i+=1
    option = int(input('Press your number option:'))

    print('\n\nLyrics:\n')
    soup2 = conection(songs_url[option-1])
    lyrics = soup2.find('div',{'id':'letra'}).find_all('p')
    for sentence in lyrics:
        print(sentence.text)