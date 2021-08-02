from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import boto3
import json
import logging

client = boto3.client('events')
lambda_client = boto3.client('lambda')
logger = logging.getLogger(__name__)

@csrf_exempt
def scheduleAwsInstance(request):
    response = HttpResponse()
    response_data = {}
    response_data['status']='ERROR'
    aws_response={}
    response= JsonResponse(response_data)
    jsonrequest=json.loads(request.body)
    logger.info("Schedule Request Received",str(jsonrequest))   
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
        logger.info("Schedule Request Response",str(response)) 
    except Exception as e:
        print(e)
        response_data['status']='ERROR'
        response_data['message']=aws_response
        response= JsonResponse(response_data)
        logger.info("Schedule Request Error Response",str(response))   
    return response      

