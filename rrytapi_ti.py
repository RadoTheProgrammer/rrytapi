import rrytapi
from rrytapi.utils import TimeIt
ti=TimeIt()
video=rrytapi.get_video("https://www.youtube.com/watch?v=PEM0Vs8jf1w")
ti.print("get_video")
video.formats.sort(key=lambda x:x.itag)
print(video.formats)
print(fmt)
fmt.download()
ti.print("formats[22].download()")

# [
#    <Format#18 video/mp4 275.9KBit/s 360p(medium) 44100Hz(low),
#    <Format#133 video/mp4 186.2KBit/s 240p(small),
#    <Format#134 video/mp4 354.4KBit/s 360p(medium),
#    <Format#135 video/mp4 546.9KBit/s 480p(large),
#    <Format#136 video/mp4 1.0MBit/s 720p(hd720),
#    <Format#137 video/mp4 5.9MBit/s 1080p(hd1080),
#    <Format#140 audio/mp4 130.5KBit/s 44100Hz(medium),
#    <Format#160 video/mp4 105.1KBit/s 144p(tiny),
#    <Format#242 video/webm 222.8KBit/s 240p(small),
#    <Format#243 video/webm 409.4KBit/s 360p(medium),
#    <Format#244 video/webm 703.4KBit/s 480p(large),
#    <Format#247 video/webm 1.1MBit/s 720p(hd720),
#    <Format#248 video/webm 2.5MBit/s 1080p(hd1080),
#    <Format#249 audio/webm 70.4KBit/s 48000Hz(low),
#    <Format#250 audio/webm 92.0KBit/s 48000Hz(low),
#    <Format#251 audio/webm 180.1KBit/s 48000Hz(medium),
#    <Format#278 video/webm 97.5KBit/s 144p(tiny),
#    <Format#394 video/mp4 84.1KBit/s 144p(tiny),
#    <Format#395 video/mp4 187.3KBit/s 240p(small),
#    <Format#396 video/mp4 375.7KBit/s 360p(medium),
#    <Format#397 video/mp4 614.9KBit/s 480p(large),
#    <Format#398 video/mp4 996.4KBit/s 720p(hd720),
#    <Format#399 video/mp4 2.4MBit/s 1080p(hd1080)
# ]

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