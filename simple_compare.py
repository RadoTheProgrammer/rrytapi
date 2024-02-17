
import rrytapi
import requests
from rrytapi.utils import TimeIt

ti=TimeIt()

v=rrytapi.get_video("https://www.youtube.com/watch?v=M-mtdN6R3bQ")
url=v.formats._url

ti.print("GET...")
with requests.get(url,stream=True) as res:
    ti.print("CONTENT...")
    res.raise_for_status()
    for chunk in res.iter_content(chunk_size=8192):
        pass

ti.print("DONE")

"""
stream=False
001.012 001.012 GET...
030.007 028.995 CONTENT...
030.007 000.000 DONE

stream=True
000.829 000.829 GET...
000.865 000.036 CONTENT...
029.783 028.918 DONE

chunk_size=8192
028.916
028.977
028.918

chunk_size=1024
028.937
028.917
"""

