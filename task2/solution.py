import csv
from collections import defaultdict

import requests
from bs4 import BeautifulSoup

RUSSIAN_LETTERS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'

def get_animals_by_letter():
    url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    
    letter_counts = defaultdict(int)
    
    while url:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Что то сломалось на странице {url}\nКод ошибки: {response.status_code}")
        
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content = soup.find('div', {'id': 'mw-pages'})
        
        namings = content.find_all('li')
        
        for naming in namings:
            naming_text = naming.text.strip()
            if naming_text and naming_text[0] in RUSSIAN_LETTERS:
                letter_counts[naming_text[0]] += 1
        
        next_page = soup.find('a', string='Следующая страница')
        url = f"https://ru.wikipedia.org{next_page['href']}" if next_page else None
    
    return letter_counts

def save_to_csv(letter_counts):
    sorted_letters = sorted(letter_counts.keys(), key=lambda x: RUSSIAN_LETTERS.index(x))
    
    with open('beasts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted_letters:
            writer.writerow([letter, letter_counts[letter]])

def main():
    letter_counts = get_animals_by_letter()
    save_to_csv(letter_counts)

if __name__ == "__main__":
    main()
