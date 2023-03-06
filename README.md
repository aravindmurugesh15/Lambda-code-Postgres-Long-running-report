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

4. Create the step function and copy past the json then save it.

5. Change then lambda function name you created in the code and email address to sent to in the step function then save and test.

## Run the step function 
