import sys

def showInExplorerFunc(file):
    import subprocess
    
    if sys.platform=="darwin":
        cmd="open -R %s"%repr(file)
    elif sys.platform=="win32":
        cmd='explorer /select, "%s"'%file
    else:
        return
    #print(cmd)
    return subprocess.call(cmd,shell=True)

class Format(Url):
    size=videoQuality=videoQualityType=width=height=pixels\
    =qualityLabel=qualityType=fps=audioQuality=sampleRate=audioQualityType\
    =None
    def __init__(self,video,fmtData):
        self.video=video
        #ti.print("HELLO")
        with Info(self) as info:
            info.itag=int(fmtData["itag"])
            #print("Format %s"%info.itag)
            self._fmtData=fmtData
            protected=False
            #print("VVVVV%s"%self.video.url)
            try:
                self.url=fmtData["url"]
            except:
                #print("decrypt...")
                protected=True
                self.url=video.player.decryptSigWithParams(fmtData["signatureCipher"])
            #print(protected)
            #print(self.url)
            info.protected=protected
            
            #webbrowser.open(self.url)
            #print(self.url)
            #assert 0
            #print(fmtData["mimeType"])

            info.mimeType,self.codecs=fmtData["mimeType"].split("; codecs=")
            self.codecs=eval(self.codecs)
            info.extension=mimetypes.guess_extension(info.mimeType)
            #self.videoOrAudio=info.mimeType.videoOrAudio
            info.bitrate=Bitrate(fmtData["bitrate"])
            contentLength=fmtData.get("contentLength")
            info.contentLength=BytesCount(contentLength) if contentLength else None
            #ti.print("getting content length")
            #contentLength=self.getContentLength()
            #ti.print("getted content length")
                #odata(self.video._data)
            #if info.contentLength and contentLength!=info.contentLength:
            #        print("Not same contentLength: %s != %s"%(contentLength,info.contentLength),file=sys.stderr)
            info.hasAudio=False
            sampleRate=fmtData.get("audioSampleRate")
            if sampleRate:
                info.hasAudio=True
                audioQuality=AudioQuality(fmtData["audioQuality"],sampleRate)
            #ti.print("MIDDLE")
            info.export()
            if "video" in self.mimeType:
                info.size=Size(fmtData["width"],fmtData["height"])

                info.videoQuality=VideoQuality(fmtData["quality"],fmtData["qualityLabel"])
                self.videoQualityType=self.qualityType=info.videoQuality.qualityType
                self.width=info.size.width
                self.height=info.size.height
                self.pixels=self.qualityPixels=info.videoQuality.qualityPixels
                self.qualityLabel=info.videoQuality.qualityLabel
                self.qualityType=info.videoQuality.qualityType
                self.fps=info.videoQuality.fps
                
            if info.hasAudio:
                info.audioQuality=AudioQuality(fmtData["audioQuality"],sampleRate)
                self.sampleRate=info.audioQuality.sampleRate
                self.audioQualityType=info.audioQuality.qualityType
            self.type=info.mimeType
            self.id=info.itag
        #ti.print("BYE")
            #info.hasAudio=displaySetLen(hasAudio,5)
            #info.audioQuality=displaySetLen(audioQuality,16)
            #super().__init__(self.url,os.path.join(DLDIR,"{fmt.video.id} - {onlyalpha(fmt.video.title)} {fmt.videoOrAudio}#{fmt.itag}.{fmt.extension}"))
    def __repr__(self):return reprWithCls(str(dict(self.info)),self)

    def download(self,fileDest="rrytapi_downloads/{to_filename(self.video.title)}_{self.itag}{self.extension}",resume=True,printInfo=True,showInExplorerBool=True,chunk_size=8192,waitIntervalToPrint=1):

        global show
        #show=lambda:subprocess.call(["open","-R",repr(fileDest)]) if showInFinder else lambda:None
