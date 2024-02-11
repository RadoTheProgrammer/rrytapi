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