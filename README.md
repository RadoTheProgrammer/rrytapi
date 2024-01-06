# RRYTApi
RRYTApi is a youtube api that allow you to download videos in any available format. It can also show the output of a search request, and read the content of a playlist.

This is my first real github repository that I've done. And I hope that it works. (If not, pls send an issue and i fix it! Nothing is perfect.)

To download it, use `git clone` command (maybe you already know that)
```
git clone https://github.com/RadoTheProgrammer/rrytapi; cd rrytapi
```
Don't forget to install the requirements
```
pip install -r requirements.txt
```
And now, to use it, create a python file (make sure it's in rrytapi's folder) and import `rryt`

## Usage
To download a video:
```python
import rryt
v=rryt.Video.get(<video url>)
v.download()
```
You can see it's really simple to use. Normally it'll put in a folder called rrytapi_downloads.

You can also download the audio of a video with
```python
v.formats.audio.download()
```
To display all available formats, just use
```python
print(v.formats)
```

