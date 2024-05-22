server deploy

```

sudo cp setup/sso_django.conf  /etc/supervisor/conf.d/
sudo mkdir /var/log/gunicorn
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart sso_django
```
