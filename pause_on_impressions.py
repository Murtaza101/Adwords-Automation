import sys
from googleads import adwords
import pandas as pd
import csv

def pause_campaign(client, campaign_id):
  # Initialize appropriate service.
  campaign_service = client.GetService('CampaignService', version='v201809')

  # Construct operations and update campaign.
  operations = [{
      'operator': 'SET',
      'operand': {
          'id': campaign_id,
          'status': 'PAUSED'
      }
  }]
  campaigns = campaign_service.mutate(operations)

  # Display results.
  for campaign in campaigns['value']:
    print ('Campaign with name "%s" and id "%s" was updated.'
           % (campaign['name'], campaign['id']))

def main(client):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201809')

  # Create report query.
  report_query = (adwords.ReportQueryBuilder()
                  .Select('CampaignId', 'AdGroupId', 'Id', 'Criteria',
                          'CriteriaType', 'FinalUrls', 'Impressions', 'Clicks',
                          'Cost')
                  .From('CRITERIA_PERFORMANCE_REPORT')
                  .Where('Status').In('ENABLED', 'PAUSED')
                  .During('LAST_7_DAYS')
                  .Build())

  # You can provide a file object to write the output to. For this
  #
  file = open('data.csv', 'w+')
  report_downloader.DownloadReportWithAwql(
      report_query, 'CSV', file, skip_report_header=True,
      skip_column_header=False, skip_report_summary=True,
      include_zero_impressions=True)
  file = open('data.csv', 'r')
  data = pd.read_csv(file)

  for i in range(len(data)):
      if data['Impressions'][i] < 10:
          pause_campaign(client,data['Campaign ID'][i])

if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client)