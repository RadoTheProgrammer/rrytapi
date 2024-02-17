import urllib

from mini_lambda import x,Constant

from . import utils #pylint: disable=E0611:no-name-in-module
from . import video
import cleantext
import rrprettier

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
        return utils.printerWithCls({idx:el for idx,el in enumerate(self)},self)

    # def __getitem__(self,y):
    #     if type(y)==slice:item,idxTarget=y.start,y.stop
    #     else:item,idxTarget=y,0
    #     assert item is not None
    #     l=list(self)
    #     if type(item)==int:return l.__getitem__(y)
    #     idx=0
    #     for el in l:
    #         title=url=None
    #         try:
    #             title=el.title
    #             url=el.url
    #         except:pass
    #         t=type(el)
    #         good=False
    #         if item in (t,t.__name__,title,url):
    #             good=True
    #         elif issubclass(t,ListR):
    #             try:
    #                 el=el[item]
    #                 good=True
    #             except KeyError:pass
    #         if good:
    #             if idx==idxTarget:
    #                 return el
    #             idx+=1
    #     return {}[item]
    
class UnknownR:
    def __init__(self,key,value):
        self.key=key
        self.value=value
        #ajson(value)
    def __repr__(self):
        return "<UnknownRenderer: %s>"%self.key
class ShelfR(ListR):
    def __init__(self,data):
        self.title=utils.getText(data["title"])
        content=data["content"]
        #ajson(data)
        super().__init__((content.get("horizontalListRenderer") or content["verticalListRenderer"])["items"])
    def __repr__(self):
        return utils.printerWithCls(list(self),utils.tname(self)+" "+repr(self.title))
class PlayListR(ListR):
    def __init__(self,data):
        #mypkg.open_data(data)
        
        #with utils-Info(self) as info:
        self.id=id=utils.lambdas(data,(x,x["navigationEndpoint"]["watchEndpoint"]),x["playlistId"])
        self.title=utils.getText(data["title"])
        self.thumbnails=[utils.Thumbnails(ths) for ths in data["thumbnails"]]
        self.url=utils.to_yturl(data["viewPlaylistText"]["runs"][0]["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"])
        self.urlWithVideo=utils.to_yturl(data["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"])
        self.videoId=data["navigationEndpoint"]["watchEndpoint"]["videoId"]
        self.channel=getChannelInfo(data)
        super().__init__(data["videos"])
    def __repr__(self):
        return utils.printerWithCls(list(self),"%s %s in %s"%(utils.tname(self),repr(self.title),self.url))
class AdR:
    def __init__(self,data):
        #with utils-Info(self) as info:
        self.thumbnails=utils.Thumbnails(data)
        self.title=utils.getText(data["title"])
        #self.description=utils.MiniDisplay.firstChars(utils.getText(data["description"]))
        self.description=utils.getText(data["description"])
        self.website=utils.getText(data["websiteText"])
        point=data["navigationEndpoint"]
        xpoint=Constant(point,"point")
        self.url=utils.lambdas(data,(xpoint["commandMetadata"]["webCommandMetadata"],xpoint["urlEndpoint"]),x["url"])
def __repr__(self):
        return utils.reprWithCls("%s in %s"%(repr(self.title),self.website),self) #pylint: disable=E1101:no-member

class VideoR:
    def __init__(self,data,isChild=False,fromPlaylist=False):
        
            #mypkg.open_data(data)
            #assert 0
        #print(data["navigationEndpoint"])
        #print(open_json(data))
        #with utils-Info(self) as info:
        point=data["navigationEndpoint"]
        xpoint=Constant(point,"point")
        try:
            self.badges=getBadges(data.get("badges"),"label")
        except:
            #mypkg.open_data(data)
            assert 0
        hasbadgelive="LIVE" in self.badges
        islive=tuple(data.get("thumbnailOverlays",[{}])[0].keys())==("thumbnailOverlayToggleButtonRenderer",)
        self.islive=hasbadgelive or islive
        self.hasbadgelive=hasbadgelive
        err=None
        if hasbadgelive and not islive:
            print("HASBADGELIVE:%s != ISLIVE:%s "%(islive,hasbadgelive))
        if islive:self.badges.append("LIVE")
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
                            lambda:utils.getText(timestatus["text"])=="SHORTS",
                            lambda:timestatus["style"]=="SHORTS"):
                    b=func()
                    #print(b)
                    assert isShorts is None or b==isShorts
                    isShorts=b
        isExpectedShorts=False
        try:utils.lambdas(data,xpoint["watchEndpoint"],errmode=None)
        except:
            #dddd
            #print(isShorts)
            isShorts=True
            

        self.isShorts=isShorts
        
        try:
            #info.id=id=utils.lambdas(data,(x,xpoint["reelWatchEndpoint" if isShorts else "watchEndpoint"]),x["videoId"])
            self.id=id=data["videoId"]
        except:
            rrprettier.tofile(data)
            #mypkg.open_data(data)
            assert 0

        self.url=utils.to_yturl(utils.lambdas(data,xpoint["commandMetadata"]\
                        ["webCommandMetadata"]["url"],errmode="raise") or utils.YTWATCH+id)

        """
            print(lambdas(data,[xpoint["commandMetadata"]\
                        ["webCommandMetadata"]["url"]]))
        """


        if err:
            print(err+" url:%s"%self.url)
        if not isChild:
            self.thumbnails=utils.Thumbnails(data)
        #mypkg.open_data(data)
        self.title=cleantext.remove_emoji(utils.getText(data["title"]))
        #assert 0
        #assert 0
        if not isChild:
            
            self.channel=getChannelInfo(data)
        xLengthText=x["lengthText"]
        if not self.islive:
            self.duration=utils.Duration(utils.getText(utils.lambdas(data,([x["lengthText"]]+([] if isChild or isShorts else [x["thumbnailOverlays"][0]["thumbnailOverlayTimeStatusRenderer"]["text"]])))))
        if not isChild and not fromPlaylist:
            viewCountText=data.get("viewCountText")
            self.viewCount=utils.ViewCount(utils.getText(viewCountText)) if viewCountText else "?"
            #excexrpt:odata(data)
            try:
                self.description=utils.getText(data["detailedMetadataSnippets"][0]["snippetText"])
            except:
                self.description=None
        self.owner = self.author = self.channel #pylint: disable=E1101:no-member
    def __repr__(self):
        return utils.reprWithCls(repr(self.title),utils.tname(self)+(" LIVE" if self.islive else "")) #pylint: disable=E1101:no-member
    def get(self):
        return video.Video.get(self.url) #pylint: disable=E1101:no-member


