import requests,json,js2py
from .dataprint import dprint

import urllib,os
from bs4 import BeautifulSoup
def rqstGet(url):
    if type(url)==str and url.startswith("http"):return requests.get(url,headers={"Accept-Language": "en-US"}).text
    return url
def indexp(string,find,indexstart=0):
    """
    if isinstance(find,(list,tuple)):
        finds=find
        idx=len(string)
        for find in finds:
            nidx=string.index(find,indexstart)
            
        idx=min(map(lambda f:string.index(f,indexstart),find))
    else:
    """
    idx=string.find(find,indexstart)
    if idx==-1:return idx
    return idx+len(find)
#print(indexp("atgeabe",("g","e")))
#sss
class Player:
    playersName="players"
    playersDirectory=os.path.dirname(__file__)+"/"+playersName
    try:os.mkdir(playersDirectory)
    except FileExistsError:pass
    currentPlayerName="currentPlayer"
    currentPyPlayerFile=playersDirectory+"/%s.py"%currentPlayerName
    currentJsPlayerFile=playersDirectory+"/%s.js"%currentPlayerName
    def __init__(self,playerUrl,playerId=None):
        self.playerUrl=playerUrl
        self._playerId=playerId
        if self.playerId==self.playerUrl:self.playerUrl="https://www.youtube.com/s/player/%s/player_ias.vflset/en_US/base.js"%playerUrl
    @property
    def jsPlayerFile(self):
        return self.playerFile(ext="js")
    @property
    def pyPlayerFile(self):
        return self.playerFile(ext="py")
    def playerFile(self,ext):
        return self.playersDirectory+"/"+self.varname+"."+ext
    @property
    def varname(self):
        return "player_%s"%self.playerId
    @property
    def playerId(self):
        
        if self._playerId:return self._playerId
        if "/" not in self.playerUrl:return self.playerUrl
        try:
            i=indexp(self.playerUrl,"/player/")
        except:
            raise ValueError("Cannot extract player id")
        i2=self.playerUrl.index("/",i)
        return self.playerUrl[i:i2]
    def decryptSig(self,sig,forceExtractFunction=False,forceWritePyFunction=False,forceWriteJsFunction=False):
        try:
            assert not forceExtractFunction
            self._decrypt
        except Exception as err:
            print(err)
            self.extractFunction(forceWritePyFunction,forceWriteJsFunction)
        return self._decrypt(sig)
    def decryptSigWithParams(self,params,forceExtractFunction=False,forceWritePyFunction=False,forceWriteJsFunction=False,ti=None):
        if type(params)==str:
            sparams=params
            params={}
            for param in sparams.split("&"):
                key,_,value=param.partition("=")
                params[key]=urllib.parse.unquote(value)
        return "%s&%s=%s"%(params["url"],params.get("sp","sig"),urllib.parse.quote(self.decryptSig(params["s"],forceExtractFunction,forceWritePyFunction,forceWriteJsFunction)))
    def extractFunction(self,forceWritePyFunction=False,forceWriteJsFunction=False):
        if forceWritePyFunction or not os.path.exists(self.pyPlayerFile):
            self.writePyFunction(forceWriteJsFunction)
        #print(".%s.%s"%(self.playersName,self.varname))
        print("rrytapi.%s.%s"%(self.playersName,self.varname))
        module=__import__("rryt.%s.%s"%(self.playersName,self.varname))
        print(module)
        playerModule=getattr(__import__("rryt.%s.%s"%(self.playersName,self.varname)),self.playersName)
        decrypt=getattr(getattr(playerModule,self.varname),self.varname).decrypt
        self._decrypt=decrypt
        return decrypt
    def writePyFunction(self,forceWriteJsFunction=False):
        if forceWriteJsFunction or not os.path.exists(self.jsPlayerFile):
            self.writeJsFunction()
        js2py.translate_file(self.jsPlayerFile,self.pyPlayerFile)
        self.symlink(self.pyPlayerFile,self.currentPyPlayerFile)
    @staticmethod
    def symlink(src,dst):
        try:os.remove(dst)
        except:pass
        
        os.symlink(os.path.abspath(src),dst)
        
    def writeJsFunction(self):
        player=rqstGet(self.playerUrl)
        rplayer=player[::-1]
        i2=0
        while True:
            i=player.index('{a=a.split("")',i2)
            i2=indexp(player,"}",i)
            code=player[i:i2]
            if code.endswith(';return a.join("")}'):break
        #print(code)
        code="decrypt=function(a)%s"%code
        v=[]
        i=0
        #print(code)
        #print("NAMMMEEEEEE %s"%name)
        while True:
            #print(i)
            i1=indexp(code,";",i)
            i2=indexp(code,"=",i)
            if i1==-1:
                if i2==-1:break
                i=i2
            elif i2==-1:i=i1
            else:i=min(i1,i2)
            #print(i,i1,i2)
            #dddd

            #print(i)
            i2=i+1
            while True:
                if not code[i2].isalpha():break
                i2+=1
            name=code[i:i2]
            #print("NAMMMEEEEEE %s"%name)
            if name in ("var","a","return","function","decrypt") or name in v:continue
                #print(player[i2])
            #print(name)
            v.append(name)
        #print(v)
        #raise ValueError(v)
        for var in v:
            #print(var)
            for sub in ("var %s="%var,"function %s("%var):
                try:
                    i=player.index(sub)
                    break
                except Exception as e:err=e
                
            else:
                raise err
            i2=i
            parens=0
            while True:
                i2+=1
                i3=player.index("{",i2)
                i4=player.index("}",i2)
                if i3<i4:
                    i2=i3
                    parens+=1
                else:
                    i2=i4
                    parens-=1
                    if not parens:break
            i2+=1
            code=player[i:i2]+";\n"+code
            #print(player[i:i2])
                
            #try:i=mypkg.indexp("var %s"%var)

        f=open(self.jsPlayerFile,"w")
        f.write(code)
        f.close()
        self.symlink(self.jsPlayerFile,self.currentJsPlayerFile)
    @classmethod
    def fromVideo(cls,videoUrl):
        video=rqstGet(videoUrl)
        i=indexp(video,'"jsUrl":')
        i2=video.index(",",i)
        return cls("https://youtube.com"+json.loads(video[i:i2]))
    def __repr__(self):
        return "<Player %s>"%self.playerId
