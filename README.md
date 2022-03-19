# FastAPI/Celery async API for annealing model

Some remarks:

- Celery was chosen to employ this API for asynchronous heavy batch background computations like optimizing ~1000 points.
For more lightweight computations we could use FastAPI background tasks which run in different thread but in the same event loop.
- We receive more reliability/scalability with Celery at expense of the speed, because Python objects cannot be shared between Celery workers, so we need to instantiate ML model for every worker

## How to run

1) Update values for MAX_ITERATIONS and CELERY_RESULT_TTL (time for which computed value is kept cached in Redis backend) if needed
2) Spin up the containers:
    ```sh
    $ docker-compose up --build
    ```
3) Go to http://0.0.0.0:8080/docs. Send example input to POST-handler
    ```json
    {"coordinates": [{"longitude": 55.849554, "latitude": 37.661426}, {"longitude": 55.771697, "latitude": 37.710812}, {"longitude": 55.721508, "latitude": 37.518414}, {"longitude": 55.763394, "latitude": 37.424728}]}
    ```
   Handler will return a Celery task id and task status
4) Check task status with GET-handler by task id until ready