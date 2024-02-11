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
        return prettify(list(self))
    def __getitem__(self,item):
        try:return self.access[item]
        except:return list(self)[item]