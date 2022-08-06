from __future__ import absolute_import
from celery import Celery

import sky



app = Celery(__name__, broker='redis://localhost:6379/0', result_backend='redis://localhost:6379/0')

SETUP_CMD = 'conda env list'

RUN_CMD = 'echo My hostname: $(hostname)'


@app.task
def run_sky(cluster_name: str) -> str:
    print(f'Started with cluster_name: {cluster_name}')
    with sky.Dag() as dag:
        # The run command will be run on *all* nodes.
        # Should see two lines:
        #   My hostname: <host1>
        #   My hostname: <host2>
        sky.Task(
            setup=SETUP_CMD,
            run=RUN_CMD,
            num_nodes=1).set_resources(sky.Resources(sky.AWS()))

    sky.launch(dag, cluster_name=cluster_name)
    return 'success'


if __name__ == '__main__':
    app.start()
