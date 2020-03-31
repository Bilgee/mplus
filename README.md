# mplus

## create apps directory

Application нь /opt/sites дотор ажиллахаар тохиргооны файлууд маань бичигдсэн байгаа тул /var/www доор apps folder-г үүсгэнэ.

Лог хийхэд зориулж /var/log/uwsgi director-г үүсгэнэ.

```
cd /opt/sites
git clone repo
```

## Creating virtualenv(python3.6) && install dependencies

lmdb data loader library-с шалтгаалан python3 дээр ажиллахаар болсон байгаа.

```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## config file location root/application/config/config.yml

AWS S3 key болон Redis, Log-н тохиргооны параметрүүд-г нэмж өгнө

## uwsgi+flask deployment sample

##### https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04

## nginx setting sample

```
server {
    listen 80;
    server_name localhost 127.0.0.1;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/opt/sites/mplus/server.sock;
    }
}
```

## wsgi.ini

```
[uwsgi]
pidfile = /tmp/mplus.pid
socket = 127.0.0.1:5001
chdir = /opt/sites/mplus
module = runserver

master = true
processes = 4

socket = server.sock
chmod-socket = 666
vacuum = true

die-on-term = true
```

## mplus.service.example

```
[Unit]
Description=uWSGI instance to serve mplus
After=network.target

[Service]
User=bilgee
Group=www-data
WorkingDirectory=/opt/sites/mplus
Environment="PATH=/opt/sites/mplus/venv/bin"
ExecStart=/opt/sites/mplus/venv/bin/uwsgi --ini wsgi.ini
ExecStop=/opt/sites/mplus/venv/bin/uwsgi --stop /tmp/mplus.pid
[Install]
WantedBy=multi-user.target
```

## setting lendmn_idreader service

Асааж унтраахыг хялбаршуулахын тулд system service болгон бүртгэх

```
sudo cp mplus.service.example /etc/systemd/system/mplus.service
```

service-г идэвхжүүлэх

```
sudo systemctl enable mplus
```

асаах

```
sudo systemctl start mplus
```

статус шалгах

```
sudo systemctl status mplus
```

унтраах

```
sudo systemctl stop mplus
```

## Testing API

mplus/application/test дотор байрлах testApi ажиллуулах.  
Шаардлагатай тохиолдолд IP хаяг болон Port-г солих.  
Ок гэж хэвлэгдэх эсэхийг шалгах.

```
cd mplus/application/test
python3 -m unittest testApi
```
