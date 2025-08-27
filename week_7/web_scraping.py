import requests
from bs4 import BeautifulSoup
import sqlite3

# Web scraping quotes and authors from a website and saving them to a SQLite database using the same structure as the CSV example provided in week 4 assignment.


url = "http://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = []
authors = []

for quote in soup.find_all("span", class_="text"):
    quotes.append(quote.get_text())

for author in soup.find_all("small", class_="author"):
    authors.append(author.get_text())

conn = sqlite3.connect('quotes.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS quotes
             (quote TEXT, author TEXT)''')

for quote, author in zip(quotes, authors):
    c.execute("INSERT INTO quotes (quote, author) VALUES (?, ?)", (quote, author))
conn.commit()

c.execute("SELECT COUNT(*) FROM quotes")
print("Total quotes saved:", c.fetchall()[0][0])

c.execute("SELECT rowid, quote, author FROM quotes")
rows = c.fetchall()
for row in rows:
    print(f"{row[0]}: {row[1]} — {row[2]}")

conn.close()
