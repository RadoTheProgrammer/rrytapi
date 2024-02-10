import rrytapi,requests
ti=rrytapi.TimeIt()
v=rrytapi.Video.get("https://www.youtube.com/watch?v=M-mtdN6R3bQ")
url=v.formats.url

ti.print("GET...")
a=requests.get(url)
ti.print("CONTENT...")
b=a.content
ti.print("DONE")

