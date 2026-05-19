# Week 4 — Relational Databases (Postgres and RDS)

## Task Overview
This week was a deep dive into data persistence. I transitioned the Cruddur application from mock data to a production-grade PostgreSQL architecture. This involved local DB automation, provisioning Amazon RDS, and building a secure bridge between Amazon Cognito and Postgres using AWS Lambda. I also refactored the backend to a "Templated SQL" architecture for better code maintainability and security.

## GENERAL TASKS COMPLETED
- [x] **Local Postgres & RDS Provisioning:** Set up a local Docker Postgres instance and launched an AWS RDS `db.t3.micro` instance.
- [x] **Automation Suite:** Developed bash scripts (`db-connect`, `db-schema-load`, `db-seed`, etc.) using `sed` for dynamic URL handling and ANSI colors for better logging.
- [x] **Templated SQL Architecture:** Created a "bridge" in `lib/db.py` using `db.template()` to decouple SQL logic from Python services, moving queries into dedicated `.sql` files in `/backend-flask/db/sql`.
- [x] **Post-Confirmation Lambda:** Developed a Lambda function to automatically insert new Cognito users into the RDS `users` table upon email confirmation.
- [x] **Reusable Infrastructure:** Created a dedicated GitHub repository [aws-lambda-psycopg2-layer](https://github.com) for building AWS Lambda layers for `psycopg2`.
- [x] **Backend & Frontend Auth Integration:** Refactored the Flask backend to verify JWT tokens and updated the React frontend to pass the `Authorization` header.
- [x] **SQL JSON Wrapping:** Implemented `query_wrap_object` and `query_wrap_array` to offload JSON formatting to the Postgres engine.

## TECHNICAL CHALLENGES AND PERSONAL SOLUTIONS

### Challenge 1: Psycopg3 Parameter & Syntax Errors
I hit `psycopg.errors.SyntaxError: syntax error at or near ";"` in `backend-flask/db/sql/create_activity_object.sql`.
**My Solution:** I identified that Psycopg3 handles typing natively. I removed `$1::uuid`, the trailing semicolon, and switched to named parameters: `WHERE activities.uuid = %(uuid)s`.

### Challenge 2: The "Cognito Sub" Lookup Trap
Inserts failed because `claims['username']` returns the Cognito `sub` (UUID).
**My Solution:** I updated the SQL templates to match against the `cognito_user_id` column: `WHERE users.cognito_user_id = %(handle)s::text`.

### Challenge 3: Lambda Dependency & Runtime Mismatches
The Lambda crashed with `No module named 'psycopg2._psycopg'`. 
**My Solution:** I built a custom layer using my [https://github.com/O-S-O-01/aws-lambda-psycopg2-layer]. I used a `build.sh` script to install `psycopg2-binary -t python/`, zip it, and upload it as a layer compatible with Python 3.11+.

### Challenge 4: Lambda Task Timeout (VPC/Networking)
The Lambda timed out after 3.00 seconds while trying to connect to RDS.
**My Solution:** I updated the RDS Security Group inbound rules to allow the current traffic, as the IP address had changed, preventing the connection from hanging.

### Challenge 5: "Fetch What You Created" Pattern
The frontend showed mock data after a post because the return object was hardcoded.
**My Solution:** I refactored `create_activity.py` to capture the `activity_uuid` from the insert and then called `db.template('create_activity_object')` to fetch the real joined object from the database.

### Challenge 6: Argument Mismatch in DB Template
I hit `TypeError: DB.template() takes 2 positional arguments but 3 were given`.
**My Solution:** I corrected the call from `db.template('activities', 'home')` to `db.template('home')` in `home_activities.py`, passing only the file name as required by the `lib/db.py` definition.

### Challenge 7: Hardcoded User Handles
The backend attempted inserts for a hardcoded `'paulooh'` handle that didn't exist in production.
**My Solution:** I refactored `app.py` to use `claims = cognito_jwt_token.verify(access_token)` and `user_handle = claims['username']` for dynamic user identification.

### Challenge 8: Missing Frontend Auth Token
Backend logs showed `DEBUG in app: No token provided` and `401 Unauthorized`.
**My Solution:** I updated the `ActivityForm.js` headers to include `'Authorization': 'Bearer ${localStorage.getItem("access_token")}'`.

### Challenge 9: Post-Confirmation Lambda Syntax
The Lambda failed with `invalid syntax (lambda_function.py, line 1)` due to malformed triple quotes and unquoted SQL values.
**My Solution:** I refactored the function to use clean multiline strings and `%s` parameterization:
```python
sql = "INSERT INTO users (display_name, email, handle, cognito_user_id) VALUES (%s, %s, %s, %s)"
cur.execute(sql, (user_display_name, user_email, user_handle, user_cognito_id))
```

### Challenge 10: Incomplete Table Definitions & SQL Syntax
I hit `ERROR: syntax error at end of input` in my schema files.
**My Solution:** I fixed the `INSERT INTO public.activities` in `create_activity.sql` by adding missing commas and corrected the `CREATE TABLE` structure to ensure all blocks were properly closed with `);`.

### Challenge 11: Import Syntax Errors
I hit `SyntaxError: invalid syntax` on the backend due to `import flask import current_app as app`.
**My Solution:** I corrected the import to `from flask import current_app as app`.

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

#### AWS Cognito Configuration

AWS_COGNITO_USER_POOL_ID=ca-central-1_yyyy

AWS_COGNITO_USER_POOL_CLIENT_ID=zzzz

AWS_USER_POOLS_ID=ca-central-1_yyyy

AWS_CLIENT_ID=zzzz

REACT_APP_AWS_USER_POOLS_ID=ca-central-1_yyyy

REACT_APP_CLIENT_ID=zzzz

#### postgres connection_url
CONNECTION_URL=postgresql://qwest:password@db:5432/cruddur
#CONNECTION_URL=postgresql://qwest:password@localhost:5432/cruddur
PROD_CONNECTION_URL=postgresql://xxxx:xxxx@cruddur-db-instance.xxxx.ca-central-1.rds.amazonaws.com:5432/cruddur

#### AWS Security Group Configuration for RDS
DB_SG_ID="xxxx"

#### AWS Security Group inbound Rule ID for RDS (lin39-42 is done in order to allow access to RDS from local machine and EC2 instance)
DB_SG_RULE_ID="xxxx"

#### to view my ip use curl ifconfig.me
MY_IP=xxx.xxx.x.x