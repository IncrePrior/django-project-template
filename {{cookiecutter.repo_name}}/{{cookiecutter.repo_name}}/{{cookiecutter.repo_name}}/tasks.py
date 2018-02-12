import logging

from {{cookiecutter.repo_name}}.celery import app


logger = logging.getLogger(__name__)


@app.task
def default_task():
    logger.info('This is a default Celery test task (no-op)')
