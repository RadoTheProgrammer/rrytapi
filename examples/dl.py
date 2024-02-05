"""
Download a video
"""
import rrytapi
import timeit

v=rrytapi.Video.get("https://www.youtube.com/watch?v=M-mtdN6R3bQ")
print(timeit.timeit(lambda:v.download(),number=1))
#print(v.formats(140).download("))
# v.download("/Users/alain/Documents/GHRRYT.WAV")
