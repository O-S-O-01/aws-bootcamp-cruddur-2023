from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from aws_xray_sdk.core import xray_recorder
from lib.db import db
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

      results = db.query_array_json("""
        SELECT
          activities.uuid,
          users.display_name,
          users.handle,
          activities.message,
          activities.replies_count,
          activities.reposts_count,
          activities.likes_count,
          activities.reply_to_activity_uuid,
          activities.expires_at,
          activities.created_at
        FROM public.activities
        LEFT JOIN public.users ON users.uuid = activities.user_uuid
        ORDER BY activities.created_at DESC
        """)
      return results