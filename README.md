# AWS_instSchedular
REQUEST 1:CREATE SCHEDULE FORMAT: JSON

{ "Instance_Identifier":"i-1233232278", // "Event_Type":"ADD", //<ADD|UPDATE|DELETE|FETCH> "Schedule_State":"STOP", //<STOP|START> "Schedule_Configuration":{ "Hours":"18",
"Minutes":"0", "Day-of-month":"?", "Month":"", "Day-of-week":"MON-FRI", "Year":"" } }

The above request will add a rule of schedule type cron for the instance specified
