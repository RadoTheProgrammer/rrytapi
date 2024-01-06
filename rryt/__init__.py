
"""
Requirements
clean-text
Js2Py
requests
"""

#print(globals())
import time
import sys
from .dataprint import printer,saveinfile
import requests
import re
import json
import subprocess
import os
import random
import unicodedata
import string
import mimetypes
from cleantext import remove_emoji
from functools import partial
import webbrowser
import builtins
from string import Formatter
from .player import Player
from mini_lambda import x,Constant
import urllib,os


class TimeIt:
    def __init__(self):
        self.start()
    def start(self):
        self.stt=self.tt=time.time()
    def print(self,txt):
        tt=time.time()
        print("%07.3f %07.3f %s"%(tt-self.stt,tt-self.tt,txt))
        self.tt=tt

class Repr:
    def __init__(self,txt):self.txt=txt
    def __repr__(self):return self.txt

formatter=Formatter()

ti=TimeIt()
sys.path[0]=""
defaultFileDest=Repr("self.defaultFileDest")
acceptLang={"Accept-Language": "en-US"}


def attrError(obj,name):
    return AttributeError("%s object has no attribute %s"%(repr(type(obj).__name__),repr(name)))

function=type(attrError)

#assert 0,DLDIR
YT="https://youtube.com"
YTWATCH=YT+"/watch?v="
YTPLAYLIST=YT+"/playlist?list="

class LambdasError(Exception):pass

filenameChars = "-_.%s%s" % (string.ascii_letters, string.digits)

def to_filename(s):
    return "".join(c if c in filenameChars else "-" for c in unicodedata.normalize("NFKD",s))

def ajson(data):
    saveinfile(data)
    assert 0


def asfunc(lambdaOrFunc):
    try:return lambdaOrFunc.evaluate
    except:
        if lambdaOrFunc is None:return lambda v=None,*a,**k:v
        return lambdaOrFunc
    
def printerr(err):
    print(err,file=sys.stderr)

def errToStr(err):
    return "%s: %s"%(type(err).__name__,", ".join(err.args))

def lambdas(xValue,lambdasExpr,endFunc=None,errmode="print",funcVerifIfSame=None):
    if not funcVerifIfSame:funcVerifIfSame=lambda x,y:x==y
    funcVerifIfSame=asfunc(funcVerifIfSame)
    endFunc=asfunc(endFunc)
    errfunc=errmode
    if errmode in (print,"print",printerr):errfunc=printerr
    elif errmode=="raise":
        def errfunc(err):
            print("DSNFOISNFOISFI")
            raise err
        #print("WWWWDGG")
    elif type(errmode) in (type,function):errfunc=errmode
    errfunc=asfunc(errfunc)
    for lambdaExpr in lambdasExpr if type(lambdasExpr) in (list,tuple) else (lambdasExpr,):
        func=None
        if type(lambdaExpr) in (list,tuple):
            lambdaExpr,func=lambdaExpr
            
        func=asfunc(func)
        try:value=asfunc(func)(endFunc(asfunc(lambdaExpr)(xValue)))
        except Exception as err:
            #print((asfunc(lambdaExpr)(xValue)))
            errfunc(LambdasError("%s: %s"%(repr(lambdaExpr),errToStr(err))))
            continue
        else:
            #print(avalue)
            try:avalue
            except:pass
            else:
                if not funcVerifIfSame(avalue,value):
                    errfunc(LambdasError("\n%s: %s\n!=\n%s: %s\n\n"%(repr(aLambdaExpr),repr(avalue),repr(lambdaExpr),repr(value))))
        avalue=value
        aLambdaExpr=lambdaExpr
    try:
        if not value:pass
            #print("INVALID")
            #print(value)
            
        return value
    except:pass
    raise LambdasError("Failed extract value")


"""
value=lambdas(2,x+"",x/0,errmode="print")

assert 0
def tryout(*accessFunctions,errmode="raise",verifIfSame=None):
    if not verifIfSame:verifIfSame=lambda x,y:x==y
    if errmode in (print,"print",mypkg.printerr):errfunc=mypkg.printerr
    elif errmode=="raise":
        def errfunc(err):raise err
    elif type(errmode) in (type,function):errfunc=errmode
    elif not errmode:errfunc=lambda *a,**k:None
    for id,func in enumerate(accessFunctions):
        try:value=func()
        except Exception as err:errfunc(TryOutError("#%s: %s"%(id,mypkg.errToStr(err))))
        try:avalue
        except:pass
        else:
            if not verifIfSame(avalue,value):
                errfunc(TryOutError("#%s & #%s: %s != %s"%(id-1,id,avalue,value)))
        avalue=value
    return value

"""
def showInExplorerFunc(file):
    
    if sys.platform=="darwin":
        cmd="open -R %s"%repr(file)
    elif sys.platform=="win32":
        cmd='explorer /select, "%s"'%file
    else:
        return
    #print(cmd)
    return subprocess.call(cmd,shell=True)

def bcptr(link):
    return link+"&bcptr=9999999999&has_verified=1"

def aliasprop(name):
    prop=[]
    exec("prop.append(property(lambda self:self.%s))"%name)
    return prop[0]

def tname(cls):
    if type(cls)!=str:
        t=type(cls)
        if t!=type:
            cls=t
        cls=cls.__name__
    return cls
def reprWithCls(string,cls):
    return "<%s: %s>"%(tname(cls),string)

def printerWithCls(data,cls):
    return reprWithCls("\n"+printer(data),cls)

