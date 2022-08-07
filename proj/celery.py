from __future__ import absolute_import
import textwrap

from celery import Celery
import sky



app = Celery(__name__, broker='redis://localhost:6379/0', result_backend='redis://localhost:6379/0')

SETUP_CMD = """\
    conda activate myenv
    if [ $? -eq 0 ]; then
        echo "conda env exists"
    else
        echo "creating conda env"
        conda create -n myenv python=3.8 -y
        conda activate myenv
        pip install tqdm
    fi
    """

RUN_CMD = textwrap.dedent("""\
    echo start training
    conda activate myenv
    python -u - <<EOF
    import time
    import tqdm
    print('Start training for image {image_id}')
    for i in tqdm.tqdm(range(120)):
        # 2 minutes training
        time.sleep(1)
    EOF
    """)


@app.task
def run_sky(cluster_name: str, image_id) -> str:
    print(f'Started with cluster_name: {cluster_name}')
    with sky.Dag() as dag:
        # The run command will be run on *all* nodes.
        # Should see two lines:
        #   My hostname: <host1>
        #   My hostname: <host2>
        sky.Task(
            setup=SETUP_CMD,
            run=RUN_CMD.format(image_id=image_id),
            num_nodes=1).set_resources(sky.Resources(sky.AWS()))

    sky.launch(dag, cluster_name=cluster_name)
    return 'success'


if __name__ == '__main__':
    app.start()
