"""
Just utils
"""
import time
import json
import random
import re
import sys

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



acceptLang={"Accept-Language": "en-US"}

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

def lambdas(xValue,lambdasExpr,endFunc=None,errmode="print",funcVerifIfSame=None):
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