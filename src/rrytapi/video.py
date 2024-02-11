import time

import cleantext
from mini_lambda import x, Constant
import requests

from . import utils
from . import player
from . import videoformats



acceptLang={"Accept-Language": "en-US"}

class Video:
    def __init__(self,webpage):
        data=self._data=utils.extractVar(webpage,"ytInitialPlayerResponse")
        #ti.print("webpage getted")
        #odata(data)
        streaming=data["streamingData"]
        details=data["videoDetails"]
        xdetails=Constant(details,"details")
        microformat=data["microformat"]["playerMicroformatRenderer"]
        xmicroformat=Constant(microformat,"microformat")
        

        with utils.Info(self) as info:
            info.id=details["videoId"]
            info.url=utils.Url(utils.YTWATCH+info.id)
            #open_json(details)
            info.islive=utils.lambdas(data,(x["responseContext"]["serviceTrackingParams"][0]["params"][0]["value"]=="True",
                                      Constant(bool)(x["playabilityStatus"].get("liveStreamability")),
                                      xdetails["isLiveContent"]))
            #odata(data)
            info.title=cleantext.remove_emoji(utils.lambdas(data,(xdetails,(xmicroformat,utils.getText)),x["title"]))
            l=utils.lambdas(data,(xdetails,xmicroformat),Constant(int)(x["lengthSeconds"]),funcVerifIfSame=lambda x,y:abs(x-y)<2)
            #print(l)
            info.duration=utils.Duration(l)
            #print(info.lengthSeconds)
            #print(Duration(l))
            #print(type(info.lengthSeconds))
            keywords=details.get("keywords",[])
            #odata(data)
            info.keywords=utils.MiniDisplay.withL(keywords,"keywords")
            info.thumbnails=utils.MiniDisplay.withL(utils.Thumbnails(details,microformat),"thumbnails")
            info.viewCount=utils.ViewCount(utils.lambdas(data,(xdetails,xmicroformat),x["viewCount"]))
            info.channel=utils.ChannelInfo(utils.lambdas(data,(xdetails["author"],xmicroformat["ownerChannelName"])),
                               utils.lambdas(data,(xdetails["channelId"],xmicroformat["externalChannelId"])),
                               microformat["ownerProfileUrl"])
            info.export()
            #ti.print("player...")
            self.player=player.Player.fromVideo(webpage)
            #ti.print("played...")
            formats=videoformats.Formats()
            #ti.print("formated")
            for fmt in streaming.get("formats",[])+streaming.get("adaptiveFormats",[]):
                #ti.print("new format")
                formats.append(self.Format(fmt))
            #ti.print("f1")
            info.formats=utils.MiniDisplay.withL(formats,"formats")
            #ti.print("ff")
        self.videoId=self.id #pylint: disable=E1101:no-member
        self.videoUrl=self.url #pylint: disable=E1101:no-member
        self.length=self.seconds=self.lengthSeconds=self.duration #pylint: disable=E1101:no-member
        self.owner=self.author=self.channel #pylint: disable=E1101:no-member
        self.download=self.formats.download #pylint: disable=E1101:no-member
        #print(self.title)
    def __repr__(self):
        return utils.reprWithCls("%s in %s"%(repr(self.title),self.url),self) #pylint: disable=E1101:no-member
    def Format(self,fmtData):
        return videoformats.Format(self,fmtData)
    @classmethod
    def get(cls,video_or_url,tries=30,wait=1):
        utils.ti.start()
        if isinstance(video_or_url,Video):return video_or_url
        try:
            url=video_or_url.url
        except AttributeError:
            url=video_or_url
        url=utils.YTWATCH+utils.getVideoId(str(url))+"&bcptr=9999999999&has_verified=1"
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
            except utils.ContentLengthError as e:err=e
            #ti.print("cls")
            time.sleep(wait)
            #ti.print("FAIL")
        raise err
    
get_video=Video.get

