# Quickstart

## Docker - I just want to test !

It's really simple to test the API very quickly by using [docker][docker-website].

Install [docker][docker-website] on your host, then launch :
```bash
docker run  --publish=8001:8000 -d --name lisa-api seraf/lisa-api
```
Then, you can access `http://localhost:8001/api-auth/login/` (if docker is on your localhost)

The login and pass of this image is `admin`/`admin`.

You can find the docker repository [here][docker-repository]

## Ansible - I want to automatize the deployment

### Ansible

You may want to have a machine to **pilot** all the LISA components. And it's a good idea !

For that, we will use [Ansible][ansible-website]. A [role has been created][ansible-role] to install the required packages to your api host.

You have to install Ansible. It's up to you to install the package of your linux distribution or to install it with `pip`.

### Install Ansible Role

First, we will install the [lisa-api role][ansible-role] :
```bash
ansible-galaxy install Seraf.lisa-api
```

### What is in the stack ?

This role will deploy a stack on your server with :

* **Rabbitmq** : to have a messaging server used for communication between client and api
* **Python** : it will install the python package of your distribution
* **Virtualenv** : it will create a user/group named `alivelisa` and create a virtual environment in `/home/alivelisa`
* **Supervisord** : it is a daemon which ensure a process is always running. Instead of creating a service for LISA, supervisord will manage the process

The only component you may need to install is the `mysql-server`. I did the choice to not install it as you need to setup a root account and you may want specific credentials for the `lisa_api` user.

### Configure your Ansible

For this part, you should find most of the documentation on [Ansible website][ansible-website]. We will cover only the needed parts.

You need to tell to Ansible which host is a lisa-api.

For this, edit the file `/etc/ansible/hosts` :

```ini
[lisa-api]
192.168.1.85
```

Here, my host `192.168.1.85` is a lxc container.

If you have no ssh key, create one :

```bash
ssh-keygen -t rsa
```

You also need to copy your ssh key to the host to have a passwordless connection.
This command will ask you the password of the root account of the remote host :

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub root@192.168.1.85
```

Now, you should be able to connect on your host (here `192.168.1.85`) without any password :

```bash
ssh root@192.168.1.85
```

You can test that ansible is able to join your host :

```bash
ansible lisa-api -m ping
```

### Deploy the role on your server

Now, we need to tell to Ansible to apply the role `Seraf.lisa-api` on the group `lisa-api`.

Create the [playbook][lisa-api-playbook] file named `install-lisa-api.yml` :

```yaml
---
- hosts: lisa-api
  roles:
     - Seraf.lisa-api
```

That's all ! You should be able to run it with :

```bash
ansible-playbook install-lisa-api.yml
```

### Create the configuration file

The API will read by default the configuration files located in `/etc/lisa/conf/lisa_api.ini` and `/home/alivelisa/.virtualenvs/lisa-api/local/lib/python2.7/site-packages/lisa_api/lisa_api.ini`

An example of ini file to connect to a default database (used in docker container) :
```ini
[api]
debug = True

[database]
name = lisa_api
user = lisa_api
password = lisapassword
host = localhost
port = 3306

[rabbitmq]
user = guest
password = guest
host = localhost
```

The api will read the configuration file in two places. One on the system `/etc` and another in the userland `/home`. It will ensure user who aren't root to be able to modify easily their configuration.

### Create the MySQL database

As this part isn't covered by the ansible role, you need to install by yourself the mysql server and configure it.

You will need to create a database :

```sql
create database lisa_api;
```

And the user associated :

```sql
grant all privileges on lisa_api.* to 'lisa_api'@'localhost' identified by 'lisapassword';
```

### Start the API

You can connect with ssh on your host to start/stop/restart the api using `supervisorctl` :

```
root@lxc-lisa-api:~# supervisorctl 
lisa-api                         RUNNING    pid 1406, uptime 4:11:57
supervisor> stop lisa-api
lisa-api: stopped
supervisor> start lisa-api
lisa-api: started
```

Or you can use ansible to do this :

```bash
ansible lisa-api -m supervisorctl -a "name=lisa-api state=restarted"
```

## By Hand - Install for the brave and true

It's the best method to understand what you are doing and which components are required by the api.

Create a user named `alivelisa` and a group with the same name :

```bash
sudo groupadd alivelisa
sudo useradd -m -g alivelisa alivelisa
```

Install tools for virtual environment :
```
sudo pip install virtualenv virtualenvwrapper
```

Create the virtual environment :

```
su - alivelisa
cd /home/alivelisa
mkvirtualenv lisa-api
workon lisa-api
```


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

## Optionals

There is some optional packages you may need to install :

* If you want to use **picotts** : `libav-tools` `libttspico-data` `libttspico-utils` `libavcodec-extra-53`

[docker-website]: https://www.docker.com/
[docker-repository]: https://github.com/project-lisa/lisa-api-docker
[ansible-website]: http://www.ansible.com/home
[ansible-role]: https://github.com/project-lisa/lisa-api-deployment
[lisa-api-playbook]: https://github.com/project-lisa/lisa-api/ansible/install-lisa-api.yml