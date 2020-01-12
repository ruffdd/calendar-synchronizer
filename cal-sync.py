#!/usr/bin/env python3
import os

import caldav
import icalendar
import requests
from caldav.elements import cdav, dav
from datetime import datetime
import settings
import easywebdav



def getCalendarIcs(url):
    request = requests.get(url)
    assert (request.status_code == 200)
    calendar = icalendar.Calendar.from_ical(request.content)
    return calendar

def getCalendarCalDav(calendar_settings):
    username = None
    password = None
    if ~(calendar_settings.login is None):
        username=calendar_settings.login.username
        password=calendar_settings.login.password
    client = caldav.DAVClient(calendar_settings.url,username=username,password=password,ssl_verify_cert=True)
    output = client.principal().calendars()[0]
    return output


def getCalendarIcsFile(path):
    return icalendar.Calendar.from_ical(open(path).read())

def getUrl(event):
    url = str(event)
    url = url.replace("[Event(","",1)
    url = url.replace(")]","",1)
    return url



calendars_settings = settings.get_all_calendar_settings()
sync_settings = settings.get_all_syncs()

for sync in sync_settings:
    input_calendar = icalendar.Calendar()
    output_calendar = getCalendarCalDav(sync.target)
    if sync.source.connectionType == 'ics':
        getCalendarIcs(sync.source)
    elif sync.source.connectionType == 'caldav':
        print('input from caldav not supproted')
        continue
    elif sync.source.connectionType == 'icsfile':
        input_calendar = getCalendarIcsFile(sync.source.url)
    else :
        print('type not known')
        continue

    empty_input_calendar = icalendar.Calendar()
    for key in input_calendar.keys():
        if key == 'METHOD':
            continue
        empty_input_calendar.add(key,input_calendar.get(key))

    for component in input_calendar.subcomponents:
        if sync.test_where(component):
            wrap_calendar = empty_input_calendar.copy()
            wrap_calendar.add_component(component)
            output_calendar.add_event(wrap_calendar.to_ical().decode())
