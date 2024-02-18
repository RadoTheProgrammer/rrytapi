"""
Just utils
"""
import time
import json
import random
import re
import sys
import webbrowser
import os

import requests
import rrprettier

YT="https://youtube.com"
YTWATCH=YT+"/watch?v="
YTPLAYLIST=YT+"/playlist?list="

class TimeIt:

    def __init__(self):
        self.tt=0
        self.start()
    def start(self):
        self.stt=self.tt=time.time()
    def print(self,txt):
        tt=time.time()
        print("%07.3f %07.3f %s"%(tt-self.stt,tt-self.tt,txt))
        self.tt=tt

ti=TimeIt()



def extractVar(webpage,varname):
    if type(webpage)==str and webpage.startswith("http"):
        webpage=requests.get(
            webpage,
            headers=acceptLang,
            cookies={
                'CONSENT': f'YES+cb.20210328-17-p0.en-GB+FX+{random.randint(100, 999)}'},
            timeout = 10
                

        ).text
    #mypkg.open_data(mypkg.htmlsoup(webpage))
    try:
        idx2=webpage.index("var %s"%varname)
    except ValueError as exc:
        raise ValueError("Cannot extract var") from exc
    d=webpage[webpage.index("{",idx2):]
    try:
        d=json.loads(d)
    except json.JSONDecodeError as err:
        return json.loads(d[:err.pos])

functionType=type(extractVar)

def to_filename(s):
    return re.sub(r'[^\w\.\-_]', "_", s)

def asfunc(lambdaOrFunc):
    try:return lambdaOrFunc.evaluate
    except AttributeError:
        if lambdaOrFunc is None:
            return lambda v=None,*a,**k:v
        return lambdaOrFunc
    
def printerr(err):
    print(err,file=sys.stderr)

def errToStr(err):
    return "%s: %s"%(type(err).__name__,", ".join(err.args))

class LambdasError(Exception):pass
def to_yturl(url):
    if url.startswith("/"):url=YT+url
    if url.startswith("http://"):
        url="https"+url[4:]
    if url.startswith("https://www."):
        url="https://"+url[12:]
    return url



def lambdas(xValue,lambdasExpr,endFunc=None,errmode="raise",funcVerifIfSame=None):
    if not funcVerifIfSame:funcVerifIfSame=lambda x,y:x==y
    funcVerifIfSame=asfunc(funcVerifIfSame)
    endFunc=asfunc(endFunc)
    
    if errmode in (print,"print",printerr):errfunc=printerr
    elif errmode=="raise":
        def errfunc(err):
            print("DSNFOISNFOISFI")
            raise err
        #print("WWWWDGG")
    elif type(errmode) in (type,functionType):errfunc=errmode
    errfunc=asfunc(errfunc)
    for lambdaExpr in lambdasExpr if type(lambdasExpr) in (list,tuple) else (lambdasExpr,):
        func=None
        if type(lambdaExpr) in (list,tuple):
            lambdaExpr,func=lambdaExpr
            
        func=asfunc(func)
        try:value=asfunc(func)(endFunc(asfunc(lambdaExpr)(xValue)))
        except Exception as err: #pylint: disable=broad-exception-caught
            #print((asfunc(lambdaExpr)(xValue)))
            errfunc(LambdasError("%s: %s"%(repr(lambdaExpr),errToStr(err))))
            continue
        else:
            #print(avalue)
            try:avalue
            except NameError:
                pass
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
    except NameError:
        pass
    raise LambdasError("Failed extract value")

def bcptr(link):
    return link+"&bcptr=9999999999&has_verified=1"

def attrError(obj,name):
    return AttributeError("%s object has no attribute %s"%(repr(type(obj).__name__),repr(name)))



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
    return reprWithCls("\n"+rrprettier.prettify(data),cls)

# class MiniDisplay:

