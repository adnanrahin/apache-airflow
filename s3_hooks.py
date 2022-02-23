from airflow.hooks.S3_hook import S3Hook


def create_bucket():
    hook = S3Hook(aws_conn_id='aws_credentials')
    hook.create_bucket(bucket_name='optimus-prime-test-arahin')


# create_bucket()


def list_bucket():
    hook = S3Hook(aws_conn_id='aws_credentials')
    lr = hook.list_keys(bucket_name='spark-flight-data-bucket')
    print(lr)


list_bucket()