def formatWithAttrs(string,fmt):
    s=""
    for strg,key,_,_ in formatter.parse(string):
        #attr=[]
        #exec("attr.append(%s)"%key)
        if key:key=str(eval(key))
        else:key=""
        s+=strg+key
    return s


#def removeEmojis(text):
#    return emojiPattern.sub(r'',text)
#remove_emoji=removeEmojis
class BytesCount(int):
    bNotation="bytes"
    def display(self,ndigits=1):
        value=1
        contentLength=int(self)
        for key,maxvalue in (
                          (self.bNotation, 1000),
                          ("KB",    1000000),
                          ("MB",    1000000000),
                          ("GB",    1000000000000)):
            if contentLength<maxvalue:
                key=key
                break
            value=maxvalue
        div=contentLength/value
        div=round(div,ndigits)
        if not ndigits:div=int(div)
        
        return str(div)+key
    def __repr__(self):return self.display()
    def __str__(self):return self.display()

class BitCount(BytesCount):
    bNotation="bit"
    def display(self,ndigits=1):
        return super().display(ndigits)+"it"
    
class Bitrate(BitCount):
    def display(self,ndigits=1):
        return super().display(ndigits)+"/s"
    
def tryexec(func,tries=3,wait=1):
    for _ in range(tries):
        try:return func()
        except Exception as e:
            err=e
            time.sleep(wait)
    raise err

class ContentLengthError(Exception):pass
class Url:

    def __init__(self,url,defaultFileDest=None):
        url=str(url)
        if url.startswith("/"):url=YT+url
        if url.startswith("http://"):
            url="https"+url[4:]
        if url.startswith("https://www."):
            url="https://"+url[12:]
        self.url=url
        #print(url)
        self.defaultFileDest=defaultFileDest
        

        

    def __repr__(self):
        return "<Url %s>"%repr(self.url)
    def __str__(self):
        if type(self)==Url:
            return self.url
        return repr(self)
    def __eq__(self,url):
        return str(self)==str(url)
    def getContentLength(self,tries=3,wait=0):
        url=self.url
        #print("TRY2")
        #print(self)
        for _ in range(tries):
            try:
                for _ in range(1):
                    #print("TRY")
                    #requests.get(url,stream=True)
                    #print(url)
                    #print("WW")
                    #ti.print("request....")
                    res=requests.head(url)
                    #ti.print("requested")
                    res.raise_for_status()
                    headers=res.headers
                    """
                    try:url=headers["location"]
                    except:pass
                    else:continue
                    """
                    contentLength=BytesCount(headers['content-length'])
                    assert contentLength
                    return contentLength
            except Exception as e:
                #print("TOUT")
                time.sleep(wait)
                #print(self.url)
                err=e
        try:raise err
        except Exception as err:
            #print("ERROR: %s"%err)
            raise ContentLengthError("Cannot extract the contentLength")

    def wb_open(self):
        webbrowser.open(str(self))

class Duration(int):
    def __new__(cls,duration):
        if type(duration)==str:
            seconds,minutes,hours=cls.split(duration)
            duration=hours*3600+minutes*60+seconds
        return super().__new__(cls,duration)
    def __repr__(self):
        r="%s:%s"%(str(self.minutes).rjust(2,"0"),str(self.seconds).rjust(2,"0"))
        if self.hours:return "%s:%s"%(str(self.hours).rjust(2,"0"),r)
        return r
    @property
    def hours(self):return self.totalMinutes//60
    @property
    def minutes(self):return self.totalMinutes%60
    @property
    def seconds(self):return self%60
    @property
    def totalSeconds(self):return int(self)
    @property
    def totalMinutes(self):return self.totalSeconds//60
    @staticmethod
    def split(duration):
        m=map(int,duration.split(":")[::-1])
        parts=list(m)
        while len(parts)<3:parts.append(0)
        return parts
        
    __str__=__repr__
#duration=Duration("10:56:22")
#print(duration)
#assert 0
class Size:
    def __init__(self,width,height):
        self.width=int(width)
        self.height=int(height)
    def __repr__(self):
        return str(self.width)+"x"+str(self.height)
    def __iter__(self):return iter((self.width,self.height))

    def __lt__(self,size):
        size=Size(*size)
        return (self.width,self.height)<(size.width,size.height)



class QualityLabel:
    def __init__(self,qualityLabel):
        if type(qualityLabel)==int:qualityLabel=str(qualityLabel)
        qualityLabel=qualityLabel.split("p")
        self.qualityPixels=int(qualityLabel[0])
        try:
            self.fps=int(qualityLabel[1])
            assert self.fps
        except:
            self.fps=None
    def __repr__(self):
        return "%sp%s"%(self.qualityPixels,self.fps if self.fps else "")
class VideoQuality:
    def __init__(self,qualityType,qualityLabel):
        self.qualityType=qualityType
        self.qualityLabel=QualityLabel(qualityLabel)
    type=aliasprop("qualityType")
    qualityPixels=pixels=aliasprop("qualityLabel.qualityPixels")
    fps=aliasprop("qualityLabel.fps")
    def __repr__(self):
        return str(self.qualityLabel)+" ("+self.qualityType+")"
class AudioQuality:
    def __init__(self,qualityType,sampleRate):
        self.qualityType=qualityType.lower().replace("audio_quality_","")
        self.sampleRate=int(sampleRate)
    type=aliasprop("self.qualityType")
    def __repr__(self):
        return str(self.sampleRate)+"Hz ("+self.qualityType+")"
class Thumbnail(Url):
    def __init__(self,thData,name=""):
        try:
            self.size=Size(thData["width"],thData["height"])
        except:print(thData)
        self.name=name
        super().__init__(thData["url"])
    width=aliasprop("size.width")
    height=aliasprop("size.height")
    def __repr__(self):
        return "<Thumbnail "+str(self.size)+">"
