from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from aws_xray_sdk.core import xray_recorder
from lib.db import pool
import logging

LOGGER = logging.getLogger(__name__)
tracer = trace.get_tracer("home.activities")

class HomeActivities:
  @xray_recorder.capture('activities_home')
  def run(cognito_user_id=None):
    # in the line above, the bracket is supposed to have "logger" as parameter
    # in the line below, we disable logging to cloudwatch for this function
    #logger.info("HomeActivities")THE #TAG IS TO DISABLE LOGGING FOR THIS LINE AND PREVENT SPEND ON AWS CLOUDWATCH
    with tracer.start_as_current_span("home-activities-mock-data"):
      subsegment = xray_recorder.begin_subsegment('mock_data_generation')
      now = datetime.now(timezone.utc).astimezone()
      subsegment.put_metadata('user_count', 3)
      xray_recorder.end_subsegment()

      sql = """
      SELECT * FROM activities
      """
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchall()
      return json[0]