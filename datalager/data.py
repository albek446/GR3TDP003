#!/bin/env python
# -*- coding: utf-8 -*-

import csv
projektLista = []
teknikLista = []
errorKod = 1

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

                temp[unicode(key, 'utf-8')] = val
            else:
                temp[unicode(key, 'utf-8')] = unicode(value, 'utf-8')

        ret.append(temp)

    return ret

def init():
    spamReader = UnicodeDictReader(open('data.csv'))

    for row in spamReader:
        tekReader = csv.reader([row[u'techniques_used']])
        
        row[u'techniques_used'] = []

        for i in tekReader:
            for j in i:
                row[u'techniques_used'].append(unicode(j, 'utf-8'))
                if not j in teknikLista:
                    teknikLista.append(unicode(j, 'utf-8'))
        
        row[u'techniques_used'].sort()
        projektLista.append(row)

    teknikLista.sort()

    global errorKod
    errorKod = 0

def project_count():
    return (errorKod, len(projektLista))

def lookup_project(id):
    for proj in projektLista:
        if proj['project_no'] == id:
            return (errorKod, proj)

    return (2, None)

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
    returlist = []
    for i in projektLista:
        add = False
        if search != None and search_fields != None:
            for s in search_fields:
                if isinstance(i[s], int) or isinstance(i[s], float):
                    sField = unicode(str(i[s]), 'utf-8')
                elif isinstance(i[s], list):
                    sField = u','.join(i[s])
                else:
                    sField = i[s]            

                if sField.lower().find(unicode(search, 'utf-8').lower()) != -1:
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

    return (errorKod, returlist)

def retrieve_techniques():
    return (errorKod, teknikLista)

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
    return (errorKod, returlist)
