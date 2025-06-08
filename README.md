# FirstGlueJob
This Glue Delployment to s3 i am creating for learning my first glue deployment.
✅ Overview
Create a GitHub repo and push your Glue script

Upload the script to an S3 bucket (Glue pulls it from S3)

Create a Glue Job that references this script

Run the Glue job and check results

🧱 STEP-BY-STEP GUIDE
🔹 STEP 1: Create GitHub Repository and Push Code
✅ 1.1 Create a GitHub Repo
Go to https://github.com/new and create a repo. Example:
my-glue-job

✅ 1.2 Clone It Locally
bash
Copy code
git clone https://github.com/your-username/my-glue-job.git
cd my-glue-job
✅ 1.3 Add Your Glue Script
Save your Glue script as: glue_job_script.py

You can use this simple working version:

python
Copy code
# glue_job_script.py

import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH', 'S3_OUTPUT_PATH', 'COLUMN_TO_DROP'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print("=== Job Started ===")
print(f"INPUT: {args['S3_INPUT_PATH']}")
print(f"OUTPUT: {args['S3_OUTPUT_PATH']}")
print(f"DROP COLUMN: {args['COLUMN_TO_DROP']}")

df = spark.read.option("header", "true").option("inferSchema", "true").csv(args['S3_INPUT_PATH'])

if args['COLUMN_TO_DROP'] in df.columns:
    df = df.drop(args['COLUMN_TO_DROP'])
    print(f"Dropped column: {args['COLUMN_TO_DROP']}")
else:
    print("Column not found, skipping drop.")

dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={"path": args['S3_OUTPUT_PATH']},
    format="parquet"
)

job.commit()
print("=== Job Finished ===")
✅ 1.4 Commit and Push
bash
Copy code
git add glue_job_script.py
git commit -m "Add AWS Glue job script"
git push origin main
🔹 STEP 2: Upload Script to S3
AWS Glue runs scripts from S3, not directly from GitHub.

✅ 2.1 Choose or Create an S3 Bucket
Example: my-glue-job-bucket

✅ 2.2 Upload Script
You can do this via AWS Console or CLI:

bash
Copy code
aws s3 cp glue_job_script.py s3://my-glue-job-bucket/scripts/glue_job_script.py
Now the script is at:

arduino
Copy code
s3://my-glue-job-bucket/scripts/glue_job_script.py
🔹 STEP 3: Create AWS Glue Job
✅ 3.1 Go to: AWS Glue Console
Navigate to Jobs > Add Job

Give it a name: glue-drop-column-job

IAM Role: Choose or create one with S3 access

Type: Spark

Glue version: Glue 4.0+

Script file path:
s3://my-glue-job-bucket/scripts/glue_job_script.py

Python version: 3.10

Temporary directory (required):
s3://my-glue-job-bucket/temp/

Click Next, then Save job and edit script (if needed), otherwise Save.

🔹 STEP 4: Run the Job
✅ 4.1 Configure Parameters
Click Run > Edit Job Parameters

Set:

bash
Copy code
--JOB_NAME=glue-drop-column-job
--S3_INPUT_PATH=s3://my-glue-job-bucket/input/
--S3_OUTPUT_PATH=s3://my-glue-job-bucket/output/
--COLUMN_TO_DROP=email
📌 Make sure:

input/ contains your CSV file(s)

output/ and temp/ folders are empty or writable

✅ 4.2 Run Job
Click Run Job.

🔹 STEP 5: Monitor Logs in CloudWatch
Go to AWS Glue > Jobs > Your Job

Click the job run → View logs

Watch for print() statements and confirm output is written

✅ Optional: Automate Deployment via Script (Future)
You can later:

Use a script to zip, upload to S3, and trigger Glue job via boto3

Integrate this into a GitHub Actions pipeline

🔚 You're Done!
You've now:

Put your code in GitHub

Uploaded it to S3

Deployed an AWS Glue job

Run it successfully with parameters

Would you like a sample GitHub Actions CI/CD pipeline to auto-deploy your script to S3 when you push?


You said:
I need automated deployment via script, so that when i pushed code into github, all the files or script to be pushed into s3, give me straight forward approach

ChatGPT said:
Perfect — here's a straightforward solution to automate S3 upload from GitHub when you push your code.

We’ll use GitHub Actions to detect your code changes and sync your repo to an S3 bucket automatically.

✅ What You’ll Achieve
When you git push to your GitHub repo:
➡️ A GitHub Actions workflow runs
➡️ Uploads glue_job_script.py (or all files) to your S3 bucket

🔧 Prerequisites
An S3 bucket (e.g. my-glue-job-bucket)

An IAM user with programmatic access and S3 permissions

GitHub repo with your Glue script

🔐 STEP 1: Create AWS IAM User for GitHub Access
Go to AWS IAM → Users

Create a new user: github-glue-deploy

Enable programmatic access

Attach AmazonS3FullAccess (or better: restrict to your bucket only)

Save the Access key ID and Secret access key

🔐 STEP 2: Add AWS Credentials to GitHub Secrets
In your GitHub repo:

Go to Settings > Secrets and variables > Actions > New repository secret

Add:

AWS_ACCESS_KEY_ID → (your IAM key)

AWS_SECRET_ACCESS_KEY → (your IAM secret)

📂 STEP 3: Create GitHub Actions Workflow
In your repo, create a folder and file:

bash
Copy code
mkdir -p .github/workflows
touch .github/workflows/deploy-to-s3.yml
Paste this into .github/workflows/deploy-to-s3.yml:

yaml
Copy code
name: Deploy Glue Script to S3

on:
  push:
    branches: [main]  # or 'master'

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v3
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1  # change if you're using a different region

      - name: Upload Glue scripts to S3
        run: |
          aws s3 cp glue_job_script.py s3://my-glue-job-bucket/scripts/glue_job_script.py
🔄 OPTIONAL: Upload All Files
Replace aws s3 cp with:

bash
Copy code
aws s3 sync . s3://my-glue-job-bucket/scripts/ --exclude ".git/*"
This will sync the whole repo (excluding .git/) to your S3 bucket.

🚀 STEP 4: Push to GitHub
bash
Copy code
git add .
git commit -m "Trigger Glue deploy to S3"
git push origin main
GitHub Actions will now:

Run the workflow

Upload your file(s) to S3 automatically

You can view it under: GitHub > Actions tab

🧪 STEP 5: Confirm on AWS
Go to S3 Console → my-glue-job-bucket/scripts/
➡️ You should see the updated glue_job_script.py

🏁 You’re Done!
From now on, every time you push code to GitHub:

Your script is automatically deployed to S3

You can use it immediately in your Glue job
