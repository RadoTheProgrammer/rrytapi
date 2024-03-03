"""
Download a video
"""
import rrytapi
from rrytapi.utils import get_info
v=rrytapi.get_video("https://youtube.com/watch?v=QegcGsE9tYE")
#v.formats.download()
#print(v.formats.filtrer(lambda x:x.itag==18))
#print(v.formats)
#print(v.formats.audio.bestwithvideo)
print(v.formats)
#fmt=v.formats[394]
#print(get_info(fmt))
#print(get_info(v.formats(18)))
# from the formats, i should only capture the minimal: mimeType, bitrate, hasAudio, size
# example of a format output: <Format#18: video/mp4 352.7KBit/s, 640x360, 44100Hz (low)>

# <Stream: itag="18" mime_type="video/mp4" res="360p" fps="24fps" vcodec="avc1.42001E" acodec="mp4a.40.2" progressive="True" type="video">
# <Stream: itag="22" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.64001F" acodec="mp4a.40.2" progressive="True" type="video">
# <Stream: itag="137" mime_type="video/mp4" res="1080p" fps="24fps" vcodec="avc1.640028" progressive="False" type="video">
# <Stream: itag="248" mime_type="video/webm" res="1080p" fps="24fps" vcodec="vp9" progressive="False" type="video">
# <Stream: itag="136" mime_type="video/mp4" res="720p" fps="24fps" vcodec="avc1.4d401f" progressive="False" type="video">
# <Stream: itag="247" mime_type="video/webm" res="720p" fps="24fps" vcodec="vp9" progressive="False" type="video">
# <Stream: itag="135" mime_type="video/mp4" res="480p" fps="24fps" vcodec="avc1.4d401e" progressive="False" type="video">
# <Stream: itag="244" mime_type="video/webm" res="480p" fps="24fps" vcodec="vp9" progressive="False" type="video">
# <Stream: itag="134" mime_type="video/mp4" res="360p" fps="24fps" vcodec="avc1.4d4015" progressive="False" type="video">
# <Stream: itag="243" mime_type="video/webm" res="360p" fps="24fps" vcodec="vp9" progressive="False" type="video">
# <Stream: itag="133" mime_type="video/mp4" res="240p" fps="24fps" vcodec="avc1.4d400d" progressive="False" type="video">
# <Stream: itag="242" mime_type="video/webm" res="240p" fps="24fps" vcodec="vp9" progressive="False" type="video">
# <Stream: itag="160" mime_type="video/mp4" res="144p" fps="24fps" vcodec="avc1.4d400b" progressive="False" type="video">
# <Stream: itag="278" mime_type="video/webm" res="144p" fps="24fps" vcodec="vp9" progressive="False" type="video">
# <Stream: itag="139" mime_type="audio/mp4" abr="48kbps" acodec="mp4a.40.5" progressive="False" type="audio">
# <Stream: itag="140" mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2" progressive="False" type="audio">
# <Stream: itag="249" mime_type="audio/webm" abr="50kbps" acodec="opus" progressive="False" type="audio">
# <Stream: itag="250" mime_type="audio/webm" abr="70kbps" acodec="opus" progressive="False" type="audio">
# <Stream: itag="251" mime_type="audio/webm" abr="160kbps" acodec="opus" progressive="False" type="audio">
