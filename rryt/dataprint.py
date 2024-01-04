TAB="   "



def dprint(data):
    print(printer(data))
def _tp(v,t):
    return printer(v,t)[len(t):]
def _addspaces(string,l):
    string=str(string)
    return string+" "*(l-len(string))
def printer(data,tab=""):
    t=tab+TAB
    def fromiter(empty_iter):
        chars=str(empty_iter)
        return tab+(chars[0]+"\n"+("".join(map((lambda i:printer(i,t)+",\n"),data)))+tab+chars[1] if data else chars)
    def fromitems(k,v):
        return t+_addspaces(k,lmax)+": "+_tp(v,t2)+",\n"
    if type(data)==list:
        return fromiter([])
    if type(data)==tuple:
        return fromiter(())
    if type(data)==set:
        return fromiter({})
    if type(data)==dict:
        keys=list(map(repr,data.keys()))
        if not keys:return tab+"{}"
        values=list(data.values())
        lmax=max(map(len,keys))
        t2=t+" "*(lmax+2)
        return tab+"{\n"+("".join(map(fromitems,keys,values)))+tab+"}"
    return tab+(repr(data).replace("\n","\n"+tab))
def saveinfile(data,file="data.json"):
    with open(file,"w") as f:
        f.write(printer(data))

#print(printer({1:2,3:4,50:[1,2]}))
saveinfile({1:2,3:4,5:6,"abbbbccccc":[1,2,3]})
#dprint({1:2,3:4,5:6})q