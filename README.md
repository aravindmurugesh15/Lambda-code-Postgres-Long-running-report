# Lambda-StepFunction-code-Postgres-Long-running-report

An AWS Lambda and Step function that runs postgres long running queries greater than 5 seconds and sends out email as table.

It can be configured to run periodically using CloudWatch events.

## Quick start

1. Create an AWS lambda function:
    - Author from scratch
    - Runtime: Python 3.7
    - Architecture: x86_64
    - Layers: AWSSDKPandas-Python37, psycopg2
2. tab "Code" -> "Upload from" -> ".zip file":
    - copy paste the python code 
    - tab "Configuration" -> "General Configuration" -> "Edit"
        - Timeout: 15 minutes
    - Save
3. test the lambda function 
