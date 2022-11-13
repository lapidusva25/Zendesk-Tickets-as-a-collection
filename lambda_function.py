
import pandas as pd
import base64
from s3ops import FileOutput, GetS3File
from tickets import getTickets

zendesk_domain = '<your Zendesk domain>'
AWS_key = '<your aws key>'
AWS_secret = '<your aws secret>'
zendesk_email = '<your zendesk email>'
zendesk_token = '<<your zendesk token>'
zendesk_bindign_key = '<your zendesk binding key>'
AWS_bucket = '<your aws bucket>'

#Auto creates a Zendesk foler in the bucket if it doesn't exist.


def lambda_handler(var1,var2):
  message = zendesk_email + '/token:' + zendesk_token
  message_bytes = message.encode('ascii')
  base64_bytes = base64.b64encode(message_bytes)
  base64_message = 'Basic ' + base64_bytes.decode('ascii')

  zendesk_headers = {
    'Authorization': base64_message
  }
  zendesk_query = {'query':'status<closed'}

  dfTickets = pd.DataFrame()

  dfPreviousPull = pd.DataFrame()
  try:
    dfPreviousPull = GetS3File('Zendesk/tickets.csv',AWS_key,AWS_secret,bucket).copy(deep=True)
    previousfile = True
  except:
    previousfile = False
  dfPreviousPull = GetS3File('Zendesk/tickets.csv',AWS_key,AWS_secret,bucket).copy(deep=True)
  print(dfPreviousPull)
  print(dfPreviousPull['Last Update Date'].max())





  if(previousfile):
    zendesk_query['query'] = zendesk_query['query'] + ' updated>' + dfPreviousPull['Last Update Date'].max()
  print(zendesk_query)
  dfTemp = getTickets(zendesk_domain,zendesk_query,zendesk_headers,AWS_key,AWS_secret,bucket,zendesk_bindign_key)
  dfTickets = dfTickets.append(dfTemp)



  
  FileOutput(dfTickets,'Zendesk/tickets.csv',AWS_key,AWS_secret,bucket, index=True)