from mini_lambda import x,Constant

from . import utils
from . import searcher

class Playlist(list):
    def __init__(self,data):
        #odata(data)

        #with utils-Info(self) as info:
        renderer=data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]\
                ["contents"][0]["itemSectionRenderer"]["contents"][0]["playlistVideoListRenderer"]
        xrenderer=Constant(renderer,"renderer")
        idx=0
        for videoData in renderer["contents"]:
            #ajson(videoData)
            if videoData.get("continuationItemRenderer"):continue
            #print(idx)
            self.append(
                searcher.VideoR(videoData["playlistVideoRenderer"],fromPlaylist=True)
            )
            #videos.append(video)
            idx+=1
        self.videos=utils.MiniDisplay.withL(self,"videos")
        header=data["header"]["playlistHeaderRenderer"]
        #ajson(header)
        xheader=Constant(header,"header")
        microformat=data["microformat"]["microformatDataRenderer"]
        xmicroformat=Constant(microformat,"microformat")
        metadata=data["metadata"]["playlistMetadataRenderer"]
        xmetadata=Constant(metadata,"metadata")
        self.id=utils.lambdas(data,(xrenderer["playlistId"],xrenderer["targetId"],xheader["playlistId"],
                                xheader["serviceEndpoints"][0]["playlistEditEndpoint"]["actions"][0]["sourcePlaylistId"]))
        # xbutton=x["button"]["buttonRenderer"]["navigationEndpoint"]["signInEndpoint"]["nextEndpoint"]\
        #                      ["commendMetadata"]["webCommandMetadata"]
        self.url=utils.Url(utils.lambdas(data,(xheader["saveButton"]["toggleButtonRenderer"]["defaultNavigationEndpoint"]\
                                ["modalEndpoint"]["modal"]["modalWithTitleAndButtonRenderer"]["button"]\
                                ["buttonRenderer"]["navigationEndpoint"]["signInEndpoint"]["nextEndpoint"]\
                                ["commandMetadata"]["webCommandMetadata"]["url"],
                                    xmicroformat["urlCanonical"],
                                    xmicroformat["iosAppArguments"],
                                    xmicroformat["linkAlternates"][0]["hrefUrl"],
                            
                                    ),
                                utils.Url))
        
        #info.videoId=header["playEndpoint"]["watchEndpoint"]["videoId"]
        #info.urlWithVideo=Url(lambdas(data,xheader["playEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]))
        self.title=utils.lambdas(data,(Constant(utils.getText)(xheader["title"]),xmetadata["title"],
                                    xmicroformat["title"]))
        self.videosNumber=int(utils.getText(utils.lambdas(data,(xheader["numVideosText"],xheader["stats"][0]))).partition(" ")[0])
        description=utils.lambdas(data,(Constant(utils.getText)(xheader["descriptionText"]),xmetadata["description"]))
        self.description=utils.MiniDisplay(description,microformat["description"])
        self.channel=searcher.getChannelInfo(header)
        self.viewCount=utils.ViewCount(utils.getText(utils.lambdas(data,(xheader["viewCountText"],xheader["stats"][1]))))
        self.thumbnails=utils.MiniDisplay.withL(utils.Thumbnails(microformat),"thumbnails")
    @classmethod
    def get(cls,url):
        url=utils.YTPLAYLIST+utils.getPlaylistId(url)
        #print(url)
        return cls(utils.extractVar(url,"ytInitialData"))
    def __repr__(self):
        return utils.printerWithCls(list(self),f"{utils.tname(self)} {repr(self.title)} in {self.url}") #pylint: disable=E1101:no-member
    
get_playlist=Playlist.get