class Thumbnails(list):
    #size=videoQuality=videoQualityType=width=height=pixels=qualityLabel\
    #    =qualityType=fps=
    def __init__(self,*thumbnails,name=""):
        super().__init__()
        self.access={}
        self.name=name
        for ths in thumbnails:
            self.add(ths)
    def add(self,thumbnails):
        while type(thumbnails)==dict:
            thumbnails=thumbnails.get("thumbnail") or thumbnails.get("thumbnails")
        def setitem(d,item,value):
            if item in d:return
        for th in thumbnails:


            if type(th)!=Thumbnail:th=Thumbnail(th,self.name)
            for i in (th.width,th.height,th.width*th.height):
                if i in self.access:continue
                self.access[i]=th
            self.append(th)
        
    def __repr__(self):
        return printer(list(self))
    def __getitem__(self,item):
        try:return self.access[item]
        except:return list(self)[item]


def convert_audio(input_file,output_file="{input_file}.{ext or 'mp3'}",ext=None):
    from pydub import AudioSegment
    output_file=eval("f"+repr(output_file),locals()) #pylint: disable=W0123
    print(output_file)
    if not ext:
        ext=os.path.splitext(output_file)[1].lstrip(".")
    audio=AudioSegment.from_file(input_file)
    audio.export(output_file,format=ext)



class Format(Url):
    size=videoQuality=videoQualityType=width=height=pixels\
    =qualityLabel=qualityType=fps=audioQuality=sampleRate=audioQualityType\
    =None
    def __init__(self,video,fmtData):
        self.video=video
        #ti.print("HELLO")
        with Info(self) as info:
            info.itag=int(fmtData["itag"])
            #print("Format %s"%info.itag)
            self._fmtData=fmtData
            protected=False
            #print("VVVVV%s"%self.video.url)
            try:
                self.url=fmtData["url"]
            except:
                #print("decrypt...")
                protected=True
                self.url=video.player.decryptSigWithParams(fmtData["signatureCipher"])
            #print(protected)
            #print(self.url)
            info.protected=protected
            
            #webbrowser.open(self.url)
            #print(self.url)
            #assert 0
            #print(fmtData["mimeType"])

            info.mimeType,self.codecs=fmtData["mimeType"].split("; codecs=")
            self.codecs=eval(self.codecs)
            info.extension=mimetypes.guess_extension(info.mimeType)
            #self.videoOrAudio=info.mimeType.videoOrAudio
            info.bitrate=Bitrate(fmtData["bitrate"])
            contentLength=fmtData.get("contentLength")
            info.contentLength=BytesCount(contentLength) if contentLength else None
            #ti.print("getting content length")
            #contentLength=self.getContentLength()
            #ti.print("getted content length")
                #odata(self.video._data)
            #if info.contentLength and contentLength!=info.contentLength:
            #        print("Not same contentLength: %s != %s"%(contentLength,info.contentLength),file=sys.stderr)
            info.hasAudio=False
            sampleRate=fmtData.get("audioSampleRate")
            if sampleRate:
                info.hasAudio=True
                audioQuality=AudioQuality(fmtData["audioQuality"],sampleRate)
            #ti.print("MIDDLE")
            info.export()
            if "video" in self.mimeType:
                info.size=Size(fmtData["width"],fmtData["height"])

                info.videoQuality=VideoQuality(fmtData["quality"],fmtData["qualityLabel"])
                self.videoQualityType=self.qualityType=info.videoQuality.qualityType
                self.width=info.size.width
                self.height=info.size.height
                self.pixels=self.qualityPixels=info.videoQuality.qualityPixels
                self.qualityLabel=info.videoQuality.qualityLabel
                self.qualityType=info.videoQuality.qualityType
                self.fps=info.videoQuality.fps
                
            if info.hasAudio:
                info.audioQuality=AudioQuality(fmtData["audioQuality"],sampleRate)
                self.sampleRate=info.audioQuality.sampleRate
                self.audioQualityType=info.audioQuality.qualityType
            self.type=info.mimeType
            self.id=info.itag
        #ti.print("BYE")
            #info.hasAudio=displaySetLen(hasAudio,5)
            #info.audioQuality=displaySetLen(audioQuality,16)
            #super().__init__(self.url,os.path.join(DLDIR,"{fmt.video.id} - {onlyalpha(fmt.video.title)} {fmt.videoOrAudio}#{fmt.itag}.{fmt.extension}"))
    def __repr__(self):return reprWithCls(str(dict(self.info)),self)

    def download(self,fileDest="rrytapi_downloads/{to_filename(self.video.title)}_{self.itag}{self.extension}",resume=True,printInfo=True,showInExplorerBool=True,chunk_size=8192,waitIntervalToPrint=1):

        global show
        #show=lambda:subprocess.call(["open","-R",repr(fileDest)]) if showInFinder else lambda:None
