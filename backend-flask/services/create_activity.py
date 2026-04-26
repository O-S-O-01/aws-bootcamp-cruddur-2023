import uuid
from datetime import datetime, timedelta, timezone

from lib.db import db

class CreateActivity:
  def run(message, user_handle, ttl):
    model = {
      'errors': None,
      'data': None
    }

    user_uuid = ''
    sql = """
      INSERT INTO (
      use_uuid
      message
      expires_at
      )
      VALUES (
      "{user_uuid}"
      "{message}"
      "{expires_at}"
      )
    """

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'handle':  user_handle,
        'message': message
      }   
    else:
      expires_at = (now + ttl_offset)
      activity_uuid = CreateActivity.create_activity(handle=user_handle, message=message, expires_at=expires_at)
      object_json = CreateActivity.query_object_activity(activity_uuid)
      model['data'] = object_json
    return model

  def create_activity(handle, message, expires_at):
    sql = db.template('create_activity')
    activity_uuid = db.query_commit(sql, {
      'handle': handle,
      'message': message,
      'expires_at': expires_at
    })
    return activity_uuid

  def query_object_activity(activity_uuid):
    sql = db.template('create_activity_object')
    return db.query_object_json(sql, {'uuid': activity_uuid})

   
    
    