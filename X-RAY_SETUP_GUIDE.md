# AWS X-Ray Setup Guide for Cruddur

## Overview
This guide documents the complete X-Ray tracing setup for the Cruddur application, including troubleshooting steps and configuration details.

## Current Working Configuration

### 1. Docker Compose Setup
```yaml
# X-Ray Daemon Service
xray-daemon:
  image: "amazon/aws-xray-daemon"
  environment:
    - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
    - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    - AWS_REGION=${AWS_REGION:-ca-central-1}
  command:
    - "xray -o -b xray-daemon:2000"
  ports:
    - 2000:2000/udp
  networks:
    - internal-network

# Backend Flask Service
backend-flask:
  environment:
    - AWS_XRAY_URL=${AWS_XRAY_URL}
    - AWS_XRAY_DAEMON_ADDRESS=xray-daemon:2000
    - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
    - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
```

### 2. Environment Variables (.env file)
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=ca-central-1
AWS_XRAY_URL=*localhost:4567*
```

### 3. Flask App Configuration (app.py)
```python
# X-Ray imports
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# X-Ray configuration
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)

# Example endpoint with X-Ray decorator
@app.route("/api/health-check", methods=["GET"])
@xray_recorder.capture('health_check')
def health_check():
    return {"success": True, "message": "Backend running fine!"}, 200
```

### 4. Service-Level Tracing
```python
# home_activities.py
from aws_xray_sdk.core import xray_recorder

class HomeActivities:
  @xray_recorder.capture('activities_home')
  def run():
    # Add subsegments for detailed tracing
    subsegment = xray_recorder.begin_subsegment('mock_data_generation')
    subsegment.put_metadata('user_count', 3)
    xray_recorder.end_subsegment()
    # ... rest of function
```

## How X-Ray Works

### Trace Generation
- **Event-Driven**: X-Ray only generates traces when API requests are made
- **Not Continuous**: Unlike logs, X-Ray doesn't send data constantly
- **Request-Response Cycle**: Each API call = one trace segment

### Normal Behavior
```
API Request → X-Ray Capture → Send to AWS → Wait for next request
```

### Expected Log Output
```
xray-daemon-1 | [Info] Successfully sent batch of 1 segments (0.352 seconds)
```

## Generating X-Ray Traces

### Method 1: Frontend Usage
- Open http://localhost:3000
- Navigate through the application
- Each page load triggers backend API calls

### Method 2: Direct API Calls
```bash
# Single requests
curl http://localhost:4567/api/activities/home
curl http://localhost:4567/api/activities/notifications
curl http://localhost:4567/api/health-check

# Continuous testing
while true; do
  curl -s http://localhost:4567/api/activities/home > /dev/null
  curl -s http://localhost:4567/api/activities/notifications > /dev/null
  sleep 10
done
```

### Method 3: Automated Testing Script
```bash
#!/bin/bash
# Generate X-Ray traces for testing
endpoints=(
  "/api/activities/home"
  "/api/activities/notifications"
  "/api/health-check"
)

for endpoint in "${endpoints[@]}"; do
  echo "Testing $endpoint"
  curl -s "http://localhost:4567$endpoint" > /dev/null
  sleep 2
done
```

## Current Active Endpoints with X-Ray

| Endpoint | Decorator | Subsegments |
|----------|-----------|-------------|
| `/api/activities/home` | ✅ `activities_home` | ✅ `mock_data_generation` |
| `/api/activities/notifications` | ✅ `activities_notifications` | ❌ |
| `/api/health-check` | ✅ `health_check` | ❌ |

## Viewing Traces in AWS Console

1. **Navigate to X-Ray Console**:
   - URL: https://ca-central-1.console.aws.amazon.com/xray/home
   - Region: ca-central-1

2. **Look for Service**:
   - Service Name: "Cruddur"
   - Traces appear within 1-2 minutes of API calls

3. **Trace Details**:
   - Service map shows request flow
   - Individual traces show timing and metadata
   - Subsegments provide detailed breakdowns

## Troubleshooting

### Common Issues and Solutions

#### 1. No Traces Appearing
**Check:**
```bash
# Verify X-Ray daemon is running
docker-compose ps | grep xray

# Check daemon logs
docker-compose logs xray-daemon

# Verify credentials
docker-compose exec xray-daemon env | grep AWS
```

#### 2. Credentials Not Working
**Solutions:**
- Ensure AWS credentials are in .env file
- Verify docker-compose uses `${AWS_ACCESS_KEY_ID}` syntax
- Test with: `aws sts get-caller-identity`

#### 3. Traces Stop After Initial Success
**This is Normal Behavior:**
- X-Ray is event-driven, not continuous
- Make API requests to generate new traces
- Use continuous testing script for ongoing traces

#### 4. Permission Errors
**Check IAM Permissions:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords"
      ],
      "Resource": "*"
    }
  ]
}
```

### Verification Commands
```bash
# Check if services are running
docker-compose ps

# View X-Ray daemon logs
docker-compose logs --tail=10 xray-daemon

# Test API endpoints
curl http://localhost:4567/api/health-check

# Monitor trace generation
docker-compose logs -f xray-daemon | grep "Successfully sent"
```

## Security Considerations

### .env File Usage
- ✅ **Acceptable**: For local development with proper .gitignore
- ✅ **Convenient**: Easy credential management
- ⚠️ **Risk**: Ensure .gitignore is properly configured
- 🔒 **Production**: Use IAM roles instead of access keys

### .gitignore Configuration
```bash
# Ensure .env is ignored
echo ".env" >> .gitignore
git rm --cached .env  # If already tracked
```

## Adding X-Ray to New Services

### Step 1: Import X-Ray
```python
from aws_xray_sdk.core import xray_recorder
```

### Step 2: Add Decorator
```python
@xray_recorder.capture('service_name')
def your_function():
    # function code
```

### Step 3: Add Subsegments (Optional)
```python
def your_function():
    subsegment = xray_recorder.begin_subsegment('operation_name')
    # operation code
    subsegment.put_metadata('key', 'value')
    xray_recorder.end_subsegment()
```

## Performance Impact

- **Minimal Overhead**: ~1-5ms per request
- **Network Usage**: Small trace data sent to AWS
- **Cost**: Pay per trace segment (very low cost for development)

## Best Practices

1. **Use Descriptive Names**: `activities_home` vs `function1`
2. **Add Metadata**: Include useful debugging information
3. **Subsegments for Detail**: Break down complex operations
4. **Error Handling**: X-Ray captures exceptions automatically
5. **Sampling Rules**: Configure in production to control costs

## Configuration Files Modified

- ✅ `docker-compose.yml` - X-Ray daemon and environment variables
- ✅ `.env` - AWS credentials and X-Ray URL
- ✅ `backend-flask/app.py` - X-Ray middleware and decorators
- ✅ `backend-flask/services/home_activities.py` - Service tracing
- ✅ `backend-flask/services/notifications_activities.py` - Service tracing
- ✅ `backend-flask/requirements.txt` - aws-xray-sdk dependency

## Success Indicators

✅ X-Ray daemon starts without errors
✅ Backend Flask initializes X-Ray middleware
✅ API requests generate "Successfully sent batch" logs
✅ Traces appear in AWS X-Ray console
✅ Service map shows "Cruddur" service
✅ Individual traces show timing and metadata

---

**Last Updated**: December 10, 2025
**Status**: ✅ Working Configuration
**Next Steps**: Add X-Ray to remaining API endpoints as needed