#         print(fileDest)
        if showInExplorerBool:
            def sie():
                showInExplorerFunc(fileDest)
                time.sleep(2)
        else:
            sie=lambda:None
        #if extension:
        #    fileDest+="."+extension
        """
        for _ in range(10):
            show()
            time.sleep(1)
            print("SHOWD")
        """
        prt=print if printInfo else lambda a:a
        #print(self)
        #print(type(self))
        #print(vars(self))
        #[K[download]  24.6% of 2.69MiB at  4.99KiB/s ETA 06:5
        #contentLength=tryexec(getContentLength)
        contentLength=self.getContentLength()
        
        """
        try:
            sContentLength=self.contentLength
            assert sContentLength
        except:pass
        else:
            if contentLength!=sContentLength:
                prt("Not same contentLength: %s != %s"%(contentLength,sContentLength),file=sys.stderr)
        """
        #print("BEFORE: %s"%fileDest)
        fileDest=eval("f"+repr(fileDest),globals(),locals())
        dir=os.path.dirname(fileDest)
        if dir:
            os.makedirs(dir,exist_ok=True)
        #print("AFTER: %s"%fileDest)
        prt("Download %s to %s..."%(contentLength.display(True),repr(fileDest)))
        ndl=0
        if resume and os.path.exists(fileDest):
            with open(fileDest,"ab"):pass
            downloaded=os.path.getsize(fileDest)
            if downloaded>=contentLength:
                #downloaded-=1
                prt("Downloaded (already)")
                sie()
                return fileDest
            headers={"Range":"bytes=%s-"%downloaded}
            prt("Download resume at %s"%BytesCount(downloaded))
        else:
            with open(fileDest,"wb"):pass
            downloaded=0
            headers={}
        sie()
        #print("CEST MONTRö")
        #print("GO")
        #if not fileDest:raise ValueError("Please put the fileDest")
        tt=ftt=time.time()
        with requests.get(self.url,stream=True,headers=headers) as res:
            res.raise_for_status()
            #show()
            for chunk in res.iter_content(chunk_size=chunk_size):
                with open(fileDest,"ab") as f:
                    f.write(chunk)
                downloaded+=chunk_size
                ndl+=chunk_size
                ntt=time.time()
                if ntt>tt+waitIntervalToPrint:
                    #print("HELLO")
                    tt=ntt
                    perSecond=BytesCount(ndl/(ntt-ftt))
                    prt("Download Progress: %s%% %s/%s  %s/s  last:%s"%(str(round(downloaded/contentLength*100,1)).rjust(4,"0"),str(BytesCount(downloaded)).rjust(7),contentLength,perSecond,Duration(int((contentLength-downloaded)/perSecond))))
                    pdl=0
        #r=requests.get(str(self),stream=True)
        prt("Downloaded")
        return fileDest
        #return File(fileDest,r.content)
    #quality=aliasprop("qualityPixels")


    
    """
    def __getattr__(self,name):
        for obj in (self.size,self.mimeType,self.videoQuality,self.audioQuality):
            try:return getattr(obj,name)
            except:pass
        raise attrError(self,name)
    """
    #def download(self,):


"""
for name in ("width","height",
                 "extension","isAudio","isVideo","videoOrAudio",
                 "pixels","qualityLabel","qualityPixels","qualityType","fps",
                 "sampleRate",
                 ):
    exec('Format.%s=aliasprop("__getattr__(%s)")'%(name,repr(name)))
"""
class Formats(list):
    _fmt=None

    def __repr__(self):
        return printer(list(self))

    def __call__(self,item):
        return (
            self.filtrer(lambda x:x.itag==item) or\
            self.filtrer(lambda x:item in x.extension) or\
            self.filtrer(lambda x:x.videoQualityType==item) or\
            self.filtrer(lambda x:x.audioQualityType==item)
        )
        
    def __getattr__(self,item):
        try:return getattr(self[0],item)
        except:
            try:
                return self(item)
            except:
                raise attrError(self,item)
        if not self._fmt:
            self._fmt=self[0]
            for d in dir(self._fmt):
                if d.startswith("_") or d=="video":continue
                #print(self._fmt,d,type(self._fmt))
                #dddd
                try:
                    attr=getattr(self._fmt,d)
                except Exception as err:
                    import __main__
                    __main__._fmt=self._fmt
                    raise err
                setattr(self,d,attr)
        try:return self.__getitem__(item)
        except:
            try:return getattr(self._fmt,item)
            except AttributeError:pass
        raise attrError(self,item)

    def filtrer(self,condition):
        #print("LA CONDITION")

        return Formats([fmt for fmt in self if condition(fmt)])
    #def download(self,url=defaultFileDest):
    #    url=defaultFileDest.format()
    video=aliasprop("filtrer(lambda fmt:'video' in fmt.mimeType)")
    audio=aliasprop("filtrer(lambda fmt:'audio' in fmt.mimeType)")
    withAudio=aliasprop("filtrer(lambda fmt:fmt.hasAudio)")
    withoutAudio=aliasprop("filtrer(lambda fmt:not fmt.hasAudio)")
    #__getattr__=__getitem__
class NoneFormats:
    def __getattr__(self,*a,**k):return self
    def __call__(self,*a,**k):return self
class ChannelInfo:
    def __init__(self,name,id,url,thumbnails=None,badges=[]):
        with Info(self) as info:
            info.name=name
            info.id=id
            info.url=Url(url)
            if thumbnails:
                if type(thumbnails)!=Thumbnails:info.thumbnails=Thumbnails(thumbnails,name="channel %s"%name)
            info.badges=badges
    def __repr__(self):
        return reprWithCls(repr(self.name),self)
def intorfloat(count):
    try:
        i=int(count)
        if i==count:return i
    except:pass
    return float(count)
def viewcount(count):
    try:return intorfloat(count)
    except:pass
    if count=="No Views":return 0
    count=count.partition(" ")[0].replace(",","")
    tcoef=count[-1]
    if tcoef=="K":coef=1000
    elif tcoef=="M":coef=1000000
    else:raise NameError(count[-1])
    return intorfloat(count[:-1])*coef
