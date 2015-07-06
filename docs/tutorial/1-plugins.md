# Plugins

## How it work
As the API is done with [Django][django-website], you will need to understand [Django][django-website] to create the plugins.

Plugins are created with [Django Rest Framework][django-restframework] (you should read the docs too).

Each plugin is a [Django Application][django-app] which is dynamically loaded by django using the entry points.

An entry point is a Python object in a project’s code that is identified by a string in the project’s `setup.py` file. The entry point is referenced by a group and a name so that the object may be discoverable. This means that another application can search for all the installed software that has an entry point with a particular group name, and then access the Python object associated with that name.

This is extremely useful because it means it is possible to write plugins for an appropriately-designed application that can be loaded at run time.

It is important to understand that entry points are a feature of the new Python eggs package format and are not a standard feature of Python.

The entry point in our plugin look like :

    entry_points={
        'lisa.api.plugins': [
            'shopping = lisa_plugins_shopping:ShoppingPlugin',
        ]
    },

We register the plugin `shopping` in the namespace `lisa.api.plugins` and it is mapped to the class `ShoppingPlugin` in our package (defined in the `__init__.py` file).

The `INSTALLED_APP` list of Django is populated by the plugin manager which will look for all plugin available in the namespace `lisa.api.plugins` and will import all their urls and models.

Django as other framework don't support to add or delete routes at runtime. So the plugins are loaded when the api server is launched.
When a new plugin is installed or removed, the server needs to be restarted.

## Structure

A plugin is mainly a Django Application with some added features. By default, it has this structure :

