# problem definition

Develop two separate programs that will:

### 1st Program:
Process CSV files and send each row/data to a message queue*. An example CSV file is attached. 

### 2nd Program:
Consume the messages that are sent by the 1st program and insert them into a database table**. There can only be one record with the same email address. Imagine this program will be running on multiple servers or even on the same server with multiple processes at the same time.

* Can be any production-ready distributed system such as redis, rabbitmq, sqs, or even kafka.

** Can be any modern relational database but the solution is better to be independent of the database server.

Tips And Tricks:

- Pay attention to the details in the description.
- Develop the programs as you are developing it for a production system in a real-life scenario.
- Any programming language can be used.

# Q&A
### Q1
* are there any constraints/or/preferences about the first program? like:
    * how it interacts with the user and gets input?
    * is it a CLI program or web service?
    * should it have concurrent instances?
### A1
There are no constraints about it , you can choose what to do but the second program which consumes the messages can run multiple instances so can do the work in parallel. 
### Q2
* about the second program:
    * what is the desired behavior in case of collision?
    * what is the desired behavior in case of invalid emails (bad data)?
### A2
If the email exists it should keep the existing data and skip the new one. If an email is invalid it means it is not an email. In the real world what would you do, assume this csv file is coming from an 3rd party company.
### Q3
for the second program, can I use task queues like Celery or python-rq or the task requires to listen directly to the message queue (redis for example) and handle issues like: connection management, error handling, connection recovery, concurrency and metric collection
### A3
You are totally free.

---
# solution

## operations
### install and run
in project root
```bash
cp example.env .env
docker-compose build
docker-compose up
```
### api usage
```bash
curl -X POST \
  http://127.0.0.1:5000/api/upload/ \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F 'file=@/path/to/your/data.csv'
```
you can see the queued tasks from rq_dashboard on:
`http://localhost:5000/dashboard/`

also you see sqlalchemy logs in the console

### accessing the database
while ``docker-compose up`` is running, in another terminal type:
```bash
docker-compose run database psql -hdatabase -Uusr csv
```

### flask shell
```bash
docker-compose run client flask shell-plus
```

### running tests
for convenience tests runs once while launching the app, but you can run it using
```bash
docker-compose run test
```

## design
### the message queue
depends on redis official docker image
###### important configuration
RDB snapshots
```
save 900 1
save 300 10
save 60 10000
``` 
AOF
```
appendonly yes
appendfsync always
```
password is being set to the value in `.env` during the launch of the application using `sed`
```
requirepass {REDIS_PASSWORD}
```
hostname
```
bind redis
```
###### redis container limitations
overcommit_memory is set to zero
(this is more related to OS kernel and we may not deploy redis as container in production)
[issue #19](https://github.com/docker-library/redis/issues/19), [workaround](https://github.com/bkuhl/redis-overcommit-on-host)

### redis_rq
utilizing redis as a task queue and does:
* connection management,
* error handling,
* connection recovery,
* manage concurrency
* manage metric collection
* failing tasks go through dedicated queue 

### the first program
a flask app that accepts csv files in an api call, push the file into redis_rq, and responds to user synchronously 

### the second program
redis_rq worker with 3 instances

### database
the application is database independent, it uses SQLAlchemy as an ORM to isolate our code from DBMS
we also use alembic for migrations
I have chosen Postgres as I am convenient with, but the app is not using any (postgres specific feature)

## app structure
`app/app/apis.py`
contains flask views

`app/app/config.py`
contains app configurations it depends on [flask_env](https://github.com/brettlangdon/flask-env) to load values from environment variables

`app/app/jobs.py`
redis_rq jobs that is being pushed to the queue

`app/app/routes.py`
url, view mapping

`app/app/schema.py`
the database tables definition

`app/manage.py`
cli commands to manage the app

## TODO
* enhance tests (create a new database for testing with each test case separated from production database)
* increase coverage
* use fakeredis for testing
* fix docker volume mapping permissions to allow containers to write files on host
* build an api to get results and status of processed file
* write backup and restore scripts for redis
* validate email domain has SMTP Server and verify email exists
* write documentation