class ViewCount(int):
    def __new__(cls,count):
        try:
            return super().__new__(cls,(0 if "no" in count.lower() else count.partition(" ")[0].replace(",","")) if type(count)==str else count)
        except:
            print(count=="no views")
            assert 0,count
    #def __repr__(self):return int(self)
class ValueNotFound(Exception):pass
def getText(data):
    try:runs=data["runs"]
    except:return data["simpleText"]
    return "".join(run["text"] for run in runs)

class MiniDisplay:
    def __init__(self,obj,display):
        self.obj=obj
        self.display=display
    def __repr__(self):return self.display
    @classmethod
    def withL(cls,obj,name):
        return cls(obj,"<%s %s>"%(len(obj),name))
    @classmethod
    def firstChars(cls,obj,l=100):
        return cls(obj,repr(obj[:l]+"..."))
    
def forceSetAttr(self,n,v):
    object.__setattr__(self,n,v)
    #f=self.__setattr__
    #del self.__setattr__
    #self.__setattr__(n,v)
    #self.__setattr__=f
class Info(dict):
    def __init__(self,dst):
        object.__setattr__(self,"dst",dst)
        #self.dst=dst
        self.dst.info=self 
        super().__init__()
    def __enter__(self):return self
    def export(self):
        #if error:raise error
        for name,value in self.items():
            if type(value)==MiniDisplay:
                value=value.obj
            setattr(self.dst,name,value)
    def __exit__(self,type,err,tb):
        self.export()
    def __repr__(self):
        return printer(dict(self))
    def __getitem__(self,key):
        value=super().__getitem__(key)
        return value.obj if type(value)==MiniDisplay else value
    
    __setattr__=dict.__setitem__
    __getattr__=__getitem__
#class Test:pass
#i=Info(Test())
#i.a=2
#print(i)
#dddd

def getBadges(data,key):
    if not data:return []
    return [badge["metadataBadgeRenderer"][key] for badge in data]

def getChannelInfo(data,isChannel=False):
    lmb=[]
    for name in ("shortBylineText","ownerText","longBylineText"):
        try:d=data[name]
        except:continue
        lmb.append(Constant(d,name))

    channel=lambdas(data,lmb)["runs"][0]


    channelPoint=channel["navigationEndpoint"]

    thumbnails=data.get("channelThumbnailSupportedRenderers")
    thumbnails=[data["thumbnail"]] if isChannel else [data.get("channelThumbnailSupportedRenderers",{}).get("channelThumbnailWithLinkRenderer")]
    

    return ChannelInfo(channel["text"],
                        channelPoint["browseEndpoint"]["browseId"],
                        lambdas(
                            channelPoint,
                            (x["commandMetadata"]["webCommandMetadata"]["url"],
                            x["browseEndpoint"]["canonicalBaseUrl"]),
                            urllib.parse.unquote),
                        None if thumbnails in (None,[None]) else Thumbnails(*thumbnails),
                       getBadges(data.get("ownerBadges"),"tooltip"))


class Video:
    def __init__(self,webpage):
        data=self._data=extractVar(webpage,"ytInitialPlayerResponse")
        #ti.print("webpage getted")
        #odata(data)
        streaming=data["streamingData"]
        details=data["videoDetails"]
        xdetails=Constant(details,"details")
        microformat=data["microformat"]["playerMicroformatRenderer"]
        xmicroformat=Constant(microformat,"microformat")
        

        with Info(self) as info:
            info.id=details["videoId"]
            info.url=Url(YTWATCH+info.id)
            #open_json(details)
            info.islive=lambdas(data,(x["responseContext"]["serviceTrackingParams"][0]["params"][0]["value"]=="True",
                                      Constant(bool)(x["playabilityStatus"].get("liveStreamability")),
                                      xdetails["isLiveContent"]))
            #odata(data)
            info.title=remove_emoji(lambdas(data,(xdetails,(xmicroformat,getText)),x["title"]))
            l=lambdas(data,(xdetails,xmicroformat),Constant(int)(x["lengthSeconds"]),funcVerifIfSame=lambda x,y:abs(x-y)<2)
            #print(l)
            info.duration=Duration(l)
            #print(info.lengthSeconds)
            #print(Duration(l))
            #print(type(info.lengthSeconds))
            keywords=details.get("keywords",[])
            #odata(data)
            info.keywords=MiniDisplay.withL(keywords,"keywords")
            info.thumbnails=MiniDisplay.withL(Thumbnails(details,microformat),"thumbnails")
            info.viewCount=ViewCount(lambdas(data,(xdetails,xmicroformat),x["viewCount"]))
            info.channel=ChannelInfo(lambdas(data,(xdetails["author"],xmicroformat["ownerChannelName"])),
                               lambdas(data,(xdetails["channelId"],xmicroformat["externalChannelId"])),
                               microformat["ownerProfileUrl"])
            info.export()
            #ti.print("player...")
            self.player=Player.fromVideo(webpage)
            #ti.print("played...")
            formats=Formats()
            #ti.print("formated")
            for fmt in streaming.get("formats",[])+streaming.get("adaptiveFormats",[]):
                #ti.print("new format")
                formats.append(self.Format(fmt))
            #ti.print("f1")
            info.formats=MiniDisplay.withL(formats,"formats")
            #ti.print("ff")
        #print(self.title)
    def __repr__(self):
        return reprWithCls("%s in %s"%(repr(self.title),self.url),self)
    def Format(self,fmtData):
        return Format(self,fmtData)
    @classmethod
    def get(cls,video_or_url,tries=30,wait=1):
        ti.start()
        if isinstance(video_or_url,Video):return video_or_url
        elif isinstance(video_or_url,VideoR):url=video_or_url.url
        else:url=video_or_url
        url=YTWATCH+getVideoId(str(url))+"&bcptr=9999999999&has_verified=1"
        #ti.print("GETTING...")
        for _ in range(tries):
            r=requests.get(url,headers=acceptLang)
            #ti.print("requested")
            t=r.text
            #ti.print("texted")
            try:
                s=cls(t)
                #ti.print("return")
                return s
            except ContentLengthError as e:err=e
            #ti.print("cls")
            time.sleep(wait)
            #ti.print("FAIL")
        raise err
    
    videoId=aliasprop("id")
    videoUrl=aliasprop("url")
    length=seconds=lengthSeconds=aliasprop("duration")
    owner=author=aliasprop("channel")
    download=aliasprop("formats.download")
    #ownerId=aliasprop("authorId")
    #ownerUrl=aliasprop("authorUrl")