class MovieR(VideoR):pass

class ChannelR:
    def __init__(self,data):
        #with utils-Info(self) as info:
        self.id=utils.lambdas(data,(x["channelId"],x["navigationEndpoint"]["browseEndpoint"]["browseId"]))
        self.name=utils.getText(data["title"])

        self.url=utils.to_yturl(utils.lambdas(data["navigationEndpoint"],(x["commandMetadata"]["webCommandMetadata"]["url"],x["browseEndpoint"]["canonicalBaseUrl"])))
        #open_json(data)
        channel=getChannelInfo(data,isChannel=True)

        assert self.id==channel.id #pylint: disable=E1101:no-member
        assert self.name==channel.name #pylint: disable=E1101:no-member
        self.badges=channel.badges #pylint: disable=E1101:no-member
        self.description=utils.getText(data["descriptionSnippet"])
        #print(data)
        count=utils.getText(data["videoCountText"])
        if "subscribers" in count:
            self.subscriberCount=0 if "No" in count else utils.viewcount(count)
        else:assert 0
            #info.videoCount=viewcount(getText(data["videoCountText"])[:-7])
        pseudo=utils.getText(data["subscriberCountText"])
        assert "@" in pseudo
        self.pseudo=pseudo

    def __repr__(self):
        return utils.reprWithCls("%s in %s"%(repr(self.name),self.url),self) #pylint: disable=E1101:no-member
class Channel(ListR):
    def __init__(self,data):
        #odata(data)
        contents=data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
        content=contents[0]["tabRenderer"]
        xcontent=Constant(content,"content")
        #with utils-Info(self) as info:
        self.name="UNDEFINED NAME"
        self.url=utils.to_yturl(utils.lambdas(data,(xcontent["endpoint"]["commandMetadata"]["webCommandMetadata"]["url"],
                            xcontent["endpoint"]["browseEndpoint"]["canonicalBaseUrl"]),lambda x:x[:-9] if x.endswith("/featured") else x)
                    )
        
        self.video=ChannelPlayerVideoR(content["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["channelVideoPlayerRenderer"])
        
    @classmethod
    def get(cls,url):
        return cls(utils.extractVar(url,"ytInitialData"))
    
class ChannelPlayerVideoR:
    def __init__(self,data):
        #with utils-Info(self) as info:
        run=data["title"]["runs"][0]
        xrun=Constant(run,"run")
        self.id=utils.lambdas(data,(x,xrun["navigationEndpoint"]["watchEndpoint"]),x["videoId"])
        self.title=run["text"]
        self.url=utils.to_yturl(run["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"])
        #self.description=utils.MiniDisplay.firstChars(utils.getText(data["description"]))
        self.description=utils.getText(data["description"])
        self.viewCount=utils.ViewCount(utils.getText(data["viewCountText"]))
        self.publishedTime=utils.getText(data["publishedTimeText"])
    def __repr__(self):
        return utils.reprWithCls("%s in %s"%(repr(self.title),self.url),self) #pylint: disable=E1101:no-member
    

def getBadges(data,key):
    if not data:return []
    return [badge["metadataBadgeRenderer"][key] for badge in data]

def getChannelInfo(data,isChannel=False):
    lmb=[]
    for name in ("shortBylineText","ownerText","longBylineText"):
        try:d=data[name]
        except:continue
        lmb.append(Constant(d,name))

    channel=utils.lambdas(data,lmb)["runs"][0]


    channelPoint=channel["navigationEndpoint"]

    thumbnails=data.get("channelThumbnailSupportedRenderers")
    thumbnails=[data["thumbnail"]] if isChannel else [data.get("channelThumbnailSupportedRenderers",{}).get("channelThumbnailWithLinkRenderer")]
    

    return utils.ChannelInfo(channel["text"],
                        channelPoint["browseEndpoint"]["browseId"],
                        utils.lambdas(
                            channelPoint,
                            (x["commandMetadata"]["webCommandMetadata"]["url"],
                            x["browseEndpoint"]["canonicalBaseUrl"]),
                            urllib.parse.unquote),
                        None if thumbnails in (None,[None]) else utils.Thumbnails(*thumbnails),
                       getBadges(data.get("ownerBadges"),"tooltip"))
