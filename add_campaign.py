import uuid
from googleads import adwords


CAMPAIGN_ID = '2030792152'


def main(client, campaign_id):
  # Initialize appropriate service.
  ad_group_service = client.GetService('AdGroupService', version='v201809')

  # Construct operations and add ad groups.
  operations = [{
      'operator': 'ADD',
      'operand': {
          'campaignId': campaign_id,
          'name': 'Earth to Mars Cruises #%s' % uuid.uuid4(),
          'status': 'ENABLED',
          'biddingStrategyConfiguration': {
              'bids': [
                  {
                      'xsi_type': 'CpcBid',
                      'bid': {
                          'microAmount': '1000000'
                      },
                  }
              ]
          },
          'settings': [
              {
                  # Targeting restriction settings. Depending on the
                  # criterionTypeGroup value, most TargetingSettingDetail only
                  # affect Display campaigns. However, the
                  # USER_INTEREST_AND_LIST value works for RLSA campaigns -
                  # Search campaigns targeting using a remarketing list.
                  'xsi_type': 'TargetingSetting',
                  'details': [
                      # Restricting to serve ads that match your ad group
                      # placements. This is equivalent to choosing
                      # "Target and bid" in the UI.
                      {
                          'xsi_type': 'TargetingSettingDetail',
                          'criterionTypeGroup': 'PLACEMENT',
                          'targetAll': 'false',
                      },
                      # Using your ad group verticals only for bidding. This is
                      # equivalent to choosing "Bid only" in the UI.
                      {
                          'xsi_type': 'TargetingSettingDetail',
                          'criterionTypeGroup': 'VERTICAL',
                          'targetAll': 'true',
                      },
                  ]
              }
          ]
      }
  }, {
      'operator': 'ADD',
      'operand': {
          'campaignId': campaign_id,
          'name': 'Earth to Venus Cruises #%s' % uuid.uuid4(),
          'status': 'ENABLED',
          'biddingStrategyConfiguration': {
              'bids': [
                  {
                      'xsi_type': 'CpcBid',
                      'bid': {
                          'microAmount': '1000000'
                      }
                  }
              ]
          }
      }
  }]
  ad_groups = ad_group_service.mutate(operations)

  # Display results.
  for ad_group in ad_groups['value']:
    print ('Ad group with name "%s" and id "%s" was added.'
           % (ad_group['name'], ad_group['id']))


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client, CAMPAIGN_ID)