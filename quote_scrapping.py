import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice

#Scrapping functions

def quote_scrap(params = ""):
	sleep(2)
	url = "http://quotes.toscrape.com" + params
	response = requests.get(url)
	print(f"Now Scrapping {url}...")
	html = response.text
	soup = BeautifulSoup(html,"html.parser")
	return soup

def extract_quotes(soup):
	span_quotes = soup.find_all("span", class_ = "text")
	for span in span_quotes:
		quotes.append(span.get_text())
	
def extract_authors(soup):
	small_authors = soup.find_all("small", class_ = "author")
	for small in small_authors:
		authors.append(small.get_text())

def author_about_links(soup):
	for small in soup.find_all("small", class_ = "author"):
		a_about = small.find_next_sibling()
		about_authors_links.append(a_about["href"])

def new_page(soup):
	li_next = soup.find("li", class_ = "next")
	if li_next:
		a_next = li_next.find("a")
		a_href = a_next["href"]
		next_soup = quote_scrap(a_href)
		return next_soup
	return "No More pages available"

#Game functions

def get_author_bio(bio_link):
	bio_soup = quote_scrap(bio_link)
	born = bio_soup.find("span", class_ = "author-born-date").get_text()
	born_location = bio_soup.find("span", class_ = "author-born-location").get_text()
	return f"The author was born on {born} {born_location}"

def author_first_name(author):
	return f"The author's first name starts with {author[0]}"

def author_last_name(author):
	temp = author.split(" ")
	return f"The author's last name starts with {temp[-1][0]}"

#initialization

quotes  = []
authors = []
about_authors_links = []

#initial page

soup = quote_scrap()
extract_quotes(soup)
extract_authors(soup)
author_about_links(soup)

#New pages

for i in range(1,11):
	soup = new_page(soup)
	if isinstance(soup, str):
		print(soup)
		break
	extract_quotes(soup)
	extract_authors(soup)
	author_about_links(soup)

#Actual Guessing game

game_init =list(zip(quotes,authors,about_authors_links))

print("Here's a quote :")

chances = 4
while chances > 0:
	if chances == 4:
		random_quote = choice(game_init)
		current_author = random_quote[1]
		current_quote = random_quote[0]
		print(f"\n{current_quote}")
	print(f"\nWho said this? Guesses remaining: {chances}. ")
	user_guess = str(input())
	if user_guess.lower() == current_author.lower():
		print("\nYou Guessed Correctly! Congratulations!!")
	elif chances == 4:
		print(f"\nHere's a Hint : {get_author_bio(random_quote[2])}")
		chances -= 1
		continue
	elif chances == 3:
		print(f"\nHere's a Hint : {author_first_name(current_author)}")
		chances -= 1
		continue
	elif chances == 2:
		print(f"\nHere's a Hint : {author_last_name(current_author)}")
		chances -= 1
		continue
	else:
		print(f"\nSorry You've ran out of guesses. The answer was {current_author}")
	
	play_again = str(input("\nWould you like to play again (y/n)? ")).lower()
	if play_again[0] == "y":
		chances = 4
		print("\nGreat! Here we go....")
		print("\nHere's a quote :")
		continue
	else:
		print("\nOk! See you next time!\n")
		break