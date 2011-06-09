#This is an awesome python script that will download a whole bunch of cool wallpapers from
#Desktopograpy, sexy!


import pycurl
import re
import StringIO
import urllib2


site="http://desk10.customize.org/exhibitions/6"
dlsite = "http://desk10.customize.org/media/"
dldirec = "/home/marco/wallpapers/"



#first lets curl the site
def getSiteInfo():
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, site)
    string = StringIO.StringIO() 
    curl.setopt(pycurl.WRITEFUNCTION, string.write)
    curl.perform()
    return string.getvalue()

def getWallpaperLocations():
    siteInfo = getSiteInfo()
    siteInfo = siteInfo.split("\n")
    locations = []
    numberLocations = []
    for line in siteInfo:
        if(line.find('/wallpapers')!=-1):
            #print line #this is debugging should be removed later
            locations.append(line)
    for location in locations:
        m = re.search('(?<=(wallpapers/))\w+', location)
        numberLocations.append(m.group(0))
    #print numberLocations
    return numberLocations


def getWallpaperInfo(wallpaperNumber,lineIdentifier, regEX=None):
    if (regEX == None):
        regEX=lineIdentifier
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, site+'/wallpapers/'+str(wallpaperNumber))
    string = StringIO.StringIO() 
    curl.setopt(pycurl.WRITEFUNCTION, string.write)
    curl.perform()
    siteInfo = string.getvalue()
    siteInfo = siteInfo.split("\n")
    locations = []
    fileLocations = []
    for line in siteInfo:
        if(line.find(lineIdentifier)!=-1):
            #print line #this is debugging should be removed later
            locations.append(line)
    for location in locations:
        m = re.search('(?<=('+regEX+'))\w+', location)
        fileLocations.append(m.group(0))
    #print fileLocations
    return fileLocations

def getWallpaperName(wallpaperNumber):
    name = getWallpaperInfo(wallpaperNumber, '<h2 id="title"', '>  ')
    return name[0]

def getWallpaperDownloadLocations(wallpaperNumber):
    dlLocations = getWallpaperInfo(wallpaperNumber, 'value="/media/')
    return dlLocations

def downloadWallpaper(wallpaperNumber):
    name = getWallpaperName(wallpaperNumber)
    #This is 0 becuase I want the highest quality one, nothing but the best
    location = getWallpaperDownloadLocations(wallpaperNumber)[0]
    wallpaperFile = urllib2.urlopen(dlsite+location)
    # the wb means write and make it binary so it stores data and not just
    # text
    output = open(dldirec+name+'.jpg','wb')
    output.write(wallpaperFile.read())
    output.close()

def downloadAllWallpapers():
    numberLocations = getWallpaperLocations()
    for number in numberLocations:
        downloadWallpaper(number)
if __name__=="__main__":
    print "Hi There welcome Python Desktopography wallpaper downloader! v1 :D"
    print "A wallpaper DLer written in fewer than 100 lines of code, Sexy!"
    downloadAllWallpapers()
