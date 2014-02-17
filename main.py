#encoding=UTF-8
import web
import settings
import MySQLdb
import re
from urllib import unquote
import json
import uuid

RENDER = web.template.render('templates/')


class index:
    def GET(self):
        return RENDER.form()

    def POST(self,name):
        return 0


class search:
    def GET(self, name):
        query = unquote(web.ctx.env['QUERY_STRING'])
        query = query[8:]
        print query
        retext = settings.RE_HEAD
        for i in query.split('+'):
            retext += i + '|'
        retext = retext[:len(retext) - 1]
        retext += settings.RE_END
        print retext
        regular = re.compile(retext)
        result = sql_select(settings.SQL_SELECT_ART)
        node = []
        print result
        for i in result:
            print i[0]
            if (regular.match(i[1])) or (regular.match(i[2])):
                node.append(list(i))
        print node
        for i in range(len(node)):
            for j in range(len(node[i])):
                if type(node[i][j]) == type(1L):
                    continue
                node[i][j] = node[i][j].decode(encoding='utf-8').encode(encoding='utf-8')

        edge = []
        for i in node:
            result = sql_select(settings.SQL_SELECT_EDGE % i[0])
            print result
            for j in result:
                edge.append([i[0], j[0]])
        if len(node) != 0:
            return json.dumps([node, edge])
        else:
            return 0

    def POST(self, name):
        return 0


class insert:
    def GET(self, name):
        return 0

    def POST(self, name):
        query = unquote(web.data()).split('&')
        print query
        query_dict = {}
        #return 'hello'+str(environ)
        for i in query[:len(query) - 1]:
            query_dict[i.split('=')[0]] = (i.split('=')[1]).decode(encoding='utf-8').encode(encoding='utf8')
        query_dict['level'] = int(query[len(query) - 1].split('=')[1])
        sqltext = settings.SQL_INSERT_ART % (
        query_dict['title'], query_dict['text'], query_dict['url'], query_dict['level'])
        print  sqltext
        return sql_excu(sqltext)


class delete:
    def GET(self, name):
        query = web.ctx.env['QUERY_STRING']
        query = query[6:]
        query = int(query)
        return sql_excu(settings.SQL_DELETE_ART % query)

    def POST(self, name):
        return 0

class connect:
    def GET(self, name):
        query = web.ctx.env['QUERY_STRING']
        query = query[6:]
        query = query.split('+')
        query[0] = int(query[0])
        query[1] = int(query[1])
        print query
        return sql_excu(settings.SQL_INSERT_EDGE % (query[0], query[1]))

    def POST(self,name):
        return 0


class update:
    def GET(self, name):
        return 0

    def POST(self, name):
        query = unquote(web.data()).split('&')
        print query
        query_dict = {}
        #return 'hello'+str(environ)
        for i in query[1:len(query) - 1]:
            query_dict[i.split('=')[0]] = (i.split('=')[1]).decode(encoding='utf-8').encode(encoding='utf8')
        query_dict['id'] = int(query[0].split('=')[1])
        query_dict['level'] = int(query[len(query) - 1].split('=')[1])
        sqltext = settings.SQL_UPDATE_ART % (
        query_dict['title'], query_dict['text'], query_dict['url'], query_dict['level'], query_dict['id'])
        print  sqltext
        return sql_excu(sqltext)


class sendfile:
    def GET(self,name):
        return False
    def POST(self, name):
        x = web.input(upfile={})
        #web.debug(x['upfile'].filename) # This is the filename
        #web.debug(x['upfile'].value) # This is the file contents
        text = x['upfile'].file.read() # Or use a file(-like) object
        if len(text) == 0:
            return False
        text = json.loads(text)
        print text
        id_max = sql_select('SELECT MAX(id) FROM arts')[0][0]
        print id_max
        change_map = {}
        id_max += 1
        for j in text[0]:
            l = []
            for k in j:
                if type(k) == type(1):
                    l.append(k)
                else:
                    l.append(k.encode('utf-8'))#.decode(encoding='utf-8'))
            change_map[l[0]]=id_max
            id_max+=1
            query = settings.SQL_INSERT_ART % (l[1], l[2], l[3], l[4])
            print query
            sql_excu(query)
        for i in text[1]:
            query = settings.SQL_INSERT_EDGE % (change_map[i[0]], change_map[i[1]])
            print query
            sql_excu(query)

        return text

class getfile():
    def GET(self,name):
        env=web.ctx.env
        result = sql_select(settings.SQL_SELECT_ART)
        node = []
        #print result
        for i in result:
            node.append(list(i))
        #print node
        for i in range(len(node)):
            for j in range(len(node[i])):
                if type(node[i][j]) == type(1L):
                    continue
                node[i][j] = node[i][j].decode(encoding='utf-8').encode(encoding='utf-8')

        edge = []
        for i in node:
            result = sql_select(settings.SQL_SELECT_EDGE % i[0])
            #print result
            for j in result:
                edge.append([i[0], j[0]])
        ustr=str(uuid.uuid1())
        file=open('tempfile/'+ustr+'.json','w')
        tempurl="<a href='http://"+env['SERVER_NAME']+":"+str(8004)+'/tempfile/'+ustr+".json'>Download</a>"
        if len(node) != 0:
            file.write(json.dumps([node, edge]))
        else:
            print 0
        file.close()
        return tempurl
    def POST(self,name):
        return False

def sql_excu(query_string):
    try:
        print query_string
        conn = MySQLdb.connect(host=settings.SQL_HOST, user='root', passwd='root', db='pkm', port=3306)
        cur = conn.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute(query_string)
        cur.close()
        conn.close()
        return True
    except Exception, e:
        #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return False


def sql_select(query_string):
    try:
        conn = MySQLdb.connect(host=settings.SQL_HOST, user=settings.SQL_USER, passwd=settings.SQL_PASSWORD,
                               db=settings.SQL_DB)
        cur = conn.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute(query_string)
        text = cur.fetchall()
        cur.close()
        conn.close()
        return text
    except Exception, e:
        #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return None


urls = (
    '/api[/]{0,1}', 'index',
    '/api/search[/]{0,1}(.*)', 'search',
    '/api/insert[/]{0,1}(.*)', 'insert',
    '/api/update[/]{0,1}(.*)', 'update',
    '/api/delete[/]{0,1}(.*)', 'delete',
    '/api/connect[/]{0,1}(.*)', 'connect',
    '/api/sendfile[/]{0,1}(.*)', 'sendfile',
    '/api/getfile[/]{0,1}(.*)', 'getfile'
)

app = web.application(urls, globals())

#for uwsgi -i uwsgi.ini
#or uwsgi -s :8000 -w main
application=app.wsgifunc()

#for test 127.0.0.1:8000
#if __name__ == '__main__':
#    app.run()