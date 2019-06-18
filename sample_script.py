'''
Requirement:

    Select Campaign XXX
    Go to Campaign XXX Settings
    Check for Location Targeting
    Select Location from Excel Sheet
    Update Excluded Location from Excel Sheet
    Save Campaign Setting

    Do the above and then
    Select adgroup
    enable it if paused
    pause it 1 of 3 and then 3 of 3 conditions are met.
'''

import pandas as pd
from googleads import adwords

CAMPAIGN_ID = input('Enter Campaign ID: ')
LOCATION = input('Enter Location: ')

def get_adgroups_report(client):
    # Initialize appropriate service.
    report_downloader = client.GetReportDownloader(version='v201809')

    # Create report query.
    report_query = (adwords.ReportQueryBuilder()
                    .Select('AdGroupId', 'CampaignId',
                            'AdGroupName', 'AdGroupStatus',
                            'Impressions', 'Clicks',
                            'Cost')
                    .From('ADGROUP_PERFORMANCE_REPORT')
                    .Where('AdGroupStatus').In('ENABLED', 'PAUSED')
                    .During('LAST_7_DAYS')
                    .Build())

    # You can provide a file object to write the output to. For this
    #
    file_name = 'data.csv'
    file = open(file_name, 'w+')
    report_downloader.DownloadReportWithAwql(
        report_query, 'CSV', file, skip_report_header=True,
        skip_column_header=False, skip_report_summary=True,
        include_zero_impressions=True)
    return file_name

def pause_adgroup(client, ad_group_id):
  # Initialize appropriate service.
  ad_group_service = client.GetService('AdGroupService', version='v201809')

  # Construct operations and update an ad group.
  operations = [{
      'operator': 'SET',
      'operand': {
          'id': ad_group_id,
          'status': 'PAUSED'
      }
  }]

  adgroups = ad_group_service.mutate(operations)

  # Display results.
  for adgroup in adgroups['value']:
      print('Ad Group with name "%s" and id "%s" was paused.'
            % (adgroup['name'], adgroup['id']))


def enable_adgroup(client, ad_group_id):
  # Initialize appropriate service.
  ad_group_service = client.GetService('AdGroupService', version='v201809')

  # Construct operations and update campaign.
  operations = [{
      'operator': 'SET',
      'operand': {
          'id': ad_group_id,
          'status': 'ENABLED'
      }
  }]
  adgroups = ad_group_service.mutate(operations)

  # Display results.
  for adgroup in adgroups['value']:
      print('Ad Group with name "%s" and id "%s" was enabled.'
            % (adgroup['name'], adgroup['id']))

def add_negative_campaign_criterion(client, campaign_id, location):

  # Check for location in geotargets file and extract Criterion Id
  df = pd.read_csv('geotargets.csv')

  index = df.index[df['Name']==location].tolist()[0]

  location_id = df['Criteria ID'][index]

  # Initialize appropriate service
  campaign_criterion_service = client.GetService(
      'CampaignCriterionService', version='v201809')


  # Create a negative campaign criterion operation.
  negative_campaign_criterion_operand = {
      'xsi_type': 'NegativeCampaignCriterion',
      'campaignId': campaign_id,
      'criterion': {
          'xsi_type': 'Location',
          'id': location_id
      }
  }
  # Add the negative campaign criterion.
  operations = []
  operations.append({
      'operator': 'ADD',
      'operand': negative_campaign_criterion_operand
  })

  # Make the mutate request.
  result = campaign_criterion_service.mutate(operations)

  # Display the resulting campaign criteria.
  for campaign_criterion in result['value']:
    print('Campaign criterion with campaign id "%s", criterion id "%s", '
          'and type "%s" was added.\n'
          % (campaign_criterion['campaignId'],
              campaign_criterion['criterion']['id'],
              campaign_criterion['criterion']['type']))

def main(client, campaign_id,location):
    add_negative_campaign_criterion(client, campaign_id, location)

    file = get_adgroups_report(client)

    df = pd.read_csv(file)

    for i in range(len(df)):
        if df['Campaign ID'][i] == campaign_id and df['Ad group state'][i] == 'paused':
            enable_adgroup(client, df['Ad group ID'][i])

            if df['Impressions'][i] < 10 or df['Clicks'][i] < 10 or df['Cost'][i]:
                pause_adgroup(client,df['Ad group ID'][i])
            elif df['Impressions'][i] < 10 and df['Clicks'][i] < 10 and df['Cost'][i]:
                pause_adgroup(client, df['Ad group ID'][i])

if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client,CAMPAIGN_ID,LOCATION)