#     def __init__(self,obj,display):
#         self.obj=obj
#         self.display=display
#     def __repr__(self):return self.display
#     @classmethod
#     def withL(cls,obj,name):
#         return cls(obj,"<%s %s>"%(len(obj),name))
#     @classmethod
#     def firstChars(cls,obj,l=100):
#         return cls(obj,repr(obj[:l]+"..."))
    
# class Info(dict):
#     def __init__(self,dst):
#         object.__setattr__(self,"dst",dst)
#         #self.dst=dst
#         self.dst.info=self 
#         super().__init__()
#     def __enter__(self):return self
#     def export(self):
#         #if error:raise error
#         for name,value in self.items():
#             if type(value)==MiniDisplay:
#                 value=value.obj
#             setattr(self.dst,name,value)
#     def __exit__(self,_type,err,tb):
#         self.export()
#     def __repr__(self):
#         return rrprettier.prettify(dict(self))
#     def __getitem__(self,key):
#         value=super().__getitem__(key)
#         return value.obj if type(value)==MiniDisplay else value
    
#     __setattr__=dict.__setitem__
#     __getattr__=__getitem__






def convert_audio(input_file,output_file="{input_file}.{ext or 'mp3'}",ext=None):
    from pydub import AudioSegment
    output_file=eval("f"+repr(output_file),locals()) #pylint: disable=W0123
    #print(output_file)
    if not ext:
        ext=os.path.splitext(output_file)[1].lstrip(".")
    audio=AudioSegment.from_file(input_file)
    audio.export(output_file,format=ext)

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

def getText(data):
    try:runs=data["runs"]
    except:return data["simpleText"]
    return "".join(run["text"] for run in runs)

class ValueNotFound(Exception):pass

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
    
class ChannelInfo:
    def __init__(self,name,id,url,thumbnails=None,badges=[]):
        #with utils-Info(self) as info:
        self.name=name
        self.id=id
        self.url=to_yturl(url)
        if thumbnails:
            if type(thumbnails)!=Thumbnails:self.thumbnails=Thumbnails(thumbnails,name="channel %s"%name)
        self.badges=badges
    def __repr__(self):
        return reprWithCls(repr(self.name),self) #pylint: disable=E1101:no-member

acceptLang={"Accept-Language": "en-US"}

class Thumbnail:
    def __init__(self,thData,name=""):
        try:
            self.size=Size(thData["width"],thData["height"])
        except:print(type(thData))
        self.name=name
        self.width=self.size.width
        self.height=self.size.height
        self.url=to_yturl(thData["url"])

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

        for th in thumbnails:


            if type(th)!=Thumbnail:th=Thumbnail(th,self.name)
            for i in (th.width,th.height,th.width*th.height):
                if i in self.access:continue
                self.access[i]=th
            self.append(th)
        
    def __repr__(self):
        return rrprettier.prettify(list(self))
    def __getitem__(self,item):
        try:return self.access[item]
        except:return list(self)[item]

def get_info(self):
    to_exclude=self._to_exclude if hasattr(self,"_to_exclude") else () #pylint: disable=W0212:protected-access

    return rrprettier.dictp(
        {attr:(value._mini_display if hasattr(value,"_mini_display") else value) for attr,value in vars(self).items() if not (attr.startswith("_") or attr in to_exclude)}
    ) 

infoprop=property(get_info)
class ContentLengthError(Exception):pass
def getContentLength(self,tries=3,wait=1):

    err=None
    for _ in range(tries):
        try:
            for _ in range(1):
                #print("TRY")
                #requests.get(url,stream=True)
                #print(url)
                #print("WW")
                #ti.print("request....")
                res=requests.head(self,timeout=10)
                #ti.print("requested")
                res.raise_for_status()
                headers=res.headers

                contentLength=BytesCount(headers['content-length'])
                
                assert contentLength
                return contentLength
        except Exception as e: #pylint: disable=W0718:broad-exception-caught
            #print("TOUT")
            time.sleep(wait)
            #print(self.url)
            err=e
    raise ContentLengthError("Cannot extract the contentLength") from err