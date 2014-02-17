test
uwsgi_python -s :8000 -w main

background
uwsgi_python -i uwsgi.ini

stop
uwsgi_python --stop uwsgi.pid

sql 
insert into users value('neveralso','neveralso@gmail.com','123456');

sql


kuayu
Access-Control-Allow-Origin *
