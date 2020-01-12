#this is supposed to be used to load the settings
import json
settings = json.load(open("./settings.json"))


def get_login(login_name):
    for login in settings['logins']:
        if login['name'] == login_name:
            return LoginCredentials(login)

def get_all_calendar_settings():
    output=[]
    for calSetting in settings['calendars']:
        output.append(CalendarSettings(calSetting))
    return output

def get_calendar_settings(calendar_name):
    for calSetting in settings['calendars']:
        if calSetting['name']==calendar_name:
            return CalendarSettings(calSetting)

def get_all_syncs():
    output=[]
    for sync in settings['syncs']:
        output.append(SyncSettings(sync))
    return output

class CalendarSettings:
    name=""
    url=""
    login=None
    connectionType=None
    def __init__(self,json):
        self.name=json['name']
        self.url=json['url']
        if ~(json['login'] is None):
            self.login=get_login(json['login'])
        self.connectionType=json['type']


class LoginCredentials:
    name=""
    username=""
    password=""

    def __init__(self,json):
        self.name = json['name']
        self.username = json['user']
        self.password = json['password']

class SyncSettings:
    source=None
    target=None
    where=""

    def __init__(self,json):
        self.source=get_calendar_settings(json['from'])
        self.target=get_calendar_settings(json['to'])
        self.where=json['where']

    def test_where(self,source_component):
        return True