"""
To provide an user interface allow you to search and download videos from youtube
"""
import rrytapi
while True:
    a=input("Type a request or a url\n")
    if not a:continue
    if not a.startswith("https://") or a.startswith("http://"):
        r=rrytapi.search(a)
        print(r)
        a=int(input("Choose a video id:"))
        v=r[a].get()
    else:
        v=rrytapi.get_video(a)
    
    v.formats[18].download()
