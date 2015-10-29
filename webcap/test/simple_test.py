#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import datetime


def create_dates_select():
    d = (u"周日", u"周一", u"周二", u"周三", u"周四", u"周五", u"周六")
    days = []
    for i in xrange(0, 4):
        t = datetime.date.today() + datetime.timedelta(i)
        key = t.strftime('%Y-%m-%d')
        index = int(t.strftime('%w'))
        value = t.strftime('%Y-%m-%d') + d[index]
        if i == 0:
            value += u'（今天）'
        day = {"key": key, "value": value}
        days.append(day)
    return days


def get_weekname(dt):
    d = (u"周一", u"周二", u"周三", u"周四", u"周五", u"周六", u"周日")
    return d[dt.weekday()]


if __name__ == '__main__':
    result = get_weekname(datetime.date.today())
    print result