#         print(fileDest)
        if showInExplorerBool:
            def sie():
                showInExplorerFunc(fileDest)
                time.sleep(2)
        else:
            sie=lambda:None
        #if extension:
        #    fileDest+="."+extension
        """
        for _ in range(10):
            show()
            time.sleep(1)
            print("SHOWD")
        """
        prt=print if printInfo else lambda a:a
        #print(self)
        #print(type(self))
        #print(vars(self))
        #[K[download]  24.6% of 2.69MiB at  4.99KiB/s ETA 06:5
        #contentLength=tryexec(getContentLength)
        contentLength=self.getContentLength()
        
        """
        try:
            sContentLength=self.contentLength
            assert sContentLength
        except:pass
        else:
            if contentLength!=sContentLength:
                prt("Not same contentLength: %s != %s"%(contentLength,sContentLength),file=sys.stderr)
        """
        #print("BEFORE: %s"%fileDest)
        fileDest=eval("f"+repr(fileDest),globals(),locals())
        dir=os.path.dirname(fileDest)
        if dir:
            os.makedirs(dir,exist_ok=True)
        #print("AFTER: %s"%fileDest)
        prt("Download %s to %s..."%(contentLength.display(True),repr(fileDest)))
        ndl=0
        if resume and os.path.exists(fileDest):
            with open(fileDest,"ab"):pass
            downloaded=os.path.getsize(fileDest)
            if downloaded>=contentLength:
                #downloaded-=1
                prt("Downloaded (already)")
                sie()
                return fileDest
            headers={"Range":"bytes=%s-"%downloaded}
            prt("Download resume at %s"%BytesCount(downloaded))
        else:
            with open(fileDest,"wb"):pass
            downloaded=0
            headers={}
        sie()
        #print("CEST MONTRö")
        #print("GO")
        #if not fileDest:raise ValueError("Please put the fileDest")
        tt=ftt=time.time()
        with requests.get(self.url,stream=True,headers=headers) as res:
            res.raise_for_status()
            #show()
            for chunk in res.iter_content(chunk_size=chunk_size):
                with open(fileDest,"ab") as f:
                    f.write(chunk)
                downloaded+=chunk_size
                ndl+=chunk_size
                ntt=time.time()
                if ntt>tt+waitIntervalToPrint:
                    #print("HELLO")
                    tt=ntt
                    perSecond=BytesCount(ndl/(ntt-ftt))
                    download_percentage = round(downloaded / contentLength * 100, 1)
                    downloaded_bytes = BytesCount(downloaded)
                    progress_bar = f"Download Progress: {download_percentage:0>4}% {downloaded_bytes}/{contentLength}  {perSecond}/s last:{Duration(int((contentLength - downloaded) / perSecond))}"
                    prt(progress_bar)
                    pdl=0
        #r=requests.get(str(self),stream=True)
        prt("Downloaded")
        return fileDest
class Size:
    def __init__(self,width,height):
        self.width=int(width)
        self.height=int(height)
    def __repr__(self):
        return str(self.width)+"x"+str(self.height)
    def __iter__(self):return iter((self.width,self.height))

    def __lt__(self,size):
        size=Size(*size)
        return (self.width,self.height)<(size.width,size.height)



class QualityLabel:
    def __init__(self,qualityLabel):
        if type(qualityLabel)==int:qualityLabel=str(qualityLabel)
        qualityLabel=qualityLabel.split("p")
        self.qualityPixels=int(qualityLabel[0])
        try:
            self.fps=int(qualityLabel[1])
            assert self.fps
        except:
            self.fps=None
    def __repr__(self):
        return "%sp%s"%(self.qualityPixels,self.fps if self.fps else "")
class VideoQuality:
    def __init__(self,qualityType,qualityLabel):
        self.qualityType = self.type = qualityType
        self.qualityPixels=self.pixels=qualityLabel.qualityPixels
        self.qualityLabel=QualityLabel(qualityLabel)
        self.fps=self.qualityLabel.fps


    def __repr__(self):
        return str(self.qualityLabel)+" ("+self.qualityType+")"
    
class AudioQuality:
    def __init__(self,qualityType,sampleRate):
        self.qualityType=qualityType.lower().replace("audio_quality_","")
        self.sampleRate=int(sampleRate)
    type=aliasprop("self.qualityType")
    def __repr__(self):
        return str(self.sampleRate)+"Hz ("+self.qualityType+")"
    
class NoneFormats:
    def __getattr__(self,*a,**k):return self
    def __call__(self,*a,**k):return self
