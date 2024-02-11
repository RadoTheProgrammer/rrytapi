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