import boto3

# Get the service resource.
from boto3.dynamodb.conditions import Key

from model.post import Post
from persistence.sqs.message_wrapper import send_message

dynamodb = boto3.resource('dynamodb')
sqs = boto3.resource('sqs')

table = dynamodb.Table('desplazados')


def save_post(post: Post):
    try:
        table.put_item(
            Item=post.to_dict()
        )
    except Exception as e:
        print(e)
        print(post)
        send_message('not-quite-dlq', post.to_json(), {"source": post.source})


def is_post_extracted(post: Post):
    response = table.query(
        KeyConditionExpression=
            Key('pk').eq(Post.build_key(post.source, True)) & Key('sk').eq(post.sk)
    )
    return len(response['Items']) == 1


def delete_post(post: Post):
    try:
        table.delete_item(
            Key={"pk": post.pk, "sk": post.sk}
        )
    except Exception as e:
        print(e)
        print(post)


def query_post(source: str, is_downloaded: bool):
    response = table.query(
        KeyConditionExpression=Key('pk').eq(Post.build_key(source, is_downloaded))
    )

    return response['Items']
