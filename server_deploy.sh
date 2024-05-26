echo "Deploy Server"
git pull
source env/bin/activate
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

sudo supervisorctl restart sso_django

cd ..
cd frontend
npm i
npm run build
sudo service nginx restart
