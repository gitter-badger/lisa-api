<p class="badges" height=20px>
    <iframe src="http://ghbtns.com/github-btn.html?user=project-lisa&amp;repo=lisa-api&amp;type=watch&amp;count=true" class="github-star-button" allowtransparency="true" frameborder="0" scrolling="0" width="110px" height="20px"></iframe>

    <a href="http://travis-ci.org/tomchristie/django-rest-framework?branch=master">
        <img src="https://secure.travis-ci.org/project-lisa/lisa-api.svg?branch=master" class="status-badge">
    </a>

    <a href="https://pypi.python.org/pypi/lisa-api">
        <img src="https://img.shields.io/pypi/v/lisa-api.svg" class="status-badge">
    </a>
</p>

---

LISA Api is a core component of LISA. It's based on Django Rest Framework that makes it easy to build Web APIs for almost everything.

The API was made to provide an easy bridge between custom home automation devices which are not zwave or having a common protocol.
If your device can be reach and used by python, so you can expose a http endpoint and it will be useable by your home automation box.

Some key features :

* Highly customizable, you can easily override native functions using your plugins
* Plugins are easy to write, and can be auto-generated
* Plugins can provide a generic interface to let other plugins plug on them
* Plugins dependancies
* Auto-generated documentation

---

## Requirements

LISA API requires the following:

* Python (2.7, 3.4)
* Django (1.8)
* Django Rest Framework
* PIP
* Django Rest Swagger
* Stevedore
* Colorlog
* Kombu
* Requests

## Quickstart

Can't wait to get started? The [quickstart guide][quickstart] is the fastest way to get up and running, and creating plugins.

## Tutorial

The tutorial will walk you through the building blocks that make up REST framework.   It'll take a little while to get through, but it'll give you a comprehensive understanding of how everything fits together, and is highly recommended reading.

* [1 - Plugins][tut-1]

## Development

See the [Contribution guidelines][contributing] for information on how to clone
the repository, run the test suite and contribute changes back to LISA API.

## Support

For support please see the [ask website][ask], try the channel on [gitter][gitter]


## License

Copyright (c) 2015, Julien Syx
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


[index]: .
[quickstart]: tutorial/quickstart.md
[contributing]: topics/contributing.md
[release-notes]: topics/release-notes.md

[tox]: http://testrun.org/tox/latest/
[gitter]: https://gitter.im/project-lisa/lisa
[ask]: http://ask.lisa-project.net
[markdown]: http://pypi.python.org/pypi/Markdown/

[tut-1]: tutorial/1-plugins.md
