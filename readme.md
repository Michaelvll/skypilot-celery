# Run SkyPilot on Celery


## File hierarchy
```
- proj/
    |- __init__.py
    |- celery.py
- run.py
```

## Execute the SkyPilot task
1. Start the celery worker with `celery -A proj worker --logfile=/dev/null` in terminal 1.
2. Run SkyPilot task on top of celery: Run `python run.py` in another terminal (terminal 2).

Note: To debug any problems with the sky task or setup/run, you can check the output in terminal 1, where all the output will be streamed to there.
