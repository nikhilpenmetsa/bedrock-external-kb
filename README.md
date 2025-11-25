# AWS Bedrock External Sources Sample

A simple Python sample demonstrating how to query PDF documents stored in S3 using Amazon Bedrock's `retrieveAndGenerate` API with External Sources.

## Overview

This sample shows how to:
1. Upload a PDF file to Amazon S3
2. Query the document using Amazon Bedrock's foundation models
3. Retrieve answers with citations from the source document

## Prerequisites

- Python 3.7+
- AWS account with access to:
  - Amazon S3
  - Amazon Bedrock (with Claude 3 Sonnet model enabled)
- AWS credentials configured (via AWS CLI, environment variables, or IAM role)

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
```bash
aws configure
```

## Usage

Basic usage:
```bash
python sample.py \
  --bucket YOUR_BUCKET_NAME \
  --file path/to/document.pdf \
  --query "Your question about the document"
```

### Example

```bash
python sample.py \
  --bucket my-documents \
  --file "Enterprise Rental Agreement.pdf" \
  --query "What are the key terms and conditions?"
```

### Options

- `--bucket` (required): S3 bucket name where the file will be uploaded
- `--file` (required): Path to the local PDF file
- `--query` (required): Question to ask about the document
- `--region` (optional): AWS region (default: us-east-1)
- `--model` (optional): Bedrock model ID (default: anthropic.claude-3-sonnet-20240229-v1:0)

## How It Works

1. **Upload**: The script uploads your PDF file to S3 under the `bedrock-samples/` prefix
2. **Configure**: Creates an ExternalSourcesRetrieveAndGenerateConfiguration pointing to the S3 URI
3. **Query**: Calls Bedrock's `retrieve_and_generate` API with your question
4. **Display**: Shows the AI-generated answer along with citations from the source document

## IAM Permissions Required

Your AWS credentials need the following permissions:

**S3 Permissions:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

**Bedrock Permissions:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:RetrieveAndGenerate"
      ],
      "Resource": "*"
    }
  ]
}
```

## Sample Output

```
Uploading Enterprise Rental Agreement.pdf to s3://my-bucket/bedrock-samples/Enterprise Rental Agreement.pdf...
✓ Upload successful

Question: What are the key terms and conditions?

Response:
================================================================================
Based on the rental agreement details provided, some key terms include:
- The rental period was from March 12, 2025 to March 14, 2025 (2 days)
- The rental rate was $41 per day, for a total of $82
- Unlimited mileage was included
...
================================================================================

Citations:
[1] Source: s3://my-bucket/bedrock-samples/Enterprise Rental Agreement.pdf
    Rental Agreement # 7JGT9L...
```

## Notes

- The S3 bucket must already exist before running the script
- Files are uploaded to the `bedrock-samples/` prefix in your bucket
- Bedrock model availability varies by region - ensure Claude 3 Sonnet is available in your chosen region
- Document size limits apply based on the Bedrock model used

## Troubleshooting

**"NoSuchBucket" error**: Create the S3 bucket first using `aws s3 mb s3://YOUR_BUCKET_NAME`

**"AccessDenied" error**: Verify your AWS credentials have the required IAM permissions

**"ResourceNotFoundException" error**: Ensure the Bedrock model is enabled in your AWS account and available in your region

## License

This sample code is provided as-is for demonstration purposes.
