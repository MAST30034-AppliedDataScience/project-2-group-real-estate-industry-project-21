import pandas as pd
import os 

dfv = pd.read_csv('../data/landing/australian_postcodes.csv', usecols=['locality', 'postcode', 'state'])

filter1 = dfv[dfv['postcode'].between(3000, 3211)]
filter2 = dfv[dfv['postcode'].between(3335, 3336)]
filter3 = dfv[dfv['postcode'].between(3754, 3755)]
filter4 = dfv[dfv['postcode'].between(3781, 3787)]
filter5 = dfv[dfv['postcode'].between(3788, 3815)]
filter6 = dfv[dfv['postcode'].between(3926, 3944)]
filter7 = dfv[dfv['postcode'].between(3910, 3920)]
filter8 = dfv[dfv['postcode'].between(3975, 3978)]
filter9 = dfv[dfv['postcode'].between(3427, 3429)]
filter10 = dfv[dfv['postcode'].between(3750, 3752)]
filter11 = dfv[dfv['postcode'].between(3754, 3755)]
filter12 = dfv[dfv['postcode'].between(3759, 3761)]
filter13 = dfv[dfv['postcode'].between(3765, 3775)]
filter14 = dfv[dfv['postcode'].isin([3338,3980])]

dfm = pd.concat([filter1, filter2,filter3,filter4,filter5,filter6,filter7,filter8,filter9,filter10,filter11,filter12,filter13,filter14], ignore_index=True)

dfm = dfm.drop_duplicates(subset='postcode', keep='first')

dfm.to_csv('../data/raw/Mel_Metro_Postcodes.csv', index=False)

