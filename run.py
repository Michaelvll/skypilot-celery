from proj.celery import run_sky

sky_task = run_sky.s('test-celery-sky-1')

print('Starting')
future = sky_task.apply_async()

print('Waiting for result')
future.get()

print('Finished')
