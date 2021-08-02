# AWS_instSchedular

URL: http://127.0.0.1:8000/schedule
We can create,update,delete,fetch schedules for a given aws instance.

Instance_Identifier:The value is the ec2 instance id
Event_Type:The value can be any one of these(ADD,DELETE,FETCH)
Schedule_State:The value can be any one of these(START,STOP)
Schedule_Configuration:The value needs to have all the details(hours,minutes,day of month,month,day of week,year)you want the instance to be running or stopped.

REQUEST 1:CREATE SCHEDULE FORMAT: JSON

{ "Instance_Identifier":"i-1233232278", 
"Event_Type":"ADD", 
"Schedule_State":"STOP", >
"Schedule_Configuration":
{ 
  "Hours":"18",
  "Minutes":"0",
  "Day-of-month":"?", 
  "Month":"",
  "Day-of-week":"MON-FRI", 
  "Year":""
}
}

The above request will add a rule of schedule type cron for the instance specified
