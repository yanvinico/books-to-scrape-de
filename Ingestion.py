# %%
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
import boto3

# %%
url = 'https://books.toscrape.com/'
response =  requests.get(url)
if response.status_code == 200:
    print('response successful')
else: 
    print('response failed')
# %%
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)

# %%
books = soup.find_all('h3')
start_time = time.time()
books_extracted = 0

for book in books:
    book_url = book.find('a')['href']
    book_response = requests.get(url + book_url)
    book_soup = BeautifulSoup(book_response.content, 'html.parser')

    title = book_soup.find('h1').text
    category = book_soup.find('ul', class_= 'breadcrumb').find_all('a')[2].text.strip()
    rating = book_soup.find('p', class_ = 'star-rating')['class'][1]
    price = book_soup.find('p', class_= 'price_color').text.strip()
    availability = book_soup.find('p', class_ = 'instock availability').text.strip()

    books_extracted += 1

    end_time = time.time()

    total_time = (end_time - start_time)/60.0

    print(f'Title: {title}\n Category: {category}\n Rating: {rating}\n Price: {price}\n Availability: {availability}\n *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+')


# %%
books_data = []

for page_num in range(1,51):
    url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('h3')
    start_time = time.time()
    books_extracted = 0

    for book in books:
        book_url = book.find('a')['href']
        book_response = requests.get('https://books.toscrape.com/catalogue/'+ book_url)
        book_soup = BeautifulSoup(book_response.content, 'html.parser')

        title = book_soup.find('h1').text
        category = book_soup.find('ul', class_= 'breadcrumb').find_all('a')[2].text.strip()
        rating = book_soup.find('p', class_ = 'star-rating')['class'][1]
        price = book_soup.find('p', class_= 'price_color').text.strip()
        availability = book_soup.find('p', class_ = 'instock availability').text.strip()

        books_extracted += 1

        end_time = time.time()

        total_time = (end_time - start_time)/60.0

        books_data.append([title, category, rating, price, availability])

        print(books_data)
        print('_+_+_+_+_+_+_+_+_+_+_+_+_+_+')
        print(f'tempo levado: {total_time:.2f} minutos')
        print('_+_+_+_+_+_+_+_+_+_+_+_+_+_+')
        print(f'{page_num*len(books)} extraidos até agora')

#%%
df = pd.DataFrame(books_data, columns=["Title", "Category", "Rating", "Price", "Availability"])
print(df.head(10))
csv_filename = "books_scraped.csv"
df.to_csv(csv_filename, index=False)

S3_BUCKET_NAME = "books-to-scrape"
S3_FOLDER_ROUTE = "Data/"

s3 = boto3.client("s3")
with open(csv_filename, "rb") as f:
    s3.upload_fileobj(f,S3_BUCKET_NAME, S3_FOLDER_ROUTE + csv_filename)
