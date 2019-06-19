# Pause a campaign based on its number of impressions and if it has a specific keyword in one of its adgroups


import sys
from googleads import adwords
import pandas as pd

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


def convertToDictionary(filename):
    import csv
    data = []
    with open(filename, newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            data.append(row)
        dic = dict()
        print(data[2])
        for i in range(len(data[1])):
            dic[data[1][i]] = [(data[j][i]) for j in range(2,len(data))]
            print(dic)
    return dic

def main(client, keyword):
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
  df = pd.read_csv(file)

  keyword_exists = False

  for i in range(len(df)):
      if df['Impressions'][i] < 10 and df['Keyword / Placement'][i] == keyword:

          # Keyword found
          keyword_exists = True

          # Pause campaign
          pause_campaign(client,df['Campaign ID'][i])

  if not keyword_exists:
      print('The keyword does not exist')


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  keyword = input('Enter the keyword: ')

  main(adwords_client,keyword)