def getItems(d,keys):
    dt={}
    for k in keys:
        try:
            dt[k]=d[k]
        except KeyError:pass
    return dt
def extractvar(url,varname):
    if type(url)==dict:return url
    soup=BeautifulSoup(rqstGet(url))
    soup=mypkg.htmlsoup(rqstGet(url))
    #mypkg.open_data(soup)
    #c=mypkg.requests_get(url)
    find="var %s = "%varname
    for script in soup.find_all("script"):
        text=script.text.strip()
        if text.startswith(find):
            return json.loads(text[len(find):-1])
def getFormats(url):
    data=extractplayer(url)["streamingData"]
    #mypkg.open_data(data)
    
    #print(data)
    return data.get("formats",[])+data.get("adaptiveFormats",[])
def extractplayer(url):
    return extractvar(url,"ytInitialPlayerResponse")
def getSigAndUrl(url):
    d=[]
    for fmt in getFormats(url):
        d.append(getItems(fmt,("itag","url","signatureCipher")))
    return d
def getArgs(sigdata):
    args={}
    for arg in sigdata.split("&"):
        k,v=arg.split("=")
        args[k]=mypkg.unquote(v)
    return args
#popcorn link: "https://www.youtube.com/watch?v=jwI1j7sslYI"
#arcades link: https://www.youtube.com/watch?v=-kCePEEBjvc
"""
d=getSigAndUrl(data)
playerUrl=getPlayerUrl(data)
sc=getArgs(d[0]["signatureCipher"])
s=sc["s"]
sp=sc["sp"]
url=sc["url"]

player=Player("4583e272")
#writeJsFunction(playerUrl)
#func=extractFunction(playerUrl,True)
#sig=decryptSignature(s,playerUrl)
func=player.extractFunction(True,True)
#func=extractFunction("https://www.youtube.com/s/player/4583e272/player_ias.vflset/en_US/base.js")
"""
if __name__=="__main__":
    
    player=Player("4583e272")
    sig=player.decryptSig("AG3C_xAwRAIgQwiScAQY7_HK7vyDFYn9DaFXUYiZ6fw4skorbq6hYnkCI\
BAN2hbpcqsFzvFyxnTgR55s9xL4l3MqWVL8-6hySp5L&sig=AOq0QJ8wRQIhAPP93yzpxnPk-vGuKZMYGKxFq6OedDxT6vsTUrxAptBiAiB3p6Vj_ekYPvrbqc1aMdb1LUQlatLNMZTc13LmgCaO2g%3D%3Du",
                          True,True,True)
    
