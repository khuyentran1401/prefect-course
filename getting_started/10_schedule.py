from google_trends.main import create_pytrends_report
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule

deployment = Deployment.build_from_flow(
    flow=create_pytrends_report,
    name="get-stats-from-google-trends",
    version=1,
    work_queue_name="test",
    schedule=(CronSchedule(cron="0 0 * * *", timezone="America/Chicago")),
)
deployment.apply()
