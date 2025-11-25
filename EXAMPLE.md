# Quick Start Example

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure AWS Credentials

```bash
aws configure
```

## Step 3: Create an S3 Bucket (if needed)

```bash
aws s3 mb s3://my-bedrock-documents
```

## Step 4: Run the Sample

```bash
python sample.py \
  --bucket my-bedrock-documents \
  --file your-document.pdf \
  --query "What is this document about?"
```

## Real Example

Using a school district calendar:

```bash
python sample.py \
  --bucket my-bedrock-documents \
  --file SchoolDistrictCalendar2025-2026.pdf \
  --query "What are the major holidays observed?"
```

**Output:**
```
Uploading SchoolDistrictCalendar2025-2026.pdf to s3://my-bedrock-documents/bedrock-samples/SchoolDistrictCalendar2025-2026.pdf...
✓ Upload successful

Question: What are the major holidays observed?

Response:
================================================================================
According to the calendar, the major cultural and religious holidays observed include:
- Rosh Hashanah (September 22-24)
- Yom Kippur (October 1-2)
- Diwali (October 20)
- Christmas (December 25)
- Lunar New Year (February 17)
- Eid al-Fitr (March 19-20)
- Easter (April 5)
- Eid al-Adha (May 26-27)
================================================================================

Citations:
[1] Source: s3://my-bedrock-documents/bedrock-samples/SchoolDistrictCalendar2025-2026.pdf
    SEPTEMBER 22*-24  Rosh Hashanah OCTOBER 1*-2  Yom Kippur...
```

## What's Happening?

1. **Upload**: Your PDF is uploaded to S3
2. **Query**: Bedrock analyzes the document and answers your question
3. **Citations**: You get references to the source material

## Code Structure

The sample is intentionally simple (~75 lines) to show the core API pattern:

```python
# 1. Upload to S3
s3.upload_file(file_path, bucket, key)

# 2. Call Bedrock with S3 reference
response = bedrock.retrieve_and_generate(
    input={'text': query},
    retrieveAndGenerateConfiguration={
        'type': 'EXTERNAL_SOURCES',
        'externalSourcesConfiguration': {
            'modelArn': model_arn,
            'sources': [{
                'sourceType': 'S3',
                's3Location': {'uri': s3_uri}
            }]
        }
    }
)

# 3. Display results
print(response['output']['text'])
```
