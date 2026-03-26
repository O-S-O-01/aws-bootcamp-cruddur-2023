# wk_0 - setting up github for my settup 

## Task Overview

This week was focused on laying the foundation for cruddur application,the gol was to ensure the AWS environment was secure and monitored for costs.

### GENERAL TASK COMPLETED

- [x] created a fresh AWS account and enabled MFA on the root and IAM user
- [x] created an IAM user with admin access and generated AWS credentials
- [x] successfully installed and authenticated the AWS CLI within my local WSL environment
- [X] configured a cloudwatch billing alarm to trigger an email at a $0.2 threshold using this

 '''{
    "AlarmName": "DailyEstimatedChargesforawsbootcampcruddur_followalong",
    "AlarmDescription": "This alarm would be triggered if the daily estimated charges exceeds 0.2$",
    "ActionsEnabled": true,
    "AlarmActions": [
       "arn:aws:sns:us-east-1:706004250326:billing-alarm" 
    ],
    "EvaluationPeriods": 1,
    "DatapointsToAlarm": 1,
    "Threshold": 50,
    "ComparisonOperator": "GreaterThanOrEqualToThreshold",
    "TreatMissingData": "breaching",
    "Metrics": [{
        "Id": "m1",
        "MetricStat": {
            "Metric": {
                "Namespace": "AWS/Billing",
                "MetricName": "EstimatedCharges",
                "Dimensions": [{
                    "Name": "Currency",
                    "Value": "USD"
                }]
            },
            "Period": 86400,
            "Stat": "Maximum"
        },
        "ReturnData": false
    },
    {
        "Id": "e1",
        "Expression": "IF(RATE(m1)>0,RATE(m1)*86400,0)",
        "Label": "DailyEstimatedCharges",
        "ReturnData": true
    }]
}'''

- [x] created an AS budget using the installed AWS CLI 

    '''{
    "BudgetLimit": {
        "Amount": "2",
        "Unit": "USD"
    },
    "BudgetName": "cli budget trial",
    "BudgetType": "COST",
    "CostFilters": {
        "TagKeyValue": [
            "user:Key$value1",
            "user:Key$value2"
        ]
    },
    "CostTypes": {
        "IncludeCredit": true,
        "IncludeDiscount": true,
        "IncludeOtherSubscription": true,
        "IncludeRecurring": true,
        "IncludeRefund": true,
        "IncludeSubscription": true,
        "IncludeSupport": true,
        "IncludeTax": true,
        "IncludeUpfront": true,
        "UseBlended": false
    },
    "TimePeriod": {
        "Start": 1477958399,
        "End": 3706473600
    },
    "TimeUnit": "MONTHLY"
}'''

---
***TECHNICAL CHALLENGES AND PERSONAL SOLUTION***

*challenge 1*: while the bootcamp suggested using gitpod (ona) i opted to build a local environment by installing WSL (ubuntu) to run linux environment in a windows UI, this is to enable linux-first development workflow which mirror production environment

*challenge 2:* a major pain point was getting github to recognize my WSL configuration. i initially strugguled with 'permission denied (publickey)' errors when trying to push or pull progress and i didnt want to enter my github credential manually so i did this

    - generated a new ED25519 SSH key pair specifically for WSL environment

    - configured my .bashrc file to automatically start the ssh agent amd add my private key whenever a terminal session starts.

    - added the public key to my github profile enabling seemless, passwordless and secure communication between my desktop amd the repository

*challenge 3:* i needed the AWS CLI in my WSL shell to remain authenticated across sessions without manually re-entering credentials. more importantly, i had to ensure my 'AWS_ACCESS_KEY_ID' and 'AWS_SECRET_ACCESS_KEY' were never exposed in my source code or accidentally committed to a public Github repository i did the following 
    
    - i addopted the .env pattern, a .env file in my project root to store sensitive credential using a git guardrail by creating a gitignore file and explicitly added a .env to the exclusion list. this ensured that my credential remained strictly local to my machine and were never tracked by version control
    
    - i configured my application to load environment variables from the .env file at runtime, this allowed me to access AWS credentials securely within my application without hardcoding them into the source code

*challenge 4* one of the requirement was to create the application logical architecture in lucidchart, i found it confusing so i skipped 