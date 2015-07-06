# Quickstart

## Installation

Install using `pip`, including any optional packages you want...

    pip install lisa-api

...or clone the project from github.

    git clone git@github.com:project-lisa/lisa-api.git

Create the MySQL user

    grant all privileges on lisa_api.* to 'lisa_api'@'localhost' identified by 'lisapassword';

Create a configuration file

    sudo mkdir -p /etc/lisa/conf/
    lisa-api-cli configuration save --filename /etc/lisa/conf/lisa_api.ini

You can of course edit these configuration parameters following your needs

Create your super-user

    lisa-api-cli createsuperuser

Then launch the lisa-api webserver
    
    lisa-api-cli runserver 0.0.0.0:8000

You can now access it in your browser by loging in before at [http://127.0.0.1:8000/api-auth/login/](http://127.0.0.1:8000/api-auth/login/)

    http://localhost:8000/docs/