class Playlist(list):
    def __init__(self,data):
        #odata(data)
        with Info(self) as info:
            renderer=data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]\
                    ["contents"][0]["itemSectionRenderer"]["contents"][0]["playlistVideoListRenderer"]
            xrenderer=Constant(renderer,"renderer")
            idx=0
            for videoData in renderer["contents"]:
                #ajson(videoData)
                if videoData.get("continuationItemRenderer"):continue
                #print(idx)
                self.append(
                    VideoR(videoData["playlistVideoRenderer"],fromPlaylist=True)
                )
                #videos.append(video)
                idx+=1
            info.videos=MiniDisplay.withL(self,"videos")
            header=data["header"]["playlistHeaderRenderer"]
            #ajson(header)
            xheader=Constant(header,"header")
            microformat=data["microformat"]["microformatDataRenderer"]
            xmicroformat=Constant(microformat,"microformat")
            metadata=data["metadata"]["playlistMetadataRenderer"]
            xmetadata=Constant(metadata,"metadata")
            info.id=lambdas(data,(xrenderer["playlistId"],xrenderer["targetId"],xheader["playlistId"],
                                  xheader["serviceEndpoints"][0]["playlistEditEndpoint"]["actions"][0]["sourcePlaylistId"]))
            xbutton=x["button"]["buttonRenderer"]["navigationEndpoint"]["signInEndpoint"]["nextEndpoint"]\
                                 ["commendMetadata"]["webCommandMetadata"]
            info.url=Url(lambdas(data,(xheader["saveButton"]["toggleButtonRenderer"]["defaultNavigationEndpoint"]\
                                 ["modalEndpoint"]["modal"]["modalWithTitleAndButtonRenderer"]["button"]\
                                 ["buttonRenderer"]["navigationEndpoint"]["signInEndpoint"]["nextEndpoint"]\
                                 ["commandMetadata"]["webCommandMetadata"]["url"],
                                       xmicroformat["urlCanonical"],
                                       xmicroformat["iosAppArguments"],
                                       xmicroformat["linkAlternates"][0]["hrefUrl"],
                                
                                       ),
                                 Url))
            
            #info.videoId=header["playEndpoint"]["watchEndpoint"]["videoId"]
            #info.urlWithVideo=Url(lambdas(data,xheader["playEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]))
            info.title=lambdas(data,(Constant(getText)(xheader["title"]),xmetadata["title"],
                                     xmicroformat["title"]))
            info.videosNumber=int(getText(lambdas(data,(xheader["numVideosText"],xheader["stats"][0]))).partition(" ")[0])
            description=lambdas(data,(Constant(getText)(xheader["descriptionText"]),xmetadata["description"]))
            info.description=MiniDisplay(description,microformat["description"])
            info.channel=getChannelInfo(header)
            info.viewCount=ViewCount(getText(lambdas(data,(xheader["viewCountText"],xheader["stats"][1]))))
            info.thumbnails=MiniDisplay.withL(Thumbnails(microformat),"thumbnails")
    @classmethod
    def get(cls,url):
        url=YTPLAYLIST+getPlaylistId(url)
        #print(url)
        return cls(extractVar(url,"ytInitialData"))
    def __repr__(self):
        return printerWithCls(list(self),f"{tname(self)} {repr(self.title)} in {self.url}")



#open_json({1:2,3:4})
#ddd








def getId(url,arg):
    if "/" not in url:return url
    def index(subs,s,*args):
        i=[]
        err=ValueError("Please put some subs")
        for sub in subs:
            try:idx=s.index(sub,*args)
            except ValueError as e:err=e
            else:i.append(idx)
        if not i:raise err
        return min(i)
    url="="+url+"&"
    idx=-index((("?%s="%arg)[::-1],"/"),url[::-1])
    return url[idx:index(("&"),url)]
def getVideoId(url):
    return getId(url,"v")
def getPlaylistId(url):
    return getId(url,"list")
#print(getPlaylistId("https://youtube.com/playlist?list=PLMC9KNkIncKseYxDN2niH6glGRWKsLtde"))


import random
def extractVar(webpage,varname):
    if type(webpage)==str and webpage.startswith("http"):
        webpage=requests.get(webpage,
                             headers=acceptLang,
                            cookies={'CONSENT': 'YES+cb.20210328-17-p0.en-GB+FX+%s'%random.randint(100, 999)}
                             ).text
    #mypkg.open_data(mypkg.htmlsoup(webpage))
    try:
        idx2=webpage.index("var %s"%varname)
    except ValueError:
        raise ValueError("Cannot extract var")
    d=webpage[webpage.index("{",idx2):]
    try:d=json.loads(d)
    except json.JSONDecodeError as err:
        return json.loads(d[:err.pos])


