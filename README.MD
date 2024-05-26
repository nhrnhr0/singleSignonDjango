server deploy

```

sudo cp setup/sso_django_supervisor.conf /etc/supervisor/conf.d/
sudo mkdir /var/log/gunicorn
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart sso_django
```


```
sudo cp setup/sso_django_nginx.conf /etc/nginx/sites-available/sso_django_nginx.conf
sudo ln -s /etc/nginx/sites-available/sso_django_nginx.conf /etc/nginx/sites-enabled/
```

```
python3 -m venv env
source env/bin/activate
pip install -r backend/requirements.txt
```
