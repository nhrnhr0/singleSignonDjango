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
