import sys
import mimetypes
import time
import os

import requests
import rrprettier

from . import utils
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

class Format:
    size=videoQuality=videoQualityType=width=height=pixels\
    =qualityLabel=qualityType=fps=audioQuality=sampleRate=audioQualityType\
    =None
    def __init__(self,video,fmtData):
        self.video=video
        #ti.print("HELLO")
        #with utils-Info(self) as info:
        self.itag=int(fmtData["itag"])
        #print("Format %s"%info.itag)
        self._fmtData=fmtData
        protected=False
        #print("VVVVV%s"%self.video.url)
        try:
            self._url=fmtData["url"]
        except KeyError as _err:
            #print("decrypt...")
            protected=True
            self._url=video._player.decryptSigWithParams(fmtData["signatureCipher"])
        #print(protected)
        #print(self.url)
        self.protected=protected
        
        #webbrowser.open(self.url)
        #print(self.url)
        #assert 0
        #print(fmtData["mimeType"])

        self.mimeType,self.codecs=fmtData["mimeType"].split("; codecs=")
        self.codecs=eval(self.codecs) #pylint: disable=W0123:eval-used
        self.extension=mimetypes.guess_extension(self.mimeType)
        #self.videoOrAudio=info.mimeType.videoOrAudio
        self.bitrate=utils.Bitrate(fmtData["bitrate"])
        contentLength=fmtData.get("contentLength")

        self.contentLength=utils.BytesCount(contentLength) if contentLength else utils.getContentLength(self._url)

        #ti.print("getting content length")
        #contentLength=self.getContentLength()
        #ti.print("getted content length")
            #odata(self.video._data)
        #if info.contentLength and contentLength!=info.contentLength:
        #        print("Not same contentLength: %s != %s"%(contentLength,info.contentLength),file=sys.stderr)
        if "video" in self.mimeType:
            self.size=utils.Size(fmtData["width"],fmtData["height"])
            self.videoQuality=VideoQuality(fmtData["quality"],fmtData["qualityLabel"])

        self.hasAudio=False
        sampleRate=fmtData.get("audioSampleRate")

        if sampleRate:
            self.hasAudio=True
            self.audioQuality=AudioQuality(fmtData["audioQuality"],sampleRate)
        #ti.print("MIDDLE")
        

            
        if self.hasAudio:
            self.audioQuality=AudioQuality(fmtData["audioQuality"],sampleRate)


        #ti.print("BYE")
            #info.hasAudio=displaySetLen(hasAudio,5)
            #info.audioQuality=displaySetLen(audioQuality,16)
            #super().__init__(self.url,os.path.join(DLDIR,"{fmt.video.id} - {onlyalpha(fmt.video.title)} {fmt.videoOrAudio}#{fmt.itag}.{fmt.extension}"))
    def __repr__(self):
        videoinfo=""
        if "video" in self.mimeType:
            videoinfo=f" {self.videoQuality}"
        audioinfo=""
        if self.hasAudio:
            audioinfo=f" {self.audioQuality}"
        return utils.reprWithCls(
            f"{self.mimeType} {self.bitrate}{videoinfo}{audioinfo}"
            ,self)

    id=property(lambda self:self.itag)
    type=property(lambda self:self.mimeType)
    videoQualityType=qualityType=property(lambda self:self.videoQuality.qualityType)
    width=property(lambda self:self.size.width)
    height=property(lambda self:self.size.height)
    pixels=property(lambda self:self.videoQuality.qualityPixels)
    qualityLabel=property(lambda self:self.videoQuality.qualityLabel)
    fps=property(lambda self:self.videoQuality.fps)
    audioQualityType=property(lambda self:self.audioQualityType)
    sampleRate=property(lambda self:self.sampleRate)

         
    
    def download(self,fileDest="rrytapi_downloads/{utils.to_filename(self.video.title)}_{self.itag}{self.extension}",resume=True,printInfo=True,showInExplorerBool=True,chunk_size=8192,waitIntervalToPrint=1):

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
        contentLength=utils.getContentLength(self._url)
        assert contentLength==self.contentLength
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
            prt("Download resume at %s"%utils.BytesCount(downloaded))
        else:
            with open(fileDest,"wb"):pass
            downloaded=0
            headers={}
        sie()
        #print("CEST MONTRö")
        #print("GO")
        #if not fileDest:raise ValueError("Please put the fileDest")
        tt=ftt=time.time()

        with requests.get(self._url,stream=True,headers=headers,timeout=10) as res:
            res.raise_for_status()
            #show()
            for chunk in res.iter_content(chunk_size=chunk_size):
                with open(fileDest,"ab") as f:
                    f.write(chunk)
                downloaded+=chunk_size
                ndl+=chunk_size
                ntt=time.time()
                if ntt>tt+waitIntervalToPrint:
                    tt=ntt
                    perSecond=utils.BytesCount(ndl/(ntt-ftt))
                    download_percentage = round(downloaded / contentLength * 100, 1)
                    downloaded_bytes = utils.BytesCount(downloaded)
                    progress_bar = f"{download_percentage:0>4}% {downloaded_bytes}/{contentLength}  {perSecond}/s ETA:{utils.Duration(int((contentLength - downloaded) / perSecond))}"
                    prt(progress_bar)
                    pdl=0
        #r=requests.get(str(self),stream=True)
        prt("Downloaded")
        return fileDest

    _to_exclude=("video")




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
        if not isinstance(qualityLabel,QualityLabel):
            self.qualityLabel=QualityLabel(qualityLabel)
        self.qualityType =qualityType


    def __repr__(self):
        return str(self.qualityLabel)+"("+self.qualityType+")"
    
    type=property(lambda self:self.qualityType)
    qualityPixels=pixels=property(lambda self:self.qualityLabel.qualityPixels)
    fps=property(lambda self:self.qualityLabel.fps)
class AudioQuality:
    def __init__(self,qualityType,sampleRate):
        self.qualityType=qualityType.lower().replace("audio_quality_","")
        self.sampleRate=int(sampleRate)

    def __repr__(self):
        return str(self.sampleRate)+"Hz("+self.qualityType+")"
    
    type=property(lambda self:self.qualityType)
class Formats(dict):
    _fmt=None

    def __repr__(self):
        return rrprettier.prettify(self)





    def filtrer(self,condition):
        #print("LA CONDITION")

        return Formats({itag:fmt for itag,fmt in self.items() if condition(fmt)})
    #def download(self,url=defaultFileDest):
    #    url=defaultFileDest.format()
    @property
    def video(self):
        return self.filtrer(lambda fmt:'video' in fmt.mimeType)
    @property
    def audio(self):
        return self.filtrer(lambda fmt:'audio' in fmt.mimeType)
    @property
    def withAudio(self):
        return self.filtrer(lambda fmt:fmt.hasAudio)

    withoutAudio=property(lambda self:self.filtrer(lambda fmt:not fmt.hasAudio))

    @property
    def _mini_display(self):
        return f"<{len(self)} formats>"
    #__getattr__=__getitem__


class NoneFormats:
    def __getattr__(self,*a,**k):return self
    def __call__(self,*a,**k):return self