* `tests` : it's the directory containing all your unit tests to be sure your plugin will work even if you modify it, or if it works with the new LISA API versions
* `requirements/requirements-plugin.txt` : this file contains the libraries required for your plugin (note that it differs from pip dependancies (check the setup.py file)
* `setup.py` : this file manage how you're plugin will be installed. You configure your name, and few metadata that will appears on pypi. You will have to edit this file to add entry_points or to add required libraries
* `lisa_plugins_shopping/__init__.py` : contains metadata about your plugin and the intents mapped to your API.
* `lisa_plugins_shopping/models.py` : contains the model of your object (optional). This model will be the table in the database you could use
* `lisa_plugins_shopping/serializers.py` : contains classes to explain to django how to serialize the data received on the API
* `lisa_plugins_shopping/urls.py` : contains url and the view attached
* `lisa_plugins_shopping/views.py` : the most important part of your plugin. It contains all the logic and how the data received should be used
* `lisa_plugins_shopping/migrations` : this directory contains all the evolutions of your model. his directory is automatically managed by django and will provide a very easy system to distribute new version of your plugin

## Create your first plugin

Place yourself in the directory where you have permissions to create a directory and would like to work. For this tutorial we will use `Sandbox`

    cd Sandbox

Now use the `lisa-api-cli` to create the plugin from the template

    lisa-api-cli plugins --create

Now, answer to the questions. For example, to create the shopping plugin :

    full_name (default is "Your full name here")? Julien Syx
    email (default is "you@example.com")? julien@lisa-project.net
    github_username (default is "yourname")? Seraf
    app_name (default is "package")? shopping
    project_short_description (default is "Your project description goes here")? This plugin manage a shopping list
    year (default is "2015")? 
    version (default is "0.1.0")? 
    Successfully created the plugin


## Load the plugin

The next step is to have your plugin loaded in the API (even if it do nothing).

First, we will create a git repository to track the changes and share the sources to everyone.
Create a git repository on github, bitbucket, whatever you prefer, then initialize the repository :

    git init

And follow the instructions given by github to map this repository to the one you created :

    git remote add origin git@github.com:Seraf/lisa-plugins-shopping.git
    git add *
    git commit . -m 'Initial commit'
    git push -u origin master


The plugin will be packaged in the future but for development purpose, you will have to tell python where to load your package :

    cd Sandbox/lisa-plugins-shopping
    python setup.py sdist build
    export PYTHONPATH=~/Sandbox/lisa-plugins-shopping:$PYTHONPATH

I suggest to set this line in your rc file (depending your shell). Commonly it's `~/.bashrc` or `.zshrc`

You should see your package loaded by doing a `pip freeze | grep lisa-plugins`

    -e git+https://github.com/project-lisa/lisa-plugins-shopping.git@bdfdd3a868926ed960f7be3ca27e77a03b88d920#egg=lisa_plugins_shopping-origin/develop

## Customize the plugin
First, you need to understand the concept of [views][django-views] and [models][django-models] of Django.

### Add a dependancie

For the shopping plugin, we want to have multiple lists. A list has a `name` and contains some products/items.
As items can be anything, it doesn't make sense to create a product model and play with foreign key to map a product on a list.
Instead, I will use a jsonfield and create the list in a json. Later it will be easy to store a quantity of product directly in the json.

To add this jsonfield, we will need to use [django-jsonfield][django-jsonfield].

When you add a dependancie, you must know if this one is necessary for the plugin to work.
If it is needed, add it as a dependancie of your plugin, else you can include it in the `requirements-optional.txt` file

You will need to update these files :

* `requirements/requirements-plugin.txt`
* `setup.py`

The setup file has already a dependancie to `lisa-api`. It seems logic, the plugin need the app where it will be run.
With this system you can also ask for a minimum version of the package.
For example you want to use a new class added in the version '1.3' of `lisa-api`, you can write `lisa-api>=1.3` in the `setup.py` requirements.

When a user will download your plugin, it will ensure the user has the version 1.3 minimum or it will upgrade it to the latest version available.

### Create a model

Above, we said that our list model will have a `name` attribute and a `list` jsonfield :

In the `lisa_plugins_shopping/models.py`

```python
from django.db import models
from jsonfield import JSONField


class ShoppingList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    list = JSONField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.lower()
        super(ShoppingList, self).save(force_insert, force_update)

```

The function `save` is here to override the default `save` function of a model. Here, we want to have name always in lowercase.

### Create a serializer

> Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types.
> Serializers also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the incoming data.
> -- <cite>Django Rest Framework</cite>


You will find more informations on the [serializers][drf-serializers] page of Django Rest Framework.

In our file `lisa_plugins_shopping/serializers.py` :
```python
from lisa_plugins_shopping.models import ShoppingList
from rest_framework import serializers


class ShoppingListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('url', 'name', 'list')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }
```

The `extra_kwargs` parameter allow us to build beautiful url replacing the id by the name of the list.

### Create the view
> A view is a callable which takes a request and returns a response.
> This can be more than just a function, and Django provides an example of some classes which can be used as views.
> These allow you to structure your views and reuse code by harnessing inheritance and mixins.
> -- <cite>Django</cite>

The view will contains all the logic to apply. It receive a request, apply some operations and return a response.

As we have a simple model, we don't want to write all the create/read/update/delete views, so we use Django Rest Framework which automate all these things using a [viewset][drf-viewset].

In our file `lisa_plugins_shopping/views.py` :

```python
from lisa_plugins_shopping.models import ShoppingList
from lisa_plugins_shopping.serializers import ShoppingListSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to add/edit/delete shopping lists.
    """
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    lookup_field = 'name'
```

The viewset will handle *auto-magically* the views for your object.

### Create the url

The view is created, now you need to tell django how to redirect the request to the correct view.

In the file `lisa_plugins_shopping/urls.py` :

```python
from lisa_plugins_shopping.views import ShoppingListViewSet
from rest_framework import routers
from django.conf.urls import include, url

router = routers.DefaultRouter()
router.register(r'lists', ShoppingListViewSet)

urlpatterns = [
    url(r'^/', include(router.urls)),
]
```

We bind the url `/lists` to the view we created above.

### Apply your model to SQL

You now have you model, but you need to create the tables in your database.
Don't worry, Django will manage them for you. In the last release, it come with a native tool to handle the schema management.

Each time you will do a modification on your models, you will need to create a migration file :
```
lisa-api-cli makemigrations
```

It will create in each app loaded, the migration files under the directory `migrations`.

Now, to apply these migrations :

```
lisa-api-cli migrate
```


### Access the url

Now, you can run the lisa-api server :

```
lisa-api-cli runserver 0.0.0.0:8000
```

Then, go on [http://localhost:8000/docs/][lisa-api-swagger] (be sure to be [logged][lisa-api-login] before)

You should see your plugin and the methods available.

The LISA API will automatically provide an url like this : http://server/api/v1/plugin-**plugin-name**/

For example, to create a list :

```bash
curl -X POST -H "Content-Type: application/json" http://localhost:8000/api/v1/plugin-shopping/lists/ --data '{"name": "test-list", "items": []}'
```

### How to add a custom route

If creating a model and his views is very easy, you may need to create custom views.

For example, we want to add a route to add or delete some products on our list.

Create the serializer :

```python
class ItemSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.CharField())
```

We want to receive a list of string like ['tomatoes', 'cucumbers', 'potatoes']

Now, let's create the view (adding the item_add to existing view) :

```python
from lisa_plugins_shopping.models import ShoppingList
from rest_framework import viewsets, status
from rest_framework.response import Response
from lisa_plugins_shopping.serializers import ShoppingListSerializer, ItemSerializer
from rest_framework.decorators import detail_route
from lisa_api.lisa.logger import logger
from django.utils.translation import ugettext as _


class ShoppingListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to add/edit/delete shopping lists.
    """
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    lookup_field = 'name'

    @detail_route(methods=['POST'], serializer_class=ItemSerializer)
    def item_add(self, request, name=None):
        """
        This function manage the jsonfield of a shopping list by adding a product
        :param request:
        :param name:
        :return:

        Example (if the shopping list name is 'default'):
        curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/v1/plugin-shopping/lists/default/item_add/ --data '{"items": ["carotte", "chocolat"]}
        ---
        request_serializer: ItemSerializer
        response_serializer: ItemSerializer
        """
        list = self.get_object()
        json_list = list.list

        if not json_list.get('items'):
            json_list = {'items': []}

        if request.method == 'POST':
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                logger.debug(serializer.data['items'])
                for item in serializer.data['items']:
                    if item not in json_list['items']:
                        json_list['items'].append(item)
                        logger.debug('Adding item {item} to the list'.format(item=item))
                    else:
                        logger.debug('Item {item} already exist'.format(item=item))
                list.list = json_list
                list.save()
                return Response(_('Item {items} has been added to the list').format(
                    items=', '.join(serializer.data['items'])), status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

We declare a custom route named `item_add` and it will be available on `/api/v1/plugin-shopping/lists/{list_name}/item_add/`.

It's a good practice to add some documentation about your routes, what they done, how to call them etc.

You can test to add a function to retrieve the list items, and to delete items.

The complete sources are [available on github][github-shopping-plugin].

### Add an intent

The first goal of LISA is to provide an API to connect everything. With the steps above we have enough knowledge to create all plugins we want.

But as you may know the second goal of LISA is to let a human interact direcly with this API, by voice or text.

It means we need to convert a sentence into a HTTP request. It's difficult to know from a sentence to another which field to fill or not.

For that, in the `__init__.py` file of your plugin, you will have a function named `add_intents`

When the server start, it will load each plugin and execute this function.
This function add in a table the name of the intent and the url to call.

Let's start adding an intent :

```python
obj, created = Intent.objects.update_or_create(
    name='shopping_item_add',
    defaults={
        'method': 'POST',
        'api_url': '/api/v1/plugin-shopping/lists/{list_name}/item_add/'
    }
)
logger.debug("Adding {intent_name} intent for shopping plugin".format(intent_name=obj.name))

```

It will add an intent named `shopping_item_add` if it didn't already exist or update this one.

This intent use the **POST** http verb on the url `/api/v1/plugin-shopping/lists/{list_name}/item_add/`

The `{}` allow to specify dynamic fields of the url. If the sentence is *"add some potatoes on the list wallmart"*, it will replace `{listname}` by `wallmart`

The client will process the sentence with a NLP application and will ask the intent metadata to LISA API.

LISA API will answer with these info, so the client will know the url of your function. One thing it doesn't know yet is how to deal with the arguments.

It will query the url (your view) with **OPTIONS** verb. It will answer with arguments available :

```bash
curl -X OPTIONS -H "Content-Type: application/json" http://127.0.0.1:8000/api/v1/plugin-shopping/lists/wallmart/item_add
```

```json
{  
   "name":"Shopping List",
   "description":"API endpoint that allows users to add/edit/delete shopping lists.",
   "renders":[  
      "application/json",
      "text/html"
   ],
   "parses":[  
      "application/json",
      "application/x-www-form-urlencoded",
      "multipart/form-data"
   ],
   "actions":{  
      "POST":{  
         "items":{  
            "type":"list",
            "required":true,
            "read_only":false,
            "label":"Items",
            "child":{  
               "type":"string",
               "required":true,
               "read_only":false
            }
         }
      }
   }
}
```

And now, the client will map the field items of your sentence to the items argument.
As the view need a *POST* query, the client will do a *POST* on the url it already knows, with the args filled.

## Publish it

To publish your plugin, you need to be sure to have a [pypi][pypi] account and [register][pypi-register] your plugin, then :

    cd Sandbox/lisa-plugins-shopping
    python setup.py publish

The command `publish` has been added in your `setup.py` file 

## Write more complex plugins

You can do whatever you want. You only need to follow the structure of the plugin, but the content of the views is up to you.

As plugins are based on the [Django Rest Framework][django-restframework], you should read their documentation to know how to achieve your goal.

[django-website]: https://www.djangoproject.com/
[django-restframework]: http://www.django-rest-framework.org/
[django-app]: https://docs.djangoproject.com/en/1.8/ref/applications/
[pypi]: https://pypi.python.org/pypi
[pypi-register]: https://docs.python.org/2/distutils/packageindex.html
[django-views]: https://docs.djangoproject.com/en/1.8/topics/http/views/
[django-models]: https://docs.djangoproject.com/en/1.8/topics/db/models/
[django-jsonfield]: https://github.com/bradjasper/django-jsonfield
[drf-serializers]: http://www.django-rest-framework.org/api-guide/serializers/
[drf-viewset]: http://www.django-rest-framework.org/api-guide/viewsets/
[lisa-api-swagger]: http://localhost:8000/docs/
[lisa-api-login]: http://localhost:8000/api-auth/login/
[github-plugin-shopping]: https://github.com/project-lisa/lisa-plugins-shopping/tree/master/lisa_plugins_shopping
