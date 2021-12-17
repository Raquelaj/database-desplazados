import boto3

# Get the service resource.
s3_client = boto3.client('s3')

for bucket in boto3.resource('s3').buckets.all():
    print(bucket.name)

s3_client.upload_file("/Users/leonardo/projetos/db-deslocados/data/pdfs/onic-0c009ac5fc897e3ef3d6214b48e169f7.pdf", "desplazados", "onic-0c009ac5fc897e3ef3d6214b48e169f7.pdf")
