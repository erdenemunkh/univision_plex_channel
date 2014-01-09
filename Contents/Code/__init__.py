####################################################################################################

PREFIX = '/video/univision'
NAME = 'Univision'

VERSION = 99
LOGIN_URL = 'http://my.univision.mn/user/loginformobile'
GET_CHANNELS_URL = 'http://tv.univision.mn/tv/xml?id=%s'
GET_SCHEDULE_URL = 'http://tv.univision.mn/tv/xmlByChannel?username=%s&channel=%s&date=%s'
GET_LIVE_STREAM_URL = 'http://tv.univision.mn/tv/getStreamUrl?version=' + str(VERSION) + '&username=%s&live=%s'
GET_ARCHIVE_STREAM_URL = 'http://tv.univision.mn/tv/getStreamUrl?version=' + str(VERSION) + '&username=%s&archive=%s'

LIVE_STREAM_URL = 'http://202.70.32.50/hls/_definst_/tv_mid/%s/playlist.m3u8?%s'
ARCHIVE_STREAM_URL = 'http://202.70.32.50/vod/_definst_/mp4:tv/medium/%s/playlist.m3u8?%s'

SESSION_ID = ''

CHANNELS = { }
CHANNELS['24'] = {'id': '24', 'date': '2014-01-01', 'title': unicode('MNB 2'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_mnb_2', 'url': 'smil:mnb_2.smil'}
CHANNELS['42'] = {'id': '42', 'date': '2014-01-01', 'title': unicode('Parliament'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_parliament', 'url': 'parliament.stream'}
CHANNELS['1'] = {'id': '1', 'date': '2014-01-01', 'title': unicode('МҮОНТВ'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_mnb', 'url': 'smil:mnb.smil'}
CHANNELS['22'] = {'id': '22', 'date': '2014-01-01', 'title': unicode('MN25'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_tv25', 'url': 'smil:mn25.smil'}
CHANNELS['3'] = {'id': '3', 'date': '2014-01-01', 'title': unicode('UBS'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_ubs', 'url': 'smil:ubs.smil'}
CHANNELS['25'] = {'id': '25', 'date': '2014-01-01', 'title': unicode('EagleTV'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_eagle', 'url': 'smil:eagle.smil'}
CHANNELS['4'] = {'id': '4', 'date': '2014-01-01', 'title': unicode('NTV'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_ntv', 'url': 'smil:ntv.smil'}
CHANNELS['5'] = {'id': '5', 'date': '2014-01-01', 'title': unicode('ETV HD'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_etv', 'url': 'smil:etv.smil'}
CHANNELS['23'] = {'id': '23', 'date': '2014-01-01', 'title': unicode('EDU'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_bolovsrol', 'url': 'smil:edu.smil'}
CHANNELS['26'] = {'id': '26', 'date': '2014-01-01', 'title': unicode('TV5'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_tv5', 'url': 'smil:tv5.smil'}
CHANNELS['27'] = {'id': '27', 'date': '2014-01-01', 'title': unicode('SBN'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_sbn', 'url': 'smil:sbn.smil'}
CHANNELS['31'] = {'id': '31', 'date': '2014-01-01', 'title': unicode('TV9'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_tv9', 'url': 'smil:tv9.smil'}
CHANNELS['9'] = {'id': '9', 'date': '2014-01-01', 'title': unicode('Эх орон HD'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_eh_oron', 'url': 'smil:ehoron.smil'}
CHANNELS['41'] = {'id': '41', 'date': '2014-01-01', 'title': unicode('Bloomberg HD'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_bloomberg', 'url': 'smil:bloomberg.smil'}
CHANNELS['2'] = {'id': '2', 'date': '2014-01-01', 'title': unicode('Монгол HD'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_mongolhd', 'url': 'smil:mongolhd.smil'}
CHANNELS['32'] = {'id': '32', 'date': '2014-01-01', 'title': unicode('SportBox'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_sportbox', 'url': 'smil:sportbox.smil'}
CHANNELS['38'] = {'id': '38', 'date': '2014-01-01', 'title': unicode('Royal HD'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_royal_hd', 'url': 'smil:royal.smil'}
CHANNELS['39'] = {'id': '39', 'date': '2014-01-01', 'title': unicode('MNC HD'), 'schedule': '', 'scheduletoday': '', 'image': 'logo_mon_mnc', 'url': 'smil:mnc.smil'}


####################################################################################################
def Start():
    HTTP.CacheTime = 5*CACHE_1MINUTE
    HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0'
    
def ValidatePrefs():
    login_failed = Login()
    if login_failed:
        return login_failed
    return None

####################################################################################################
@handler(PREFIX, NAME)
def MainMenu():
    if not LoggedIn():
        Login()
    UpdateChannels()
    
    oc = ObjectContainer(title1=NAME)
    
    for id in CHANNELS:
        channel = CHANNELS[id]
        oc.add(DirectoryObject(key = Callback(ChannelMenu, id=id, date=channel['date']), title=channel['title'], summary=channel['schedule'], thumb=R('%s.png' % channel['image'])))
    
    oc.add(PrefsObject(title=L('Preferences')))
    
    return oc

@route(PREFIX + '/{id}/{date}')
def ChannelMenu(id, date):
    if not LoggedIn():
        login_failed = Login()
        if login_failed:
            return login_failed
    
    channel = CHANNELS[id]
    
    oc = ObjectContainer(title2=('%s %s' % (channel['title'], date)))
    
    oc.add(VideoClipObject(url=GetArchiveStream(channel['url']), title=L("Live Stream")))
    day = date
    prev_day = (Datetime.ParseDate(day) - Datetime.Delta(days = 1)).strftime("%Y-%m-%d")
    next_day = (Datetime.ParseDate(day) + Datetime.Delta(days = 1)).strftime("%Y-%m-%d")
    oc.add(DirectoryObject(key = Callback(ChannelMenu, id=id, date=prev_day), title = prev_day))
    if day != channel['date']:
        oc.add(DirectoryObject(key = Callback(ChannelMenu, id=id, date=next_day), title = next_day))
        
    try:
        xml = HTTP.Request(url=(GET_SCHEDULE_URL % (Prefs['username'], id, date)), cacheTime=CACHE_1MINUTE)
        
        for schedule_xml in XML.ElementFromString(xml).xpath('//item'):
            starttime = Datetime.ParseDate(schedule_xml.xpath('./starttime')[0].text.strip()).strftime("%H:%M")
            endtime = Datetime.ParseDate(schedule_xml.xpath('./endtime')[0].text.strip()).strftime("%H:%M")
            title = schedule_xml.xpath('./title')[0].text.strip()
            archiveurl = ''
            try:
                archiveurl = schedule_xml.xpath('./archiveurl')[0].text.strip()
            except:
                pass
            if archiveurl:
                oc.add(VideoClipObject(url=GetArchiveStream(archiveurl), title=("%s %s" % (starttime, title))))
    except:
        Log.Exception('ChannelMenu(id, date) exception')
        pass
    
    return oc

####################################################################################################
def LoggedIn():
    return SESSION_ID

def Login():
    global SESSION_ID
    SESSION_ID = ''
    
    if Prefs['username'] == "" and not Prefs['password'] == "":
        return ObjectContainer(header=L('Login'), message=L('Enter your username and password in Preferences.'))
    
    try:
        post = {
                'username' : Prefs['username'],
                'password' : Prefs['password']
        }
        headers = { }
        successful = HTTP.Request(LOGIN_URL, post, headers).content.strip()
        
        if successful == '1':
            content = HTTP.Request(url=(GET_LIVE_STREAM_URL % (Prefs['username'], '')), cacheTime=0).content.strip()
            index = content.index('?')
            if index >= 0:
                SESSION_ID = content[index+1:]
            return None
    except:
        Log.Exception('Login() exception')
        pass
    
    return ObjectContainer(header=L('Login Failed'), message=L('Please check your username and password in Preferences.'))

def UpdateChannels():
    global CHANNELS
    
    try:
        xml = HTTP.Request(url=(GET_CHANNELS_URL % Prefs['username']), cacheTime=5*CACHE_1MINUTE)
        
        for channel_xml in XML.ElementFromString(xml).xpath('//item'):
            id = channel_xml.xpath('./id')[0].text.strip()
            CHANNELS[id]['date'] = channel_xml.xpath('./date')[0].text.strip()
            try:
                CHANNELS[id]['schedule'] = channel_xml.xpath('./schedule')[0].text.strip()
            except:
                pass
            try:
                CHANNELS[id]['scheduletoday'] = channel_xml.xpath('./scheduletoday')[0].text.strip()
            except:
                pass
    except:
        Log.Exception('UpdateChannels() exception')
        pass

def GetLiveStream(liveurl, fetch_from_server=False):
    if not fetch_from_server:
        return LIVE_STREAM_URL % (liveurl, SESSION_ID)
    
    try:
        content = HTTP.Request(url=(GET_LIVE_STREAM_URL % (Prefs['username'], liveurl)), cacheTime=CACHE_1MINUTE).content.strip()
        return content
    except:
        Log.Exception('GetLiveStream(liveurl) exception')
        pass
    return ""

def GetArchiveStream(archiveurl, fetch_from_server=False):
    if not fetch_from_server:
        return ARCHIVE_STREAM_URL % (archiveurl, SESSION_ID)
    
    try:
        content = HTTP.Request(url=(GET_ARCHIVE_STREAM_URL % (Prefs['username'], archiveurl)), cacheTime=CACHE_1MINUTE).content.strip()
        return content
    except:
        Log.Exception('GetLiveStream(channel) exception')
        pass
    return ""

####################################################################################################