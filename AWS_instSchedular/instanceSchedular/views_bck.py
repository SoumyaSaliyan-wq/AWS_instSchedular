from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def createSchedule(request):
    response = HttpResponse()
    response_data = {}
    response_data['status']='ERROR'
    response= JsonResponse(response_data)   
    try:
        if request.method=='POST':
            print(json.loads(request.body))
            sys.stdout.flush()
            response_data['status']='OK'
            response= JsonResponse(response_data)
    except Exception as e:
         response_data['status']='ERROR'

    return response

@csrf_exempt
def updateSchedule(request):
    response = HttpResponse()
    response_data = {}
    response_data['status']='ERROR'
    response= JsonResponse(response_data)
    try:
        if request.method=='POST':
            print(json.loads(request.body))
            sys.stdout.flush()
            response_data['status']='OK'
            response= JsonResponse(response_data)
    except Exception as e:
         response_data['status']='ERROR'

    return response    


@csrf_exempt
def deleteSchedule(request):
    response = HttpResponse()
    response_data = {}
    response_data['status']='ERROR'
    response= JsonResponse(response_data)
    try:
        if request.method=='POST':
            print(json.loads(request.body))
            sys.stdout.flush()
            response_data['status']='OK'
            response= JsonResponse(response_data)
    except Exception as e:
         response_data['status']='ERROR'

    return response     

@csrf_exempt
def fetchSchedule(request):
    response = HttpResponse()
    response_data = {}
    response_data['status']='ERROR'
    response= JsonResponse(response_data)
    try:
        if request.method=='POST':
            print(json.loads(request.body))
            sys.stdout.flush()
            response_data['status']='OK'
            response= JsonResponse(response_data)
    except Exception as e:
         response_data['status']='ERROR'

    return response     


# import boto3
# region = 'us-east-2b'
# instances = ['i-026d76cf93e7ee999']
# ec2 = boto3.client('ec2', region_name=region)

# def stopInstance(event, context):
#     ec2.stop_instances(InstanceIds=instances)
#     print('stopped your instances: ' + str(instances))
#     message = event['Schedule Configuration']
#     message1 = event['Instance Identifier']
#     return { 
#         'Schedule Configuration' : message,
#         'Instance Identifier':message1
#     }

# {
#   "Instance Identifier": " i-0ff3ef889f1bef5c9",
#   "Schedule Configuration": {
#       "Schedule":"stop"
#   }
# }    


# def startInstance(event, context):
#     ec2.start_instances(InstanceIds=instances)
#     print('started your instances: ' + str(instances))



import boto3
import json

client = boto3.client('events')
lambda_client = boto3.client('lambda')

@csrf_exempt
def scheduleAwsInstance(request):
    response = HttpResponse()
    response_data = {}
    response_data['status']='ERROR'
    aws_response={}
    response= JsonResponse(response_data)
    jsonrequest=json.loads(request.body)   
    try:
        if request.method=='POST':
            if(jsonrequest['Event_Type']=="ADD"):
                print(eval(jsonrequest["Schedule_Configuration"]["Minutes"]))
                minutes=eval(jsonrequest["Schedule_Configuration"]["Minutes"])
                hours=eval(jsonrequest["Schedule_Configuration"]["Hours"])
                Day_of_month=jsonrequest["Schedule_Configuration"]["Day-of-month"]
                Month=jsonrequest["Schedule_Configuration"]["Month"]
                Day_of_week=jsonrequest["Schedule_Configuration"]["Day-of-week"]
                Year=jsonrequest["Schedule_Configuration"]["Year"]
                ScheduleExpression="cron({} {} {} {} {} {})".format(minutes,hours,Day_of_month,Month,Day_of_week,Year)
                print(ScheduleExpression)
                if(jsonrequest['Schedule_State']=='STOP'):
                    FunctionName="stopInstance"
                if(jsonrequest['Schedule_State']=='START'):
                    FunctionName="startInstance"

                rule = client.put_rule(
                    Name=jsonrequest["Instance_Identifier"],
                    ScheduleExpression=ScheduleExpression,
                    State="ENABLED",
                    RoleArn="iamrole"
                )
                aws_response=client.put_targets(
                    Rule=rule_id,
                    Targets=[
                        {
                            "Id": "MyTargetId",
                            "Arn": FunctionName,
                            "Input": json.dumps({"ec2id":jsonrequest["Instance_Identifier"] })
                        }
                    ]
                )
                lambda_client.add_permission(
                    FunctionName=FunctionName,
                    StatementId="IUseTheSameHereAsTheRuleIdButYouDoAsYouPlease",
                    Action="lambda:InvokeFunction",
                    Principal="events.amazon.com",
                    SourceArn=rule["RuleArn"]
                )
            if(jsonrequest['Event_Type']=="DELETE"):
                aws_response = client.delete_rule( Name=jsonrequest["Instance_Identifier"])
            if(jsonrequest['Event_Type']=="FETCH"):
                aws_response = client.list_rules(
                NamePrefix=jsonrequest["Instance_Identifier"],
                NextToken='',
                Limit=123
                )    

        response_data['status']='OK'
        response_data['message']=aws_response 
        response= JsonResponse(response_data)
    except Exception as e:
        print(e)
        response_data['status']='ERROR'
        response_data['message']=aws_response
        response= JsonResponse(response_data)  
    return response      

