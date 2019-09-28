class BasicData:
    def __init__(self):

        self.country_abbr_dict = {
            ' California': 'CA',
            ' Texas': 'TX',
            ' Nebraska': 'NE',
            ' Vermont': 'VT',
            ' National Benefits Center': 'NBC',
        }

    def get_country_abbr(self, full_country):
        if full_country in self.country_abbr_dict:
            return self.country_abbr_dict[full_country]
        else:
            return 'OTHERS'

