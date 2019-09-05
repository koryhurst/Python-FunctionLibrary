#BeautifulSoup Functions
import requests
import urllib.request

from bs4 import BeautifulSoup

def GetLinkListOLD(UrlToSearch, SearchTerm): #or searchtermSSSS at some point
  #I am only keeping this as the Nanaimo Chamber had some malformed HTML I think
  # Connect to the URL
  response = requests.get(UrlToSearch)
  #print(response.text)
  # Parse HTML and save to BeautifulSoup object¶
  soup = BeautifulSoup(response.text, "html.parser")
  linklist = []
  # To download the whole data set, let's do a for loop through all a tags
  #print(soup.findAll('a'))
  for i in range(36, len(soup.findAll('a')),1): #'a' tags are for links
    one_a_tag = soup.findAll('a')[i]
    link = one_a_tag['href']
    #print(SearchTerm)
    if SearchTerm == -1:
      print('Test')
      linklist.append(link)
    else:
      if SearchTerm in link:
        linklist.append(link)
      
  return linklist

def GetLinkList(UrlToSearch, SearchTerm):
  linklist = []
  response = requests.get(UrlToSearch)
  #print(response.text)
  #print(response.text)
  # Parse HTML and save to BeautifulSoup object¶
  soup = BeautifulSoup(response.text, "html.parser")
  #print(soup.find_all('a'))
  
  for link in soup.find_all('a'):
    #On The Nanaimo Chamber website, there are some 'a' tags without a reference
    linktext = link.get('href')
    if SearchTerm == -1:
      linklist.append(linktext)
    else:
      if SearchTerm in linktext:
        linklist.append(linktext)

  return linklist

def GetSoup(UrlToGet):
  response = requests.get(UrlToGet)
  #print(response.text)
  # Parse HTML and save to BeautifulSoup object¶
  soup = BeautifulSoup(response.text, "html.parser")
  return soup
  
def SearchSoup(UrlToSearch, SearchTerm): #or searchtermSSSS at some point
  # Connect to the URL
  response = requests.get(UrlToSearch)
  #print(response.text)
  # Parse HTML and save to BeautifulSoup object¶
  soup = BeautifulSoup(response.text, "html.parser")
  return soup.findAll(SearchTerm)

def ShowPrettySoup(UrlToShow):
  response = requests.get(UrlToShow)
  #print(response.text)
  # Parse HTML and save to BeautifulSoup object¶
  soup = BeautifulSoup(response.text, "html.parser")
  print(soup.prettify)

def ShowLinks(UrlToShow):
  response = requests.get(UrlToShow)
  #print(response.text)
  # Parse HTML and save to BeautifulSoup object¶
  soup = BeautifulSoup(response.text, "html.parser")
  #print(soup.find_all('a'))
  for link in soup.find_all('a'):
    print(link.get('href'))

def GetSiteMap(BaseURL):
  #ShowLinks(BaseURL)

  LinksAlreadyChecked = []
  LinksAlreadyChecked.append(BaseURL)
  #print(LinksAlreadyChecked)

  #print(BaseURL)
  NewLinks = GetLinkList(BaseURL, -1)
  #print(len(NewLinks))
  print(NewLinks)
  for Link in NewLinks:
    #need an additional check for external links
    #print(Link[0:4])
    #Starting an exception list
    #Checking: http://www.feldercanada.comindex
    if Link[0:4] != 'http':
      if Link[0:len(BaseURL)] != BaseURL:
        if Link[0:1] != '/':
          LinkToCheck = BaseURL + '/' + Link
        else:
          LinkToCheck = BaseURL + Link
        if LinkToCheck in LinksAlreadyChecked:
          print('Already Checked: ' + LinkToCheck) 
          NewLinks.remove(Link)
        else:
          print('Checking: ' + LinkToCheck)
          GetMoreNewLinks = GetLinkList(LinkToCheck, -1)
          for NewerLink in GetMoreNewLinks:
            NewLinks.append(NewerLink)
          LinksAlreadyChecked.append(LinkToCheck)
    #else:
      #I guess for completeness The base URl should be checked it could be a local link with a full address, but my hunch is that those would be covered by relative links
      #print('Possible External Link (not Checking):')
      
  #print(LinksAlreadyChecked)
  return LinksAlreadyChecked
