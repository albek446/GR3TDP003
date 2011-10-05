from pysqlite2 import dbapi2 as sqlite
from csv import DictReader
from re import escape

memoryConnection = None
cursor = None
databaseFields = None

errorcode = lambda: int(memoryConnection == None)

def createDict(keys, values):
	ret = {}
	if len(values) > len(keys):
		print "Value length exceeds keys, dropping values"

	for i in xrange(len(keys)):
		ret[keys[i]] = values[i]

	return ret

def readCSV(file):
	read = DictReader(file)
	sqlDict = {}
	test = []
	for a in read:
		test.append(a)

	for field in test[0].keys():
		if "no" in field or "size" in field:
			sqlDict[field] = "INTEGER"
			if "project_no" in field:
				sqlDict[field] += " PRIMARY KEY"
		else:
			sqlDict[field] = "VARCHAR("
			asdf = 0
			for value in test:
				if len(value[field]) > asdf:
					asdf = len(value[field])

			sqlDict[field] += str(asdf+1) + ")"
	return sqlDict, test, test[0].keys()

def init():
	global memoryConnection
	memoryConnection = sqlite.connect(':memory:')
	global cursor
	cursor = memoryConnection.cursor()

	global databaseFields
	fields, data, databaseFields = readCSV(open("data.csv"))

	sqlQuery = 'CREATE TABLE projects ('
	for k, v in fields.iteritems():
		sqlQuery += k + " " + v
		if fields.keys().index(k) < len(fields.keys())-1:
			sqlQuery += ", "
	sqlQuery += ')'
	
	cursor.execute(sqlQuery)
	sqlQuery = "CREATE TABLE techniques (project_no INTEGER, technique_name VARCHAR(6))"
	cursor.execute(sqlQuery)

	for proj in data:
		sqlQuery = ""

		for k, v in proj.iteritems():
			if "VARCHAR" in fields[k]:
				sqlQuery += "'"
			sqlQuery += v
			if "VARCHAR" in fields[k]:
				sqlQuery += "'"

			if proj.keys().index(k) < len(proj.keys())-1:
				sqlQuery += ", "

		cursor.execute('INSERT INTO projects VALUES('+sqlQuery+')')

	memoryConnection.commit()

def project_count():
	return (errorcode(), cursor.execute("SELECT count(*) FROM projects").fetchall()[0][0])

def lookup_project(id):
	return (errorcode(), createDict(databaseFields, cursor.execute("SELECT p.*, t.technique_name as techniques FROM projects AS p INNER JOIN techniques AS t WHERE t.project_no=p.project_no AND p.project_no=" + str(id)).fetchall()[0]))

def retrieve_projects(sort_by='start_date', sort_order='asc', techniques=None, search=None, search_fields=None):
	sqlQuery = "SELECT * FROM projects"

	if search and search_fields and len(search_fields) > 0:
		sqlQuery += "WHERE "

		for f in search_fields:
			sqlQuery += "`" + f + "` LIKE '" + search + "'"

			if search_fields.index(f) < len(search_fields) -1:
				sql_query += " OR "

	sqlQuery += " ORDER BY " + sort_by + " " + sort_order.upper()
	print sqlQuery

	retList = []
	for ret in cursor.execute(sqlQuery).fetchall():
		retList.append(createDict(databaseFields, ret))

	return (errorcode(), retList)

def retrieve_techniques():
	sqlQuery = "SELECT DISTINCT technique_namn FROM techniques ORDER BY technique_name"
	return (errorcode(), cursor.execute(sqlQuery).fetchall()[0])
