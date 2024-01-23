"""
Download a video
"""
import rrytapi
import timeit

v=rrytapi.Video.get("https://www.youtube.com/watch?v=p7NKqVJzH4E")
print(timeit.timeit(lambda:v.download(),number=1))
#print(v.formats(140).download("))
# v.download("/Users/alain/Documents/GHRRYT.WAV")
