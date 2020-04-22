import json
import boto3
import os
from datetime import datetime 
    
def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('ec2')
    
    # Insert your Instance ID here
    instance_id = os.environ['instance_id']
    downgrade_value = os.environ['downgrade_value']
    upgrade_value = os.environ['upgrade_value']
    
    # modify_value = upgrade_value 
    day = datetime.today().weekday()
    
    if day == 4:
        modify_value = upgrade_value
        print("Day is friday! Server will be upgraded to " + upgrade_value)
    elif day == 0:
        modify_value = downgrade_value
        print("Day is Monday! Server will be downgraded to " + downgrade_value)

    else: 
        print("Date is not Friday or Monday. Code is Existing")
        exit(4)

    
    print("instance_id: " + instance_id + " | modify_value: " + modify_value)
    
    # Stop the instance
    client.stop_instances(InstanceIds=[instance_id])
    waiter=client.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])
    print('Instance Stopped')
    
    # Change the instance type
    
    mod_status = client.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value=modify_value)
    print("mod_status: ", end=" ")
    print(mod_status)
    print('Instance modified')
    
    # Start the instance
    client.start_instances(InstanceIds=[instance_id])
    print('Instance restarted')
    
    return {
        "statusCode": 200,
        "body": json.dumps('Stream1 server modified')
    }

