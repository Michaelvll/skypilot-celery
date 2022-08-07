import threading
import time
from proj.celery import run_sky

infer_tasks = []
finished = False

def inference_image(image_id: str):
    sky_task = run_sky.s('test-celery-sky', image_id)

    print(f'Starting Task for image {image_id}')
    infer_task = sky_task.apply_async()
    infer_tasks.append((image_id, infer_task))
    print(f'Task for image {image_id} started.')

def wait_for_tasks():
    while not finished or len(infer_tasks) > 0:
        if len(infer_tasks) == 0:
            time.sleep(1)
            continue

        for item in infer_tasks:
            image_id, infer_task = item
            if infer_task.ready():
                print(f'\nTask for image {image_id} finished.')
                infer_tasks.remove(item)
            

if __name__ == '__main__':
    task_thread = threading.Thread(target=wait_for_tasks)
    task_thread.start()

    while True:
        image_id = input('Enter image id: ')
        if image_id == 'q':
            finished = True
            break
        inference_image(image_id)

    task_thread.join()



