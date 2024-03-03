
import rrytapi
import requests
from rrytapi.utils import TimeIt
import urllib
ti=TimeIt()

v=rrytapi.get_video("https://www.youtube.com/watch?v=M-mtdN6R3bQ")
print(v)
fmt=v.formats.best
url=v.formats.best._url

# ti.print("GET...")
# with requests.get(url,stream=True) as res:
#     ti.print("CONTENT...")
#     res.raise_for_status()
#     for chunk in res.iter_content(chunk_size=8192):
#         pass
# import urllib.request


output_file = 'large_file.mp4'
ti.print("GET...")
# Open the URL and download the content
with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
    # Read the data in chunks and write to the output file
    chunk_size = 4096  # Adjust the chunk size as needed
    ti.print("CONTENT...")
    while True:
        chunk = response.read(chunk_size)
        if not chunk:
            break
        out_file.write(chunk)
ti.print("DONE")
print("File downloaded successfully.")



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

