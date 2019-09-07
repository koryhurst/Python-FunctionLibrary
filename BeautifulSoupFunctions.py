#BeautifulSoup Functions
import requests
import urllib.request
import mysql.connector

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

def GetSiteMap(BusinessID, BaseURL, DatabaseDetails):
  
  #Database details should be a list like this  ["localhost","user","passwd","database="]
  mydb = mysql.connector.connect(
    host=DatabaseDetails[0],
    user=DatabaseDetails[1],
    passwd=DatabaseDetails[2],
    database=DatabaseDetails[3]
    )
  sqlCheck = "select count(*) from tblWebPage where URL = '"
  sqlInsert = "INSERT INTO tblwebpage (BusinessID, URL) VALUES (%s, %s)"

  #AllLinks = []
  
  
  #print('BaseURL:' + BaseURL)
  NewLinks = GetLinkList(BaseURL, -1)
  ActualDomain = BaseURL[BaseURL.find('//') + 2 : len(BaseURL)]
  #print('ActualDomain:' +  ActualDomain)
  #print(len(NewLinks))
  #print(NewLinks)
  for Link in NewLinks:
      #need an additional check for external links
      #print(Link[0:4])
      #Starting an exception list
      #Checking: http://www.feldercanada.comindex
    if Link is not None:
      #First is it it fully formed.  If not, form it.
      if Link[0:4] != 'http':
        #Some relative links contain the '/' some don't (others contain a leading '#')
        if Link[0:1] != '/':
          LinkToCheck = BaseURL + '/' + Link
        else:
          LinkToCheck = BaseURL + Link
      else:
        LinkToCheck = Link

      #there are some sites that have too pages with many parameters 
      #see www.ablerecognition.com  their whole catalogue is there 
      #so lets try removing the parameters
      if LinkToCheck.find("?") > 0:
        LinkToCheck = LinkToCheck[0:LinkToCheck.find("?")]

      #now, if that fully formed link is in the domain
      #All the ones that we formed above will automatically pass this
      if LinkToCheck.find(ActualDomain) > 0:
        #now it should be within this site somewhere
        #have we checked it before
        mycursorCheck = mydb.cursor()
        sqlCheckThisPage = sqlCheck + Link + "'"
        mycursorCheck.execute(sqlCheckThisPage)
        myresult = mycursorCheck.fetchall()
        print(myresult)
        mycursorCheck.close()
        wait = input("PRESS ENTER TO CONTINUE")
        if myresult[0] == 1:
          print('Already Checked: ' + LinkToCheck) 
          NewLinks.remove(Link)
        #if not check it
        else:
          print('Checking: ' + LinkToCheck)
          GetMoreNewLinks = GetLinkList(LinkToCheck, -1)
          for NewerLink in GetMoreNewLinks:
            NewLinks.append(NewerLink)
          #sqlInsertThis = sqlInsert + LinkToCheck + "')"
          #print(sqlInsertThis)
          InsertValues = (BusinessID, LinkToCheck)
          myCursorInsert = mydb.cursor()
          print(InsertValues)
          print("TryingInsert")
          myCursorInsert.execute(sqlInsert, InsertValues)
          print("Tried")
          mydb.commit()
          print(myCursorInsert.rowcount, "record inserted.")
          myCursorInsert.close()
          NewLinks.remove(Link)

      #else:
        #I guess for completeness The base URl should be checked it could be a local link with a full address, but my hunch is that those would be covered by relative links
        #print('Possible External Link (not Checking):')
        
    #print(LinksAlreadyChecked)
