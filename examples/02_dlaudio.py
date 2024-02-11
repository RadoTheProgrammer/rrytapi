"""
Download an audio
"""
import rrytapi
v=rrytapi.get_video("https://www.youtube.com/watch?v=M-mtdN6R3bQ")
v.formats.audio.download()