#SEARCHING SECTION
if 1:
    def search(query):
        url="https://www.youtube.com/results?search_query="+urllib.parse.quote(query)
        #print(url)
        contents=[]
        for c in extractVar(
            url,"ytInitialData")["contents"]["twoColumnSearchResultsRenderer"]\
                ["primaryContents"]["sectionListRenderer"]["contents"]:
            if c.get("continuationItemRenderer"):continue
            
            contents.extend(c["itemSectionRenderer"]["contents"])
        return ListR(contents)
    class ListR(list):
        def __init__(self,data):
            
            #contents=data["contents"]["twoColumnRenderersRenderer"]
            #mypkg.open_data(data)
            i=0
            for drenderer in data:
                for key,value in drenderer.items():
                    if key=="videoRenderer":
                        #odata(drenderer)

                        renderer=VideoR(value)

                    elif key=="childVideoRenderer":
                        #print("CHILD")
                        #odata(drenderer)
                        renderer=VideoR(value,isChild=True)
                    elif key=="shelfRenderer":
                        renderer=ShelfR(value)
                    elif key=="playlistRenderer":
                        renderer=PlayListR(value)
                    elif key=="channelRenderer":
                        #mypkg.open_data(value)
                        #continue
                        renderer=ChannelR(value)
                    elif key=="movieRenderer":
                        renderer=MovieR(value,isChild=True)
                    elif key=="gridMovieRenderer":
                        renderer=MovieR(value,isChild=True)
                    elif key=="promotedSparklesWebRenderer":
                        renderer=AdR(value)
                    else:
                        renderer=UnknownR(key,value)
                        #odata(drenderer)
                    super().append(renderer)
        def __repr__(self):
            return printerWithCls(list(self),self)
        def __getitem__(self,y):
            if type(y)==slice:item,idxTarget=y.start,y.stop
            else:item,idxTarget=y,0
            assert item is not None
            l=list(self)
            if type(item)==int:return l.__getitem__(y)
            idx=0
            for el in l:
                title=url=None
                try:
                    title=el.title
                    url=el.url
                except:pass
                t=type(el)
                good=False
                if item in (t,t.__name__,title,url):
                    good=True
                elif issubclass(t,ListR):
                    try:
                        el=el[item]
                        good=True
                    except KeyError:pass
                if good:
                    if idx==idxTarget:
                        return el
                    idx+=1
            return {}[item]
        
    class UnknownR:
        def __init__(self,key,value):
            self.key=key
            self.value=value
            #ajson(value)
        def __repr__(self):
            return "<UnknownRenderer: %s>"%self.key
    class ShelfR(ListR):
        def __init__(self,data):
            self.title=getText(data["title"])
            content=data["content"]
            #ajson(data)
            super().__init__((content.get("horizontalListRenderer") or content["verticalListRenderer"])["items"])
        def __repr__(self):
            return printerWithCls(list(self),tname(self)+" "+repr(self.title))
    class PlayListR(ListR):
        def __init__(self,data):
            #mypkg.open_data(data)
            with Info(self) as info:
                info.id=id=lambdas(data,(x,x["navigationEndpoint"]["watchEndpoint"]),x["playlistId"])
                info.title=getText(data["title"])
                info.thumbnails=[Thumbnails(ths) for ths in data["thumbnails"]]
                info.url=Url(data["viewPlaylistText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"])
                info.urlWithVideo=Url(data["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"])
                info.videoId=data["navigationEndpoint"]["watchEndpoint"]["videoId"]
                info.channel=getChannelInfo(data)
            super().__init__(data["videos"])
        def __repr__(self):
            return printerWithCls(list(self),"%s %s in %s"%(tname(self),repr(self.title),self.url))
    class AdR:
        def __init__(self,data):
            with Info(self) as info:
                info.thumbnails=Thumbnails(data)
                info.title=getText(data["title"])
                info.description=MiniDisplay.firstChars(getText(data["description"]))
                info.website=getText(data["websiteText"])
                point=data["navigationEndpoint"]
                xpoint=Constant(point,"point")
                info.url=lambdas(data,(xpoint["commandMetadata"]["webCommandMetadata"],xpoint["urlEndpoint"]),x["url"])
        def __repr__(self):
            return reprWithCls("%s in %s"%(repr(self.title),self.website),self)

    class VideoR:
        def __init__(self,data,isChild=False,fromPlaylist=False):
            
                #mypkg.open_data(data)
                #assert 0
            #print(data["navigationEndpoint"])
            #print(open_json(data))
            with Info(self) as info:
                point=data["navigationEndpoint"]
                xpoint=Constant(point,"point")
                try:
                    info.badges=getBadges(data.get("badges"),"label")
                except:
                    #mypkg.open_data(data)
                    assert 0
                hasbadgelive="LIVE" in info.badges
                islive=tuple(data.get("thumbnailOverlays",[{}])[0].keys())==("thumbnailOverlayToggleButtonRenderer",)
                self.islive=hasbadgelive or islive
                self.hasbadgelive=hasbadgelive
                err=None
                if hasbadgelive and not islive:
                    print("HASBADGELIVE:%s != ISLIVE:%s "%(islive,hasbadgelive))
                if islive:info.badges.append("LIVE")
                """
                nostable=False
                err=None
                if islive!=islive2:
                    #mypkg.open_data(data)
                    #assert 0
                    err="ISLIVE OR NOT ISLIVE: %s != %s"%(islive,islive2)
                    nostable=True
                    if islive2:islive=islive2
                """
                #mypkg.open_data(data)
                #assert 0
                isShorts=None
                if isChild:isShorts=False
                else:
                    if not self.islive:

                        timestatus=data["thumbnailOverlays"][0]["thumbnailOverlayTimeStatusRenderer"]


                        for func in (lambda:timestatus["text"]["accessibility"]["accessibilityData"]["label"]=="Shorts",
                                    lambda:getText(timestatus["text"])=="SHORTS",
                                    lambda:timestatus["style"]=="SHORTS"):
                            b=func()
                            #print(b)
                            assert isShorts is None or b==isShorts
                            isShorts=b
                isExpectedShorts=False
                try:lambdas(data,xpoint["watchEndpoint"],errmode=None)
                except:
                    #dddd
                    #print(isShorts)
                    isShorts=True
                    

                self.isShorts=isShorts
                try:
                    info.id=id=lambdas(data,(x,xpoint["reelWatchEndpoint" if isShorts else "watchEndpoint"]),x["videoId"])
                except:
                    #mypkg.open_data(data)
                    assert 0

                info.url=Url(lambdas(data,xpoint["commandMetadata"]\
                                ["webCommandMetadata"]["url"],errmode="raise") or YTWATCH+id)

                """
                    print(lambdas(data,[xpoint["commandMetadata"]\
                                ["webCommandMetadata"]["url"]]))
                """


                if err:
                    print(err+" url:%s"%info.url)
                if not isChild:
                    info.thumbnails=Thumbnails(data)
                #mypkg.open_data(data)
                info.title=remove_emoji(getText(data["title"]))
                #assert 0
                #assert 0
                if not isChild:
                    
                    info.channel=getChannelInfo(data)
                xLengthText=x["lengthText"]
                if not self.islive:
                    info.duration=Duration(getText(lambdas(data,([x["lengthText"]]+([] if isChild or isShorts else [x["thumbnailOverlays"][0]["thumbnailOverlayTimeStatusRenderer"]["text"]])))))
                if not isChild and not fromPlaylist:
                    viewCountText=data.get("viewCountText")
                    info.viewCount=ViewCount(getText(viewCountText)) if viewCountText else "?"
                    #excexrpt:odata(data)
                    try:
                        info.description=getText(data["detailedMetadataSnippets"][0]["snippetText"])
                    except:
                        info.description=None
        def __repr__(self):
            return reprWithCls("%s in %s"%(repr(self.title),self.url),tname(self)+(" LIVE" if self.islive else ""))
        def get(self):
            return Video.get(self.url)

        owner=author=aliasprop("channel")

    class MovieR(VideoR):pass

    class ChannelR:
        def __init__(self,data):
            with Info(self) as info:
                info.id=lambdas(data,(x["channelId"],x["navigationEndpoint"]["browseEndpoint"]["browseId"]))
                info.name=getText(data["title"])

                info.url=Url(lambdas(data["navigationEndpoint"],(x["commandMetadata"]["webCommandMetadata"]["url"],x["browseEndpoint"]["canonicalBaseUrl"])))
                #open_json(data)
                channel=getChannelInfo(data,isChannel=True)

                assert info.id==channel.id
                assert info.name==channel.name
                info.badges=channel.badges
                info.description=getText(data["descriptionSnippet"])
                #print(data)
                count=getText(data["videoCountText"])
                if "subscribers" in count:
                    info.subscriberCount=0 if "No" in count else viewcount(count)
                else:assert 0
                    #info.videoCount=viewcount(getText(data["videoCountText"])[:-7])
                pseudo=getText(data["subscriberCountText"])
                assert "@" in pseudo
                info.pseudo=pseudo

        def __repr__(self):
            return reprWithCls("%s in %s"%(repr(self.name),self.url),self)
    class Channel(ListR):
        def __init__(self,data):
            #odata(data)
            contents=data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
            content=contents[0]["tabRenderer"]
            xcontent=Constant(content,"content")
            with Info(self) as info:
                info.name="UNDEFINED NAME"
                info.url=Url(lambdas(data,(xcontent["endpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
                                    xcontent["endpoint"]["browseEndpoint"]["canonicalBaseUrl"]),lambda x:x[:-9] if x.endswith("/featured") else x)
                            )
                
                info.video=ChannelPlayerVideoR(content["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelVideoPlayerRenderer"])
            
        @classmethod
        def get(cls,url):
            return cls(extractVar(url,"ytInitialData"))
        
    class ChannelPlayerVideoR:
        def __init__(self,data):
            with Info(self) as info:
                run=data["title"]["runs"][0]
                xrun=Constant(run,"run")
                info.id=lambdas(data,(x,xrun["navigationEndpoint"]["watchEndpoint"]),x["videoId"])
                info.title=run["text"]
                info.url=Url(run["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"])
                info.description=MiniDisplay.firstChars(getText(data["description"]))
                info.viewCount=ViewCount(getText(data["viewCountText"]))
                info.publishedTime=getText(data["publishedTimeText"])
        def __repr__(self):
            return reprWithCls("%s in %s"%(repr(self.title),self.url),self)
    
#var=extractVar("https://www.youtube.com/c/FuzeIII","ytInitialData")
#mypkg.open_data(var)
#assert 0
if __name__=="__main__":
    from rrytapi_caller import *
    #var=extractVar("https://www.youtube.com/results?search_query=yt","ytInitialData")
    #var=extractVar("https://www.youtube.com/watch?list=PLMC9KNkIncKseYxDN2niH6glGRWKsLtde&bcptr=9999999999&has_verified=1","ytInitialData")
    #mypkg.open_data(var)
    #var=extractVar("https://www.youtube.com/watch?list=PLMC9KNkIncKseYxDN2niH6glGRWKsLtde&amp;bcptr=9999999999&amp;has_verified=1&amp;cbrd=1","ytInitialData")
    pass
