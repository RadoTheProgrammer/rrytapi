import urllib
from . import utils

def search(query):
    url="https://www.youtube.com/results?search_query="+urllib.parse.quote(query)
    #print(url)
    contents=[]
    for c in utils.extractVar(
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
            info.title=cleantext.remove_emoji(getText(data["title"]))
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
