from googleads import adwords


PAGE_SIZE = 100


def main(client):
  # Initialize appropriate service.
  campaign_service = client.GetService('CampaignService', version='v201809')

  # Construct selector and get all campaigns.
  offset = 0
  selector = {
      'fields': ['Id', 'Name', 'Status'],
      'paging': {
          'startIndex': str(offset),
          'numberResults': str(PAGE_SIZE)
      }
  }

  more_pages = True
  while more_pages:
    page = campaign_service.get(selector)

    # Display results.
    if 'entries' in page:
      for campaign in page['entries']:
        print('Campaign with id "%s", name "%s", and status "%s" was '
              'found.' % (campaign['id'], campaign['name'],
                          campaign['status']))
    else:
      print('No campaigns were found.')
    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])


if __name__ == '__main__':
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  main(adwords_client)