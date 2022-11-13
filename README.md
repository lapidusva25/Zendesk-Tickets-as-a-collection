# Zendesk-Tickets-as-a-collection

## Quick start: 
* Edit the lambda_function.py file and input your own token/api keys
* Setup the Customer Data Hub job within Totango to fetch the file

## Business use cases:
* Give your CSMs a complete viw of all open tickets for a customer.
* Create a play when a urgent priority ticket is created.
* Create a play when a ticket is open longer than 30/60/90 days

## Requirements:
* You are using orgs within Zendesk.
* You have a field on the org in Zendesk which matches to a field within your Totango attributes.
* You have admin rights to Zendesk
* You have admin rights to Totango
* You have an AWS bucket with an AWS_key / AWS_secret
* You have the ability to read and write to this bucket

## Minimizing API calls: 
The code checks to see if the file was previously generated, if it was it grabs the max value of the updated_at date from the previously generated file and uses that in the subsequent query.

## High level functional overview:
This code is meant to run on a recurring basis.
To minimize API calls, because Zendeks doesn't directly reveal the requesters email address/org ID but rather an ID that points to a reference within another table.  The code saves the lookup list of requesters/orgs it has previously interacted with, and creates two support files (org/requesters).
You can then setup a jub in the Customer Data Hub to retrieve the file.

## Support:
Please reach out to support@totango.com with any issues
