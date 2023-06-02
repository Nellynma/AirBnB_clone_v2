#!/usr/bin/env bash
# install nginx
sudo apt-get -y update
sudo apt-get -y install nginx

# replace the index.html file content 
echo "Hello World!" | sudo tee /var/www/html/index.html > /dev/null

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "Hello Nginx!" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# restart nginx
sudo service nginx restart
