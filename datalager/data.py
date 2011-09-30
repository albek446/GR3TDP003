#!/bin/env python
# -*- coding: utf-8 -*-

import csv
projektLista = []
teknikLista = []
errorkod = lambda: int(len(projektLista)==0)
unic = lambda val: unicode(val, 'utf-8')

def UnicodeDictReader(utf8_data):
    csv_reader = csv.DictReader(utf8_data)
    ret = []
    for row in csv_reader:
        temp = {}
        for key, value in row.iteritems():
            if value.isdigit() and key != 'project_name':
                try:
                    val = int(value)
                except ValueError:
                    val = float(value)

                temp[unic(key)] = val
            else:
                temp[unic(key)] = unic(value)

        ret.append(temp)

    return ret

def init():
    spamReader = UnicodeDictReader(open('data.csv'))

    for row in spamReader:
        tekReader = csv.reader([row[u'techniques_used']])
        
        row[u'techniques_used'] = []

        for i in tekReader:
            for j in i:
                row[u'techniques_used'].append(unic(j))
                if not j in teknikLista:
                    teknikLista.append(unic(j))
        
        row[u'techniques_used'].sort()
        projektLista.append(row)

    teknikLista.sort()

def project_count():
    return (errorkod(), len(projektLista))

def lookup_project(id):
    if errorkod():
        return (errorkod(), None)

    for proj in projektLista:
        if proj['project_no'] == id:
            return (errorkod(), proj)

    return (2, None)

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
    returlist = []

    for i in projektLista:
        add = False

        if search != None and search_fields != None:
            for s in search_fields:
                if isinstance(i[s], int) or isinstance(i[s], float):
                    sField = unic(str(i[s]))
                elif isinstance(i[s], list):
                    sField = u','.join(i[s])
                else:
                    sField = i[s]            

                if sField.lower().find(unic(search).lower()) != -1:
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
    return (errorkod(), teknikLista)

def retrieve_technique_stats():
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
