SQL_SELECT_ART="SELECT id,title,text,url,level FROM arts WHERE user_id='neveralso'"
SQL_SELECT_EDGE="SELECT to_art FROM edge WHERE from_art=%d"
SQL_INSERT_ART="INSERT INTO arts(user_id,title,text,url,level) VALUES ('neveralso','%s','%s','%s',%d)"
SQL_INSERT_EDGE="INSERT INTO edge(from_art,to_art) VALUES (%d,%d)"
SQL_DELETE_ART="DELETE FROM arts WHERE id=%d"
SQL_UPDATE_ART="UPDATE arts SET title='%s',text='%s',url='%s',level=%d WHERE id=%d"
SQL_HOST='localhost'
SQL_USER='root'
SQL_PASSWORD='root'
SQL_DB='pkm'
SQL_PORT=3306
RE_HEAD=r'(.*)('
RE_END=r')(.*)'
