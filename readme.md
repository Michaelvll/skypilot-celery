# Run SkyPilot on Celery


## File hierarchy
```
- proj/
    |- __init__.py
    |- celery.py
- run.py
```

## Execute the SkyPilot task
1. Start redis service with `docker run -d -p 6379:6379 redis`.
2. Start the celery worker with `celery -A proj worker --logfile=/dev/null` in terminal 1.
3. Run SkyPilot task on top of celery: Run `python run.py` in another terminal (terminal 2).

Note: 
1. To debug any problems with the sky task or setup/run, you can check the output in terminal 1, where all the output will be streamed to there. 
2. If anything changed in the proj/celery.py, we need to restart the celery worker, i.e. kill the process in terminal 1 with ctrl-c, and then run the `celery -A proj worker --logfile=/dev/null` again.

