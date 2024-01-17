import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('s3')
    bucketlist = []
    allbuckets = client.list_buckets()["Buckets"]
    for bucket in allbuckets:
        bucketName=bucket["Name"]
        allobject=[]
        my_objects=client.list_objects_v2(Bucket=bucketName)
        try:
            for object1 in my_objects["Contents"]:
                response = client.get_object(Bucket=bucketName, Key=object1["Key"])["Body"].read().decode('utf-8')
                allobject.append({'Name':object1["Key"],'Content':response})
            bucketlist.append({'BucketName':bucketName,'Objects':allobject})
        except Exception  as e:
            bucketlist.append({'BucketName':bucketName,'Objects':{}})
            continue
        
    data={}
    data['statusCode'] = 200
    data['headers'] = {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
              "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
              "Access-Control-Allow-Methods": "OPTIONS,GET"
          }
    data['body'] = json.dumps(bucketlist)
     
    
    return data