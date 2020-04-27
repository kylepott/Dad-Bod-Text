# Dad-Bod-Text
This project can be used to send yourself a text message with your daily weight.  

# Dependencies
There are a number of dependencies you'll have to meet to use this project.

Here is what I suggest:
* A Withings wi-fi equipped scale (available on Amazon.com ~$80USD)
* An account at trendweight.com that syncs with your withings scale (free)
* You will have to have an AWS account with your email verified through AWS SES (free)
** I also recommend that you move your AWS SES account out of the sandbox
* You will have to have installed the AWS CLI and configured Boto3 (free)

In the dad_bod_text.py file you will see a number of standard PIP dependencies:
* pandas
* numpy
* requests
* time
* datetime
