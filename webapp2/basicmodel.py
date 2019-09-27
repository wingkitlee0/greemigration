class BasicModel:
    def __init__(self):
        self.category_list = [
            'EB1',
            'EB2',
            'EB2-NIW',
            'EB3',
        ]

        self.center_dict = {
             'National Benefit Center': 'NBC',
             'California': 'CA',
             'Nebraska': 'NE',
             'Texas': 'TX',
             'Vermont': 'VT',
             'OTHER': 'OTHER'
        }
        self.center_list = [k for k in self.center_dict]

        self.columns = ['RFE', 'START2', 'COUNTRY2_India', 'COUNTRY2_Mexico', 'COUNTRY2_ROW',
            'CAT_EB2', 'CAT_EB2-NIW', 'CAT_EB3']

        self.country_dict = {
            'CN': 'China',
            'MX': 'Mexico',
            'IN': 'India',
        }