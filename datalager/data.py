#!/bin/env python
# -*- coding: utf-8 -*-

import csv
projektLista = None
teknikLista = []
errorkod = lambda: int(projektLista == None)
unic = lambda val: unicode(val, 'utf-8')

def UnicodeDictReader(utf8_data):
    csv_reader = csv.DictReader(utf8_data)
    ret = []
    for row in csv_reader:
        temp = {}
        for key, value in row.iteritems():
            if value.isdigit() and "no" in key.lower():
                temp[unic(key)] = int(value)
            else:
                temp[unic(key)] = unic(value)

        ret.append(temp)

    return ret

def init():
    spamReader = UnicodeDictReader(open('data.csv'))
    tempLista = []

    for row in spamReader:
        tekReader = csv.reader([row[u'techniques_used']])
        
        row[u'techniques_used'] = []

        for i in tekReader:
            for j in i:
                row[u'techniques_used'].append(unic(j))
                if not j in teknikLista:
                    teknikLista.append(unic(j))
        
        row[u'techniques_used'].sort()
        tempLista.append(row)

    teknikLista.sort()

    global projektLista
    projektLista = tempLista

def project_count():
    if errorkod():
        return (errorkod(), None)

    return (errorkod(), len(projektLista))

def lookup_project(id):
    if errorkod():
        return (errorkod(), None)

    for proj in projektLista:
        if proj['project_no'] == id:
            return (errorkod(), proj)

    return (2, None)

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
    if errorkod():
        return (errorkod(), None)

    returlist = []
    for i in projektLista:
        add = False
        if search != None and search_fields != None:
            for s in search_fields:
                if isinstance(i[s], int):
                    sField = unic(str(i[s]))
                elif isinstance(i[s], list):
                    sField = u','.join(i[s])
                else:
                    sField = i[s]            

                if unic(search).lower() in sField.lower():
                    add = True
                    break
        else:
            add = True

        if add and techniques:
            for t in techniques:
                if not t in i['techniques_used']:
                    add = False

        if add:
            returlist.append(i)

    returlist.sort(key=lambda val: val[sort_by])

    if sort_order == 'desc':
        returlist.reverse()

    return (errorkod(), returlist)

def retrieve_techniques():
    if errorkod():
        return (errorkod(), None)

    return (errorkod(), teknikLista)

def retrieve_technique_stats():
    if errorkod():
        return (errorkod(), None)

    returlist = []

    for tek in teknikLista:
        temp = {u"name": tek, u"count": 0, u"projects": []}
        for proj in projektLista:
            if tek in proj[u'techniques_used']:
                temp[u'count'] += 1
                temp[u'projects'].append({u"id": proj[u'project_no'], u"name": proj[u'project_name']})
                
        temp[u'projects'].sort(key=lambda p: p[u'name'])
        returlist.append(temp)
    return (errorkod(), returlist)
