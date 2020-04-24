import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
import datetime
from datetime import date
import pandas as pd
import pandas as pd2
from datetime import datetime

# headless
display = Display(visible=0,size=(800, 600))
display.start()

browser = webdriver.Chrome()

# you need to update this with your own trendweight URL - this is mine
browser.get("https://trendweight.com/u/91a151bdce4143/")
#take a breathe allowing JavaScript to load
time.sleep(2)
soup = BeautifulSoup(browser.page_source, "html.parser")

todays_weight = soup.findAll('td', attrs={'class':'measuredWeight'})[0].string
weight_today = float(todays_weight)

todayz_date = str(date.today())

#open master spreadsheet and append today's weight to the bottom.
#I included a sample of my weight chart to get you started
df = pd.read_excel("weight_chart.xlsx")
df2 = pd.DataFrame({"weigh_in_date":[todayz_date], "weight":[weight_today]}) 
df = df.append(df2)

#more cleanup to remove dups
df.drop_duplicates(inplace=True)

#Save the updated sheet.
df.to_excel('weight_chart.xlsx',index=False)
df3 = pd2.read_excel("weight_chart.xlsx")

df3['Percentile_rank']=df3.weight.rank(pct=True)

#establish the index for our new weight
#x = 2
x = (len(df3))-1
#print("value of x is: ")
#print(int(x))
#print(df.weight[x])
#print(df.Percentile_rank[int(x)])


import boto3
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "My Future Self <kylepott@gmail.com>"

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT = "kylepott@gmail.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the 
# ConfigurationSetName=CONFIGURATION_SET argument below.
#CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-1"

# The subject line for the email.
SUBJECT = ""

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ""

weight_up_or_down = df3.weight[int(x)] - df3.weight[int(x) -1]

#173 is my goal
how_much_to_go = df3.weight[int(x)] - 173.
# The HTML body of the email.
if weight_up_or_down < 0:
    enouragement = " Way to go, your weight is less than yesterday by " + str(round((weight_up_or_down),2)) + " pounds."
else:
    enouragement = " Get back at it, you can do it! Your weight was not less than yesterday. You went up " + str(round((weight_up_or_down),2)) + " pounds."

BODY_HTML = "<html><head></head><body><p>Today you weigh " + str(round((df3.weight[int(x)]),2)) + " which is in the " + str(round((df3.Percentile_rank[int(x)]),2)) + " percentile." + enouragement + " Keep going! Only " + str(round((how_much_to_go),2)) + " pounds left to go to your goal!</p></body></html>"

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

# Try to send the email.
try:
    #Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        #ConfigurationSetName=CONFIGURATION_SET,
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])

