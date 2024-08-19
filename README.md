# ScheduleAvailability
Running with Docker (detached):
```
docker build --tag scheduleavailability .
docker run -d -p 5000:5000 scheduleavailability
```

Connect at ```http://localhost:5000/```


To run without a Docker image:
```
python3 -m venv <env_name>
python3 -m pip install -r requirements.txt
python3 -m flask run
```
Ensure chrome is installed if running without Docker.
