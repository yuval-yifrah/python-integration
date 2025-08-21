#!/usr/bin/env python

import uuid
import click
import boto3
import os

CREATED_BY = "yuvaly"
UBUNTU_AMI = "ami-020cba7c55df1f615"
AMAZON_LINUX = "ami-00ca32bbc84273381"

@click.group()
def cli():
    pass

@cli.group()
def ec2():
    pass

@cli.group()
def s3():
    pass

@cli.group()
def route53():
    pass

def aws_connect(resource):
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION")
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    client = session.client(resource)
    return client

@ec2.command("create")
@click.argument("ami", type=click.Choice(["ubuntu", "amazon-linux"], case_sensitive=False))
@click.argument("instance_type", type=click.Choice(["t3.micro", "t2.small"], case_sensitive=False))
def create_ec2(ami,instance_type):
    client = aws_connect("ec2")
    """
    AMI: ubuntu/amazon-linux

    instance_type: t3.micro/t2.small
    """
    ami_id = UBUNTU_AMI if ami.lower() == "ubuntu" else AMAZON_LINUX
    running_count = count_list_ec2()
    if running_count < 2:
        client.run_instances(
            ImageId=ami_id,
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [{"Key": "Name", "Value": f"{CREATED_BY}-{ami}-{instance_type}"},{'Key': 'CreatedBy', 'Value': CREATED_BY}]
                }
            ]
        )
        print(f"created an instance with {ami_id} and {instance_type}")
    else:
        print("you cant have more than 2 instance running")


@ec2.command("manage")
@click.argument("action", type=click.Choice(["start", "stop","terminate"], case_sensitive=False))
@click.argument("instance_id")
def manage_ec2(action,instance_id):
    client = aws_connect("ec2")
    """
    action: start/stop/terminate
    """
    if action == "start":
        running_count = count_list_ec2()
        if running_count < 2:
            client.start_instances(InstanceIds=[instance_id])
        else:
            print("you cant have more than 2 instance running")
    elif action == "stop":
        client.stop_instances(InstanceIds=[instance_id])
    elif action == "terminate":
        client.terminate_instances(InstanceIds=[instance_id])
    print(action)

def count_list_ec2():
    client = aws_connect("ec2")
    response = client.describe_instances()
    found = False
    count = 0

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            tags = {t["Key"]: t["Value"] for t in instance.get("Tags", [])}
            if tags.get("CreatedBy") == CREATED_BY:
                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                state = instance["State"]["Name"]
                print(f"ID: {instance_id} | Type: {instance_type} | State: {state}")
                if state == "running":
                    count += 1
                found = True
    if not found:
        print("No instances found.")
    return count

@ec2.command("list")
def list_ec2():
    count_list_ec2()

@s3.command("create")
@click.argument("visibility_type", type=click.Choice(["public", "private"], case_sensitive=False))
@click.argument("name")
def create_s3(visibility_type, name):
    client = aws_connect("s3")
    client.create_bucket(Bucket=name)
    client.put_bucket_tagging(
        Bucket=name,
        Tagging={
            'TagSet': [
                {'Key': 'CreatedBy', 'Value': CREATED_BY},
                {'Key': 'Visibility', 'Value': visibility_type}
            ]
        }
    )
    """
    visibility_type: public/private

    name: name of bucket
    """
    if visibility_type == "public":
        confirm = click.confirm('are you sure?')
        if confirm:
            client.put_public_access_block(
                Bucket=name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            print(f"Bucket '{name}' created as public")
        else:
            print("Aborted")
    elif visibility_type == "private":
        print(f"Bucket '{name}' created as private")


@s3.command("upload")
@click.argument("file_name")
@click.argument("bucket_name")
@click.argument("object_name")
def upload_s3(file_name, bucket_name, object_name):
    client = aws_connect("s3")

    """
    file_name: full file path and name
    bucket_name: bucket name when you created the bucket
    object_name: object name - the name of the file in s3
    """

    client.upload_file(file_name, bucket_name, object_name)
    print("added")

@s3.command("list")
def list_s3():
    client = aws_connect("s3")
    response = client.list_buckets()
    found = False

    for bucket in response["Buckets"]:
        bucket_name = bucket["Name"]
        try:
            resp_tag = client.get_bucket_tagging(Bucket=bucket_name)
            tags = {t["Key"]: t["Value"] for t in resp_tag["TagSet"]}
            if tags.get("CreatedBy") == CREATED_BY:
                print(f"bucket name: {bucket_name}")
                found = True
        except client.exceptions.ClientError as e:
            err_code = e.response["Error"]["Code"]
            if err_code not in ["NoSuchTagSet", "AccessDenied"]:
                raise

    if not found:
        print("No buckets found.")

@route53.command("create")
@click.argument("zone_name")
def create_route53(zone_name):
    client = aws_connect("route53")
    """ 
    zone_name: the dns name for your zone. please add .com at the end
    """
    call_ref = str(uuid.uuid4())
    response = client.create_hosted_zone(Name=zone_name,CallerReference=call_ref)
    zone_id = response["HostedZone"]["Id"].split("/")[-1]

    client.change_tags_for_resource(
        ResourceType="hostedzone",
        ResourceId=zone_id,
        AddTags=[{"Key": "CreatedBy", "Value": CREATED_BY}]
    )

    print(f"created a zone name {zone_name}")

@route53.command("manage")
@click.argument("action", type=click.Choice(["create","upsert", "delete"], case_sensitive=False))
@click.argument("zone_name")
@click.argument("record_name")
@click.argument("record_type")
@click.argument("record_value")
def manage_route53(action, zone_name, record_name, record_type, record_value):
    """
    manage actions: create/upsert/delete
    zone_name: the dns name for your zone. please add .com at the end
    record_name: name of the record to update must include zone name in it (https, https, www)
    record_type: type of the record to update (A, AAAA, CNAME, MX, NS, PTR, SOA, SPF, SRV, TXT, CAA, DS, NAPTR, TLS)
    record_value: value of the record to update
    """
    client = aws_connect("route53")

    try:
        zones = client.list_hosted_zones()["HostedZones"]
    except Exception as e:
        print("Error listing hosted zones:", str(e))
        return

    hosted_zone_id = None
    for zone in zones:
        if zone["Name"].rstrip(".") == zone_name.rstrip("."):
            hosted_zone_id = zone["Id"].split("/")[-1]
            break

    if not hosted_zone_id:
        print(f"No hosted zone found for {zone_name}")
        return

    change_batch = {
        "Changes": [
            {
                "Action": action.upper(),
                "ResourceRecordSet": {
                    "Name": record_name,
                    "Type": record_type,
                    "TTL": 300,
                    "ResourceRecords": [{"Value": record_value}]
                }
            }
        ]
    }

    try:
        response = client.change_resource_record_sets(HostedZoneId=hosted_zone_id,ChangeBatch=change_batch)
        print(f"{action} record response:", response)
    except Exception as e:
        print("Error updating Route53 record:", str(e))


@route53.command("list")
def list_route53():
    client = aws_connect("route53")
    zones = client.list_hosted_zones()["HostedZones"]

    for zone in zones:
        zone_id = zone["Id"].split("/")[-1]
        zone_name = zone["Name"]

        tags_response = client.list_tags_for_resource(
            ResourceType="hostedzone",
            ResourceId=zone_id
        )
        tags = {t["Key"]: t["Value"] for t in tags_response["ResourceTagSet"]["Tags"]}
        if tags.get("CreatedBy") == CREATED_BY:
            print(f"{zone_name}, zone_id: {zone_id}")

if __name__ == "__main__":
    cli()
