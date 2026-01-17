from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from aws_xray_sdk.core import xray_recorder
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
  
      results = [{
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Andrew Brown',
        'message': 'Cloud is fun!',
        'created_at': (now - timedelta(days=2)).isoformat(),
        'expires_at': (now + timedelta(days=5)).isoformat(),
        'likes_count': 5,
        'replies_count': 1,
        'reposts_count': 0,
        'replies': [{
          'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
          'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
          'handle':  'Worf',
          'message': 'This post has no honor!',
          'likes_count': 0,
          'replies_count': 0,
          'reposts_count': 0,
          'created_at': (now - timedelta(days=2)).isoformat()
        }],
      },
      {
        'uuid': '66e12864-8c26-4c3a-9658-95a10f8fea67',
        'handle':  'Worf',
        'message': 'I am out of prune juice',
        'created_at': (now - timedelta(days=7)).isoformat(),
        'expires_at': (now + timedelta(days=9)).isoformat(),
        'likes': 0,
        'replies': []
      },
      {
        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
        'handle':  'Garek',
        'message': 'My dear doctor, I am just simple tailor',
        'created_at': (now - timedelta(hours=1)).isoformat(),
        'expires_at': (now + timedelta(hours=12)).isoformat(),
        'likes': 0,
        'replies': []
      }
      ]
      if cognito_user_id != None:
        extra_crud = {
          'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
          'handle':  'obinna',
          'message': 'My dear brother, it is great to be back to the village',
          'created_at': (now - timedelta(hours=1)).isoformat(),
          'expires_at': (now + timedelta(hours=12)).isoformat(),
          'likes': 3000,
          'replies': []
        }
        results.insert(0, extra_crud)
        span.set_attribute("app.result_length", len(results))
      
      return results