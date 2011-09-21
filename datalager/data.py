#!/bin/env python
# -*- coding: utf-8 -*-

import csv
projektLista = []
teknikLista = []
errorKod = 1

def init():
    spamReader = csv.DictReader(open('data.csv'))

    for row in spamReader:
        tekReader = csv.reader([row['techniques_used']])
        
        row['techniques_helper'] = []

        for i in tekReader:
            for j in i:
                row['techniques_helper'].append(j)
                if not j in teknikLista:
                    teknikLista.append(j)
        
        projektLista.append(row)

    teknikLista.sort()

    global errorKod
    errorKod = 0
    #unikod - hur?

def project_count():
    return (errorKod, len(projektLista))

def lookup_project(id):
    for proj in projektLista:
        if proj['project_no'] == str(id):
            return (errorKod, proj)

    return (2, None)

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
    returlist = []
    for i in projektLista:
        add = False
        if search != None and search_fields != None:
            for s in search_fields:
                if i[s].lower().find(search.lower()) != -1:
                    add = True
                    break
        else:
            add = True

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
        temp = {"name": tek, "count": 0, "projects": []}
        for proj in projektLista:
            if tek in proj['techniques_used']:
                temp['count'] += 1
                temp['projects'].append({"id": proj['project_no'], "name": proj['project_name']})

        returlist.append(temp)
    return (errorKod, returlist)
