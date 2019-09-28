import numpy as np 
import datetime
import pandas as pd
from basicdata import BasicData

CATEGORIES = ['COC', 'STATUS', 'DT', 'STARTM', 'CAT', 'START2', 'CEN', 'APP', 'YEAR', 'CON']

class ModelUtil3:
    def __init__(self, columns, presentdate):
        self.columns = columns
        self.presentdate = presentdate

        self.column_dict = { k: i for i, k in enumerate(self.columns)} # { column name: index }
        self.basic = BasicData()

    def cat_mapping(self, cat):
        if cat in [' EB1A', ' EB1B', ' EB1C']:
            return 'EB1'
        else:
            return cat.strip(' ')
    
    def RFE_mapping(self, rfe):
        return 1 if rfe == ' yes' else 0
    
    def country_mapping(self, country):
        return country if country in ['India', 'China', 'Mexico'] else 'ROW'

    def get_center_onehot_column(self, center):
        if center in ['TX', 'NE', 'VT', 'NBC', 'OTHER']:
            


        {'CA': 416,
         'TX': 20701,
         'NE': 18958,
         'VT': 427,
         'NBC': 878,
         'OTHER': 405})

    def get_country2_onehot_column(self, country):
        """
        get the index of the one-hot column for country
        """
        if country == 'China':
            return None
        else:
            abbr = self.country_mapping(country)
            col_name = 'COUNTRY2_{}'.format(abbr)
            return self.column_dict[col_name]


    def get_CAT_onehot_column(self, category):
        """
        get the index of the one-hot column for country
        """
        if category in ['EB2', 'EB2-NIW', 'EB3']:
            col_name = 'CAT_{}'.format(category)
            return self.column_dict[col_name]
        else:
            return None        

    def convert_onehot(self, country, category, has_RFE, start_date):
        """
        Convert user's input into one-hot vector
        """
        assert type(start_date) == datetime.date
        
        index_country = self.get_country2_onehot_column(country)
        index_cat = self.get_CAT_onehot_column(category)
        
        vector = [0] * len(self.columns)
        
        vector[self.column_dict['RFE']] = 1 if has_RFE else 0
        vector[self.column_dict['START2']] = (self.presentdate-start_date).days 
        
        if index_country is not None:
            vector[index_country] = 1
        if index_cat is not None:
            vector[index_cat] = 1
        
        return vector