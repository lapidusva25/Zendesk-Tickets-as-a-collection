import requests
import pandas as pd
from urllib.parse import urlencode
import json
from StoredData import getFile
from s3ops import FileOutput,GetS3File



def getTickets(domain,params,zendesk_headers,AWS_key,AWS_secret,bucket,binding_key):
  dfRequesters = getFile('Zendesk/requesters_zendesk_support_file.csv',AWS_key,AWS_secret,bucket).copy(deep=True)
  dfOrgs = getFile('Zendesk/orgs_zendesk_support_file.csv',AWS_key,AWS_secret,bucket).copy(deep=True)
  payload={}
  dfTickets = pd.DataFrame(columns = ['TicketID','AccountID','Subject','Priority','Status','Creator','URL','Create Date','Last Update Date'],dtype=str)
  dfTickets = dfTickets.set_index('TicketID')
  nextpage = 'https://'+domain+'.zendesk.com/api/v2/search.json?' + urlencode(params)
  while nextpage:
    #print(nextpage)
    response = requests.request("GET", nextpage, headers=zendesk_headers, data=payload)
    resp = json.loads(response.text)

    nextpage = resp['next_page']
    
    for ticket_index, ticket in enumerate(resp['results']):

      ticket_num=ticket['id']

      if str(ticket['organization_id']) in dfOrgs.index:
        dfTickets.at[ticket_num,'AccountID']=dfOrgs.at[str(ticket['organization_id']),'translation']
        #print('I found org in the file and used it from there')
      elif(ticket['organization_id']):
        #print('I didnt find org in the file and had to fetch it')
        
        orgURL = 'https://'+domain+'.zendesk.com/api/v2/organizations/'+str(ticket['organization_id'])
        
        response = requests.request("GET", orgURL, headers=zendesk_headers, data=payload)
        resp = json.loads(response.text)
        temp_org_id = None
        
        if binding_key in resp['organization'].keys():
          temp_org_id=resp['organization'][binding_key]
        elif binding_key in resp['organization']['organization_fields'].keys():
          temp_org_id=resp['organization']['organization_fields'][binding_key]


        dfTickets.at[ticket_num,'AccountID'] = temp_org_id
        dfOrgs.at[str(ticket['organization_id']),'translation']=temp_org_id
      dfTickets.at[ticket_num,'Subject']=ticket['subject']
      dfTickets.at[ticket_num,'Priority']=ticket['priority']
      dfTickets.at[ticket_num,'Status']=ticket['status']

      if str(ticket['requester_id']) in dfRequesters.index:
        
        dfTickets.at[ticket_num,'Creator']=dfRequesters.at[str(ticket['requester_id']),'translation']

      else:
        userURL = 'https://'+domain+'.zendesk.com/api/v2/users/'+str(ticket['requester_id'])+'/identities'
        response = requests.request("GET", userURL, headers=zendesk_headers, data=payload)
        resp = json.loads(response.text)
        dfTickets.at[ticket_num,'Creator']=resp['identities'][0]['value']
        dfRequesters.at[ticket['requester_id'],'translation']=resp['identities'][0]['value']
      
      dfTickets.at[ticket_num,'URL'] = ticket['url'][:ticket['url'].index('.zendesk.com/')] + '.zendesk.com/agent/tickets/' + str(ticket['id'])
      dfTickets.at[ticket_num,'Create Date']=ticket['created_at']
      dfTickets.at[ticket_num,'Last Update Date']=ticket['updated_at']
  FileOutput(dfRequesters,'Zendesk/requesters_zendesk_support_file.csv',AWS_key,AWS_secret,bucket,True)
  FileOutput(dfOrgs,'Zendesk/orgs_zendesk_support_file.csv',AWS_key,AWS_secret,bucket,True)
  return dfTickets