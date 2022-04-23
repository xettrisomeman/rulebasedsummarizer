#type: ignore


from bs4 import BeautifulSoup
import requests



def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml", from_encoding="utf-8")
    return soup

