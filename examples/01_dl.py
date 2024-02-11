"""
Download a video
"""
import rrytapi
v=rrytapi.Video.get("https://www.youtube.com/watch?v=M-mtdN6R3bQ")
v.download()

