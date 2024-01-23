from bs4 import BeautifulSoup
def htmlsoup(content):
    #print(content)
    if isinstance(content,BeautifulSoup):return content
    return BeautifulSoup(content,"html.parser")
def fromfile(file):
    with open(file) as f:
        return htmlsoup(f.read())
def fromurl(url):
    import requests
    res=requests.get(url)
    return htmlsoup(res.text)
def saveinfile(content,file="content.html"):
    with open(file,"w") as f:
        f.write(htmlsoup(content).prettify())
#print(fromfile("/Volumes/RRUSB/Rhtml/mywebpage/main.html"))
content=fromfile("/Volumes/RRUSB/Rhtml/mywebpage/main.html")
#print(content)

saveinfile(content)