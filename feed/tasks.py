from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from libs import verifManager as VM

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/15')),
    name="task_access_latest_headlines",
    ignore_result=True
)
def task_access_latest_headlines():
    VM.displayAll()
    logger.info("Retreived new trendingHls")