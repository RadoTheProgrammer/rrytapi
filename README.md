# RRYTApi

RRYTApi is a youtube api that allow you to download videos in any available format. It can also show the output of a search request, and read the content of a playlist.

This is my first real github repository that I've done. And I hope that it works. (If not, pls send an issue and i fix it! Nothing is perfect.)

To download it, use `git clone` command (maybe you already know that)

```
git clone https://github.com/RadoTheProgrammer/rrytapi
cd rrytapi
```

## Installation

After git cloned the repository, you can run the following command to install:

```
pip install .
```


## Usage

To download a video:

```python
import rrytypi
v=rrytypi.Video.get(<video url>)
v.download()
```

To download the audio of a video:

```python
v.formats.audio.download()
```

To display all available formats, just use

```python
print(v.formats)
```
