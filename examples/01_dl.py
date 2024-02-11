"""
Download a video
"""
import rrytapi
v=rrytapi.get_video("https://youtube.com/watch?v=QegcGsE9tYE")
v.formats(251).download()

