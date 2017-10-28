### PyRuc is the service for maintaining user accounts (UAC)
[![Coverage Status](https://coveralls.io/repos/github/stanislav-web/PyRuc/badge.svg?branch=master)](https://coveralls.io/github/stanislav-web/PyRuc?branch=master) [![Code Health](https://landscape.io/github/stanislav-web/PyRuc/master/landscape.svg?style=flat)](https://landscape.io/github/stanislav-web/PyRuc/master) [![GitHub license](https://img.shields.io/github/license/stanislav-web/PyRuc.svg)](https://github.com/stanislav-web/PyRuc/blob/master/LICENSE)

|  Python | Status |
|:-:|:-:|
|3.5|[![Build Status](https://travis-ci.org/stanislav-web/PyRuc.svg?branch=master)](https://travis-ci.org/stanislav-web/PyRuc) |
|3.6|[![Build Status](https://travis-ci.org/stanislav-web/PyRuc.svg?branch=master)](https://travis-ci.org/stanislav-web/PyRuc) |

##### What do you get out of the box?
- Registration and maintenance in mode of persistent storage use
- Granting access to your internal services
- Rapid recovery access in case of loss of control

##### Requirements
- Python >= 3.5
- Redis >= 4

##### Installation
- Docker (under development)
```bash
docker-compose up --build
```
- Pip dependencies
```bash
pip install -r requirements.txt
```
##### Try API
[http://drunk-start.surge.sh](http://drunk-start.surge.sh)

#### Run
```bash
gunicorn -c config.py server
```

#### Tests
```bash
cd app && coverage run setup.py test
```

![restfull](images/restfull.png)

![Python3](images/python3.png) ![Flask](images/flask.png) ![Redis](images/redis.png) ![JWT](images/jwt.png) ![Twillio](images/twilio.png)