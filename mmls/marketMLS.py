import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format

# Referenced later by _subtablesMetro method
# Do NOT region-specific names to list
common_brokerage_names = [
    ### note the spaces after REDFIN and EXP
    'COLDWELL BANKER', 'CENTURY 21', 'REDFIN ', 
    'KELLER WILLIAMS', 'EXP ', 'HOMESMART', 
    'COMPASS', 'RE/MAX', 'BERKSHIRE HATHAWAY', 
    'OPENDOOR', 'OFFERPAD', 'ZILLOW'
]

class MarketMLS:
    def __init__(self, csv_path, metro_name):
        self.metro_name = metro_name
        self._raw = pd.read_csv(csv_path)
        self._years = self._raw.listing_year.unique()
        print('Data imported')
        self._cleanData()
        print('Data cleaned')
        self._subtablesAll()
        print('Data grouped')

    def _cleanData(self):
        self.df = self._raw.copy()
        # handle missing office names
        # make office names all caps
        self.df.listing_office_name.fillna('', inplace=True)
        self.df['listing_office_name'] = self.df.listing_office_name.str.upper()\
                                            .str.rstrip()\
                                            .str.replace('.','')\
                                            .str.replace(',','')\
                                            .str.replace("'",'')\
                                            .str.replace('LLC', '')\
                                            .str.replace('INC', '')
        self.df['listing_office_name'] = self.df.listing_office_name.str.strip()
        ### SPECIAL: clean SOTHEBY'S INTERNATIONAL REALTY
        self.df['listing_office_name'] = [x if 'SOTHEBY' not in x 
                                          else 'SOTHEBY\'S INTERNATIONAL REALTY'
                                          for x in self.df.listing_office_name]
        ### SPECIAL: clean SOTHEBY'S INTERNATIONAL REALTY
        self.df['listing_office_name'] = [x if 'REMAX' not in x 
                                          else 'RE/MAX' 
                                          for x in self.df.listing_office_name]

    def _subtablesAll(self):
        # Group by geo and year
        # Reshape table
        grouped = self.df.groupby(['listing_year', 'geographic'])\
                        .agg({
                            'listing_office_name':'nunique',
                            'listing_office_id':'nunique',
                            'total_listings':'sum',
                            'avg_price_per_square_foot':'mean',
                            'avg_derived_days_on_market':'mean',
                            'avg_sales_price_to_list_price_ratio':'mean'
                        })
        grouped.rename(columns={'listing_office_name':'unique_cos',
                                     'listing_office_id':'unique_offices'},
                            inplace=True)
        grouped.reset_index(inplace=True)
        self.summary = grouped.reset_index().pivot(
                            columns='geographic',
                            index='listing_year',
                            values=[
                                'unique_cos',
                                'unique_offices',
                                'total_listings',
                                'avg_price_per_square_foot',
                                'avg_derived_days_on_market',
                                'avg_sales_price_to_list_price_ratio'
                            ])
        self.gridOfLines = pd.DataFrame(self.summary.unstack()).reset_index()\
            .rename(columns={'level_0':'category', 0:'values'})\
            .pivot(index=['category','listing_year'], columns='geographic', 
                   values='values')\
            .reset_index()
        new_names = {
            'avg_derived_days_on_market':'Avg. Days on Market',
            'avg_price_per_square_foot':'Avg. Price per Sq. Ft. ($)',
            'avg_sales_price_to_list_price_ratio':'Avg. Sales Price/List Price Ratio',
            'total_listings':'Listings',
            'unique_cos':'Companies',
            'unique_offices':'Offices'
        }
        self.gridOfLines['category'] = [new_names[x] for x in self.gridOfLines.category]
        self.gridOfLines.rename(columns={'category':'group', 'listing_year':'Listing Year'},
                                inplace=True)
        self.gridOfLines.columns.rename(None, inplace=True)      
    
    def companiesTable(self, regionalBrokers=[]):
        # limit operations to metro's data
        metro = self.df.copy().loc[self.df.geographic==self.metro_name]
        # standardize company names into new column
        def changeName(old_name, regionalBrokers=regionalBrokers):
            brokerage_names = common_brokerage_names + regionalBrokers
            for name in brokerage_names:
                if old_name.startswith(name):
                    return name.rstrip()
            return old_name 
        self.cos = metro.listing_office_name.value_counts().index.to_list()
        metro['listing_office_group'] = metro.listing_office_name.apply(lambda x: changeName(x))
        # get annual listings market share % column to sum in groupby agg
        listings_by_year = metro[['listing_year', 'total_listings']].groupby('listing_year').sum()
        metro['annual_listings'] = None
        for year in metro.listing_year.unique(): 
            metro.loc[metro.listing_year==year, 'annual_listings'] = listings_by_year.loc[year].sum()
        metro['perc_listings'] = metro.total_listings / metro.annual_listings * 100
        # grouped by year and company
        ByCo = metro.groupby(['listing_year', 'listing_office_group'])\
                        .agg({
                            'listing_office_name':'nunique',
                            'listing_office_id':'nunique',
                            'total_listings':'sum',
                            'avg_price_per_square_foot':'mean',
                            'avg_derived_days_on_market':'mean',
                            'avg_sales_price_to_list_price_ratio':'mean',
                            'perc_listings': 'sum'
                        })
        ByCo.rename(columns={'listing_office_name':'unique_cos',
                             'listing_office_id':'unique_offices'},
                            inplace=True)                          
        ByCo = pd.pivot_table(ByCo.reset_index(),
                                      columns='listing_year',
                                      index='listing_office_group',
                                      values=[
                                          'unique_cos',
                                          'unique_offices',
                                          'total_listings',
                                          'avg_price_per_square_foot',
                                          'avg_derived_days_on_market',
                                          'avg_sales_price_to_list_price_ratio',
                                          'perc_listings'
                                      ])
        # return companies that have been in top 100 in at least one year
        top_cos = []
        sorters = [('total_listings', year) for year in self._years]
        for sorter in sorters:
            cos = ByCo.sort_values(by=sorter, ascending=False).head(100).index
            for co in cos:
                if co not in top_cos:
                    top_cos.append(co)
        ByCo.sort_values(by=sorters, ascending=False, inplace=True)
        return ByCo.loc[ByCo.index.isin(top_cos)]
    
    def officesTable(self):
        # limit operations to metro's data
        # drop non mls
        metro = self.df.copy().loc[(self.df.geographic==self.metro_name)&(self.df.listing_office_name!='NON MLS'), 
                                    ['listing_year', 'listing_office_id', 'total_listings']]
        # get listings by year and office id
        metro = metro.groupby(['listing_year', 'listing_office_id']).sum().reset_index()
        # order by total_listings each year
        metro.sort_values(by=['listing_year', 'total_listings'], 
                              ascending=[True, False], 
                              inplace=True)
        # bin by total_listings per year
        metro = metro.groupby('listing_year').apply(
                    lambda grouped: grouped.assign(
                        listings_rank=lambda grouped: grouped.total_listings.rank(ascending=False)
                    )
                )
        metro['listings_bin'] = ['Top 10' if x < 11 else
                                '11-100' if x < 101 else 
                                '101-500' if x < 501 else 
                                '501+' for x in metro.listings_rank]
        metro.reset_index(inplace=True, drop=True)
        metro = metro[['listing_year', 'listings_bin', 'total_listings']]\
            .groupby(['listing_year','listings_bin']).sum()\
            .reset_index().pivot(index='listing_year', columns='listings_bin', values='total_listings')\
            .reset_index()
        metro.columns.rename(None, inplace=True)
        return metro[['listing_year', 'Top 10', '11-100', '101-500', '501+']]
    
    def officeBinPercs(self):
        byOffices = self.officesTable()
        byOffices.set_index('listing_year', inplace=True)
        byOffices = byOffices.div(byOffices.sum(axis=1), axis=0) * 100
        byOffices.reset_index(inplace=True)
        byOffices.rename(columns={'listing_year':'Listing Year'}, inplace=True)
        return byOffices

