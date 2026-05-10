# Week 2 — Distributed Tracing

## Task Overview
The primary focus of this week was implementing observability and distributed tracing. I instrumented the Cruddur backend with Honeycomb (OpenTelemetry), AWS X-Ray, CloudWatch Logs, and Rollbar. Beyond just following the bootcamp, I focused on making the environment platform-agnostic by building a custom DevContainer and solving critical compatibility issues between modern Flask versions and the bootcamp's legacy code.

## GENERAL TASKS COMPLETED
- [x] **Instrumented Honeycomb with OpenTelemetry:** Configured the Flask app to send spans to Honeycomb and added local console logging for easier debugging.
- [x] **AWS X-Ray Integration:** Set up the X-Ray recorder and middleware, and added the X-Ray daemon as a sidecar service in `docker-compose.yml`.
- [x] **CloudWatch Logging:** Integrated `watchtower` to ship application logs to AWS, ensuring proper credential mapping for local/containerized environments.
- [x] **Rollbar Implementation:** Added error tracking and verified it with a custom error-triggering route.
- [x] **Backend Health Check:** Added a `/api/health-check` route to prevent 404 errors during future automated health checks.
- [x] **Universal Dev Environment:** Created a `.devcontainer.json` setup to allow the project to run seamlessly on **GitHub Codespaces**, **Gitpod**, **Ona**, and local **VS Code**.

## TECHNICAL CHALLENGES AND PERSONAL SOLUTIONS

### Challenge 1: Lack of Local Visibility for Traces
The default OpenTelemetry setup only sends data to Honeycomb. If the network fails, I wouldn't see anything.
- ***My Solution:*** I updated `app.py` to include `ConsoleSpanExporter` and `SimpleSpanProcessor`. This allowed me to see the raw spans in my Docker logs immediately, while still sending the batched data to Honeycomb.changing this 
```py
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
``` 
to this
```py
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor
```
in app.py

```py
# Initialize tracing and an exporter that can send data to Honeycomb

provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
``` 
to this
```py
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(honeycomb_exporter))
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
```

### Challenge 2: Honeycomb Endpoint and Header Formatting
Using the base Honeycomb URL often fails in Python OTLP exporters.
- ***My Solution:*** I updated the `docker-compose.yml` environment variables to use the explicit `/v1/traces` endpoint: `https://honeycomb.io`. I also added shell defaults `${HONEYCOMB_API_KEY:-}` to prevent the container from crashing if the key is missing.this was done by changing this 
```yml
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
```
to this 
```yml
- OTEL_SERVICE_NAME=${SERVICE_NAME:-backend-flask}
- OTEL_EXPORTER_OTLP_ENDPOINT=https://api.honeycomb.io/v1/traces
- OTEL_EXPORTER_OTLP_HEADERS=x-honeycomb-team=${HONEYCOMB_API_KEY:-}
```

### Challenge 3: Portability Across Gitpod, Codespaces, and Local
I wanted my setup to work anywhere (Gitpod, GitHub Codespaces, or local) without manually installing tools every time.
- ***My Solution:*** I created a `.devcontainer/devcontainer.json` file. I explicitly added "features" for **Node 18**, **AWS-CLI**, and          **Docker-in-Docker**. This fixed the "npm command not found" error I hit on Gitpod and ensured that whether I'm in the cloud or on my desktop, the environment is identical.

### Challenge 4: Flask 3.x Breaking Changes (`before_first_request`)
During `pip install`, Docker fetched Flask 3.x, which removed the `before_first_request` method used by Rollbar and the bootcamp code, causing the backend to crash with an `AttributeError`.
- ***My Solution:*** I identified that the code was written for Flask 2.2. I modified `requirements.txt` to hard-code `Flask==2.2.5`. This resolved the crash and restored the functionality of the Rollbar initialization decorators.

### Challenge 5: Testing Rollbar with Missing Routes
I tried to test Rollbar using `/rollbar/error` but kept getting a 404 because that route didn't exist in the provided bootcamp code.
- ***My Solution:*** I manually defined the route in `app.py` and implemented a `try/except` block with a `1 / 0` (ZeroDivisionError) to force a real exception. This confirmed that `rollbar.report_exc_info()` was correctly capturing and sending real errors to the dashboard. this was done by doing this to `backend-flask/app.py` file

```
@app.route('/rollbar/error')
def rollbar_error():
    try:
        1 / 0  # force a ZeroDivisionError
    except Exception:
        rollbar.report_exc_info()  # send exception to Rollbar
    return "Error sent to Rollbar!"
```
### Challenge 6: "Short Read" Image Build Failures
I encountered `short read: expected 51600110 bytes but got 23085056: unexpected EOF` during the Docker build process.
- ***My Solution:*** I realized this was due to an unstable internet connection dropping mid-download. I re-established my connection and rebuilt the images, allowing Docker to resume from the cached layers.

### Challenge 7: X-Ray Traces Stopping After Initial Success
After the first few traces were sent to AWS X-Ray, the daemon logs showed no new activity:
```
xray-daemon-1 | [Info] Successfully sent batch of 1 segments (1.131 seconds)
xray-daemon-1 | [Info] Successfully sent batch of 1 segments (0.311 seconds)
# ... nothing after this
```
- ***My Solution:*** X-Ray is not a continuous monitoring tool. It only sends data when an actual API request hits the backend. No request = no trace. The daemon was working perfectly, it was just waiting for something to trace. I added `@xray_recorder.capture()` decorators to the service functions so X-Ray had more to trace, then made API requests to generate activity:

```python
# home_activities.py
from aws_xray_sdk.core import xray_recorder

class HomeActivities:
  @xray_recorder.capture('activities_home')
  def run():
```

```python
# notifications_activities.py
from aws_xray_sdk.core import xray_recorder

class NotificationsActivities:
  @xray_recorder.capture('activities_notifications')
  def run():
```

```python
# app.py
@app.route("/api/health-check", methods=["GET"])
@xray_recorder.capture('health_check')
def health_check():
```

After making requests to the endpoints, the daemon confirmed traces were being sent:
```
xray-daemon-1 | [Info] Successfully sent batch of 1 segments (0.352 seconds)
xray-daemon-1 | [Info] Successfully sent batch of 1 segments (0.280 seconds)
xray-daemon-1 | [Info] Successfully sent batch of 1 segments (0.335 seconds)
```

---
### this were the content of my .env file at this point

FRONTEND_URL=http://localhost:3000

BACKEND_URL=http://localhost:4567

REACT_APP_BACKEND_URL=http://localhost:4567

AWS_XRAY_URL=*localhost:4567*

#### AWS Configuration

AWS_ACCESS_KEY_ID=XXXXXXX

AWS_SECRET_ACCESS_KEY=XXXX

AWS_REGION=ca-central-1

AWS_DEFAULT_REGION=ca-central-1

#### Honeycomb Configuration

HONEYCOMB_API_KEY=XXXXXXXX

HONEYCOMB_DATASET=cruddur

SERVICE_NAME=backend-flask

#### Rollbar Configuration

ROLLBAR_ACCESS_TOKEN=XXXXX