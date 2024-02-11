import rrprettier

class Info(dict):
    def __init__(self,src):
        self.src=src
        self.to_exclude=None
    def __enter__(self):
        self.to_exclude=set(dir(self.src))

    def __exit__(self,errtype,err,tb):
        for attr in set(dir(self.src))-self.to_exclude:
            if attr not in self:
                self[attr] = getattr(self.src,attr)
    
    __repr__=rrprettier.prettify


