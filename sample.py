"""
AWS Bedrock External Sources Sample
Demonstrates how to upload a PDF to S3 and query it using Bedrock's retrieveAndGenerate API
"""

import boto3
import sys
import argparse
import os


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Upload PDF to S3 and query using Bedrock')
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--file', required=True, help='Local PDF file path')
    parser.add_argument('--query', required=True, help='Question to ask about the document')
    parser.add_argument('--region', default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--model', default='anthropic.claude-3-sonnet-20240229-v1:0', 
                       help='Bedrock model ID')
    args = parser.parse_args()

    # Generate S3 key from filename
    s3_key = f"bedrock-samples/{os.path.basename(args.file)}"
    s3_uri = f"s3://{args.bucket}/{s3_key}"
    
    # Initialize AWS clients
    s3 = boto3.client('s3', region_name=args.region)
    bedrock = boto3.client('bedrock-agent-runtime', region_name=args.region)
    
    try:
        # Step 1: Upload file to S3
        print(f"Uploading {args.file} to {s3_uri}...")
        s3.upload_file(args.file, args.bucket, s3_key)
        print("✓ Upload successful\n")
        
        # Step 2: Query the document using Bedrock
        print(f"Question: {args.query}\n")
        
        # Build model ARN
        model_arn = f"arn:aws:bedrock:{args.region}::foundation-model/{args.model}"
        
        # Call retrieveAndGenerate API
        response = bedrock.retrieve_and_generate(
            input={'text': args.query},
            retrieveAndGenerateConfiguration={
                'type': 'EXTERNAL_SOURCES',
                'externalSourcesConfiguration': {
                    'modelArn': model_arn,
                    'sources': [
                        {
                            'sourceType': 'S3',
                            's3Location': {'uri': s3_uri}
                        }
                    ]
                }
            }
        )
        
        # Display response
        print("Response:")
        print("=" * 80)
        print(response['output']['text'])
        print("=" * 80)
        
        # Display citations if present
        if 'citations' in response and response['citations']:
            print("\nCitations:")
            for i, citation in enumerate(response['citations'], 1):
                print(f"\n[{i}] Source: {s3_uri}")
                if 'retrievedReferences' in citation:
                    for ref in citation['retrievedReferences']:
                        if 'content' in ref and 'text' in ref['content']:
                            snippet = ref['content']['text'][:200]
                            print(f"    {snippet}...")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
