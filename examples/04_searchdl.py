"""
Search on youtube, then download
"""

import rrytapi
r=rrytapi.search("jvke autumn")
v=r[0].get()
print(v)
v.download()