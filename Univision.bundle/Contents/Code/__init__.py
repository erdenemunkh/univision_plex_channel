####################################################################################################

PREFIX = '/video/univision'
NAME = 'Univision'

VERSION = 99
LOGIN_URL = 'http://my.univision.mn/user/loginformobile'
GET_CHANNELS_URL = 'http://tv.univision.mn/tv/xml?id=%s'
GET_SCHEDULE_URL = 'http://tv.univision.mn/tv/xmlByChannel?username=%s&channel=%s&date=%s'
GET_LIVE_STREAM_URL = 'http://tv.univision.mn/tv/getStreamUrl?version=' + str(VERSION) + '&username=%s&live=%s'
GET_ARCHIVE_STREAM_URL = 'http://tv.univision.mn/tv/getStreamUrl?version=' + str(VERSION) + '&username=%s&archive=%s'

#ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################
def Start():
    #ObjectContainer.title1 = NAME
    #ObjectContainer.art = R(ART)
    #DirectoryObject.thumb = R(ICON)
    #PopupDirectoryObject.thumb = R(ICON)
    
    HTTP.CacheTime = 5*CACHE_1MINUTE


####################################################################################################
@handler(PREFIX, NAME)
def MainMenu():
    oc = ObjectContainer(title1=NAME)
    
    oc.add(DirectoryObject(key = Callback(ChannelsMenu, title = L('Channels')), title = L('Channels')))
    oc.add(DirectoryObject(key = Callback(MoviesMenu, title = L('Movies')), title = L('Movies')))
    oc.add(DirectoryObject(key = Callback(VideosMenu, title = L('Videos')), title = L('Videos')))
    
    oc.add(PrefsObject(title=L('Preferences')))
    
    return oc

@route(PREFIX + '/channels')
def ChannelsMenu(title):
    if not LoggedIn():
        login_failed = Login()
        if login_failed:
            return login_failed
        
    oc = ObjectContainer(title1=title, title2=title)
    
    try:
        xml = HTTP.Request(url=(GET_CHANNELS_URL % Prefs['username']), cacheTime=CACHE_1MINUTE)
        
        channels = XML.ElementFromString(xml).xpath('//item')
        for i in range(len(channels)):
            channel = {}
            channel['id'] = channels[i].xpath('./id')[0].text.strip()
            channel['date'] = channels[i].xpath('./date')[0].text.strip()
            channel['title'] = channels[i].xpath('./title')[0].text.strip()
            channel['schedule'] = ''
            try:
                channel['schedule'] = channels[i].xpath('./schedule')[0].text.strip()
            except:
                pass
            channel['scheduletoday'] =''
            try:
                channel['scheduletoday'] = channels[i].xpath('./scheduletoday')[0].text.strip()
            except:
                pass
            channel['image'] = channels[i].xpath('./image')[0].text.strip()
            channel['url'] = channels[i].xpath('./url')[0].text.strip()
            
            oc.add(DirectoryObject(key = Callback(ChannelMenu, id=channel['id'], date=channel['date'], channel=channel), title = channel['title']))
            
    except:
        Log.Exception('ChannelsMenu(title) exception')
        pass
    
    return oc

@route(PREFIX + '/movies')
def MoviesMenu(title):
    oc = ObjectContainer(title1=title, title2=title)
    return oc

@route(PREFIX + '/videos')
def VideosMenu(title):
    oc = ObjectContainer(title1=title, title2=title)
    return oc

@route(PREFIX + '/channels/{id}/{date}', channel=dict)
def ChannelMenu(id, date, channel):
    oc = ObjectContainer(title1=channel['title'], title2=channel['title'])
    
    oc.add(VideoClipObject(url=GetLiveStream(channel), title=("%s Live Stream" % channel['title'])))
    day = date
    prev_day = (Datetime.ParseDate(day) - Datetime.Delta(days = 1)).strftime("%Y-%m-%d")
    next_day = (Datetime.ParseDate(day) + Datetime.Delta(days = 1)).strftime("%Y-%m-%d")
    oc.add(DirectoryObject(key = Callback(ChannelMenu, id=id, date=prev_day, channel=channel), title = prev_day))
    if day != channel['date']:
        oc.add(DirectoryObject(key = Callback(ChannelMenu, id=id, date=next_day, channel=channel), title = next_day))
        
    try:
        xml = HTTP.Request(url=(GET_SCHEDULE_URL % (Prefs['username'], id, date)), cacheTime=CACHE_1MINUTE)
        
        items = XML.ElementFromString(xml).xpath('//item')
        for i in range(len(items)):
            schedule = {}
            schedule['starttime'] = Datetime.ParseDate(items[i].xpath('./starttime')[0].text.strip()).strftime("%H:%M")
            schedule['endtime'] = Datetime.ParseDate(items[i].xpath('./endtime')[0].text.strip()).strftime("%H:%M")
            schedule['title'] = items[i].xpath('./title')[0].text.strip()
            schedule['archiveurl'] = ''
            try:
                schedule['archiveurl'] = items[i].xpath('./archiveurl')[0].text.strip()
            except:
                pass
            
            oc.add(VideoClipObject(url=GetArchiveStream(schedule), title=("%s-%s %s" % (schedule['starttime'], schedule['endtime'], schedule['title']))))
    except:
        Log.Exception('ChannelsMenu(title) exception')
        pass
    
    return oc

####################################################################################################
def LoggedIn():
    logged = False
    try:
        content = HTTP.Request(url=(GET_LIVE_STREAM_URL % (Prefs['username'], '')), cacheTime=0).content.strip()
        logged = content != ""
    except:
        Log.Exception('LoggedIn() exception')
        pass
    return logged

def Login():
    if Prefs['username'] == "" and not Prefs['password'] == "":
        return ObjectContainer(header=L('Login'), message=L('Enter your username and password in Preferences.'))
    
    try:
        post = {
                'username' : Prefs['username'],
                'password' : Prefs['password']
        }
        headers = { }
        login = HTTP.Request(LOGIN_URL, post, headers).content.strip()
        
        if login == '1':
            return None
    except:
        Log.Exception('Login() exception')
        pass
    
    return ObjectContainer(header=L('Login Failed'), message=L('Please check your username and password in Preferences.'))

def GetLiveStream(channel):
    try:
        content = HTTP.Request(url=(GET_LIVE_STREAM_URL % (Prefs['username'], channel['url'])), cacheTime=CACHE_1MINUTE).content.strip()
        return content
    except:
        Log.Exception('GetLiveStream(channel) exception')
        pass
    return ""

def GetArchiveStream(schedule):
    try:
        content = HTTP.Request(url=(GET_ARCHIVE_STREAM_URL % (Prefs['username'], schedule['archiveurl'])), cacheTime=CACHE_1MINUTE).content.strip()
        return content
    except:
        Log.Exception('GetLiveStream(channel) exception')
        pass
    return ""

####################################################################################################