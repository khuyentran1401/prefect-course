from google_trends.main import create_pytrends_report
from prefect.deployments import Deployment

deployment = Deployment.build_from_flow(
    flow=create_pytrends_report,
    name="get-stats-from-google-trends",
    version=1,
    work_queue_name="test",
)
deployment.apply()
