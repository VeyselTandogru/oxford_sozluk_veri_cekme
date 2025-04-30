import requests
from bs4 import BeautifulSoup
import json

url = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford3000-5000"
url2 = "https://www.oxfordlearnersdictionaries.com"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.0"
}

response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.text,"html.parser")
kelime = soup.select("ul.top-g li")
deneme = []
for i in kelime:
    word = i.get('data-hw')
    div = i.find('div')
    dil_bilgisi = i.find('span')
    dil_bilgileri = [j.get_text(strip= True) for j in dil_bilgisi][0]
    a_href = i.find('a')
    href = a_href.get('href')
    if div:
        spans = div.find_all('span')
        span_içerik = [span.get_text(strip= True) for span in spans]
        deneme.append(word.capitalize() + " " + str(span_içerik).strip("'[]").upper() + " " + str(dil_bilgileri).strip("'[]")) 
    else:
        continue

    yeni_link = "https://www.oxfordlearnersdictionaries.com" + href
    response2 = requests.get(yeni_link, headers=headers)
    soup2 = BeautifulSoup(response2.text,"html.parser")
    
    ul = soup2.find('ul', attrs= {"class":"examples"}) 
    örnekler = [j.get_text(strip= True) for j in ul][:4] if ul else []

    veri = {
        "kelime": word.capitalize(),
        "kategori": " ".join(span_içerik).upper(),
        "dil_bilgisi": dil_bilgileri,
        "örnekler": örnekler
    }

    print(veri)
    with open('info.json', 'r+', encoding='UTF-8') as dosya:
        x = json.load(dosya)                    
        x.append(veri)                 
        dosya.seek(0)                           
        json.dump(x, dosya, ensure_ascii=False, indent=4)  
