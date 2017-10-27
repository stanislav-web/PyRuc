### PyRuc is the service for maintaining user accounts (UAC)
![Alt text](https://cdn-images-1.medium.com/max/1600/1*oIAgEukzbEs2qMJ1LPdApg.png "PyRuc")

##### What do you get out of the box?
- Registration and maintenance in mode of persistent storage use
- Granting access to your internal services
- Rapid recovery access in case of loss of control

##### Requirements
- Python >= 3.5
- Redis >= 4
- Gunicorn + Gevent Async server

##### API
[http://drunk-start.surge.sh](http://drunk-start.surge.sh)

##### Installation
- Docker (under development)
```python
docker-compose up --build
```
- PIP
```python
pip install -r requirements.txt
```

#### RUN
gunicorn -c server_config.py server

**Use postman.json for review**