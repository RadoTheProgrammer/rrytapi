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
            info.title=cleantext.remove_emoji(lambdas(data,(xdetails,(xmicroformat,getText)),x["title"]))
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
