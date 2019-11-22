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

In `filtering_distances.py`, the first cleaned dataframe was subsequently filtered:

- First, for each company in the dataframe, a query was made to call the closest airport in a radius of 30 km.
- Then, the same was done with old companies (300m instead of the 2km requested at the beggining). This decission was made because I considered more important being close to tech companies than being far from old companies. Then, remaining companies are at least 300m far from old companies.
- After that, a similar query was made with Starbucks, requesting the closest Starbucks within a km.
- Finally, the same was made requesting Tech companies with more than $1m raised, closer than 1km.

With that filter, a ranking was made showing how many tech companies were located in each city. The result was the following:

![alt text](https://raw.githubusercontent.com/jlmingo/geoLocBusiness/project-mongo/input/img/techCos.png)

I checked the rental prices for these cities having the following result:

![alt text](https://raw.githubusercontent.com/jlmingo/geoLocBusiness/project-mongo/input/img/rentals.png)

Apparently Austin, Texas is a nice place to locate a tech business and it accomplishes some of the conditions: nearby Airport, Starbucks, tech companies around and free from old-companies around.

![alt text](https://raw.githubusercontent.com/jlmingo/geoLocBusiness/project-mongo/input/img/austinTX.png)

A paralell analysis was made. Starting from the filtered dataframe (that is, nearby airport, nearby tech companies, nearby Starbucks and far from old companies), I deployed a heatmap based on how many thec companies are there around, together with a cluster indicator that shows how many possible locations are in a certain area. For instance, we see 217 possible locations in East coast, while 140 in the West coast.

![alt text](https://raw.githubusercontent.com/jlmingo/geoLocBusiness/project-mongo/input/img/worldwide.png)

## Execution of program

`main.` should be executed to generate both maps in html, that can be shown in a web browser.

## Possible improvements

It would be useful to implement a function that, based on a previous analysis of market cluster and heatmap, shows all starbucks, airports etc of the selected city. 

Also, schools, party places and vegan restaurants could be implemented.