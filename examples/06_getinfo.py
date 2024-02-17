import rrytapi
from rrytapi.utils import get_info
video=rrytapi.get_video('https://www.youtube.com/watch?v=9bZkp7q19f0')

print(get_info(video))