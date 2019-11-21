# geoLocBusiness

## Introduction
The aim of this project is finding the optimal location for a new company. The perfect location should meet the following requirements:

- Designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company have at least 1 child.
- Developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Executives like Starbucks A LOT. Ensure there's a starbucks not to far.
- Account managers need to travel a lot
- All people in the company have between 25 and 40 years, give them some place to go to party.
- Nobody in the company likes to have companies with more than 10 years in a radius of 2 KM.
- The CEO is Vegan

## Methodology

The first input is a database downloaded from crunchbase.com and imported into Compass MongoDB. It was cleaned using pandas in `clean.py` file (deadpooled companies were removed as well as companies with null coordinates). Also, during cleaning, offices were unwinded and classified into Tech and Other companies. Finally, rased money column was cleaned.

After that, airports and Starbucks were treated in `airports.py` and `starbucks.py`. Airports input was a geoDataFrame (geopandas needed). For both databases, a geoJSON column was created for further input in MongoDB.

Then, old companies and tech companies that raised >$1m were filtered in `oldCos.py` and `techCos.py` respectively.

The previous four python scripts generated .json files that were imported in Compass as collections.

In `filtering_distances.py, the first cleaned dataframe was subsequently filtered:

- First, for each company in the dataframe, a query was made to call the closest airport in a radius of 30 km.
- Then, the same was done with old companies (300m instead of the 2km requested at the beggining). This decission was made because I considered more important being close to tech companies than being far from old companies. Then, remaining companies are at least 300m far from old companies.
- After that, a similar query was made with Starbucks, requesting the closest Starbucks within a km.
- Finally, the same was made requesting Tech companies with more than $1m raised, closer than 1km.

With that filter, a ranking was made showing how many tech companies 


