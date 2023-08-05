from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend='rpc://')

app.conf.beat_schedule = {
    'fetch-every-30-minutes': {
        'task': 'tasks.fetch_articles',
        'schedule': 30.0 * 60.0,
    },
    'process-every-hour': {
        'task': 'tasks.process_articles',
        'schedule': 60.0 * 60.0,
    },
}
app.conf.timezone = 'UTC'
