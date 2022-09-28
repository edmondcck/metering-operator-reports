import datetime
from dateutil.tz import gettz
import subprocess
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import csv
from io import StringIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


#----------------------------------------#
# Function to get metering report
#----------------------------------------#
def getMeteringCsvReport(name):
  # Set common request parameters
  getReportURL = 'https://metering-openshift-metering.apps.cluster1.example.com/api/v1/reports/get'
  reqHeaders = {'Authorization': 'Bearer ' + token}

  reportName = name
  query = {'name': reportName, 'namespace': 'openshift-metering', 'format': 'csv'}
  response = session.get(getReportURL, headers=reqHeaders, params=query)
  return response.text

#----------------------#
# Global Configuration
#----------------------#

# Get the last Friday
today = datetime.date.today()
weekdaynum = today.weekday() + 3  # weekdaynum is 3 - 9 for Mon - Sun
daydelta = weekdaynum % 7
if daydelta == 0:
  daydelta = 7
lastFriday = today - datetime.timedelta(days=daydelta)

# Set Local Timezone
localzone = 'Asia/Hong_Kong'

# Requests module setting
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()
session.verify = False

# SMTP setting
smtpHost="<smtp.example.com>"
emailFrom="<openshift-report@example.com>"
emailTo=("receiver1@example.com", "receiver2@example.com", "receiver3@example.com", )
emailSubject="Red Hat OCP Hourly Usage Report [Week " + lastFriday.strftime('%Y-%m-%d') + "]"

# Set API Token
token = '<API Token of Service Account reporting-operator in the namespace openshift-metering>'

# Initialise the combined data object
combinedReport = {}

#------------------------------------------------------------------#
# Get data from the weekly report, then translate timezone to local
#------------------------------------------------------------------#
weeklyReport = getMeteringCsvReport('cluster-usage-hourly-' + lastFriday.strftime('%Y%m%d'))

lines = weeklyReport.splitlines()
reader = csv.reader(lines, delimiter=',')

virtualFile = StringIO()
writer = csv.writer(virtualFile)

for i, row in enumerate(reader):
  if i == 0:
    writer.writerow(row)
  else:
    period_start = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S %z %Z').astimezone(gettz(localzone)).strftime('%Y-%m-%d %H:%M:%S %z')
    period_end = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S %z %Z').astimezone(gettz(localzone)).strftime('%Y-%m-%d %H:%M:%S %z')
    row[0] = period_start
    row[1] = period_end
    writer.writerow(row)

contents = virtualFile.getvalue()

#----------------------#
# Send email with CSV file
#----------------------#
msg = MIMEMultipart()
msg['From'] = emailFrom
msg['To'] = ', '.join(emailTo)
msg['Subject'] = emailSubject

emailContent="Dear Sir / Madam,\n\nPlease find the Red Hat OpenShift weekly cluster usage report attached.\n\n"
msg.attach(MIMEText(emailContent))

csvFilename = 'openshift_cluster_usage_report_' + lastFriday.strftime('%Y%m%d') + '.csv'
part = MIMEBase('application', "octet-stream")
part.set_payload(contents)
encoders.encode_base64(part)
part.add_header('Content-Disposition',
                'attachment; filename="{}"'.format(csvFilename))
msg.attach(part)

with smtplib.SMTP(smtpHost, port='25') as smtp_server:
  smtp_server.ehlo()
  smtp_server.send_message(msg)
  smtp_server.quit()

