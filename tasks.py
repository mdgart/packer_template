from celery import Celery
from celery.signals import task_sent, task_success, task_postrun

app = Celery('tasks', broker='amqp://', backend='amqp://')

@app.task
def get_packer_version():
    from subprocess import Popen, PIPE
    args = ["packer -machine-readable version"]
    p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    (out, err) = p.communicate()
    #out = [o.split(",") for o in out.split("\n")]
    return (out, err)
    

@task_success.connect
def task_success_handler(sender=None, result=None, args=None, kwargs=None, **kwds):
    f = open('workfile', 'w')
    value = ('''Success!
        sender:%s
        result:%s
        args:%s
        kwargs:%s
        kwds:%s''' % (dir(sender), result, args, kwargs, kwds))
    s = str(value)
    f.write(s)
    f.close()


r = get_packer_version.delay()
