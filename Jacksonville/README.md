# Jacksonville analysis for March 27, 2024 DD

<h2>Data from CL:</h2>

<strong>869,252 rows & 7 columns</strong>

Listing counts, office names, office ids, average price per sq. ft., avg. derived days on market, and avg. sales price: list price ratio for Jacksonville, Florida from 2019 through 2023 grouped by year, geography and listing office id. Geography consists of three bins: Jacksonville, the rest of Florida (Florida minus Jacksonville), and the rest of the U.S. (U.S. minus Florida).

Data compiled by CL from <a href="https://discovery.corelogic.com/exchange/products/hKh1jSjJTwCvgbw5f4tOww">this dataset</a>. Shared in <a href="https://discovery.corelogic.com/collection">this collection</a>.

<h2>Data wrangling:</h2>

Discovered error in CL price per sq. ft. data. Values were extremely high and volatile (max of >$11M, Keller Williams at ~$4K in 2022 and $223 in 2023). Notified CL of error and was told they would work on it; did not receive any corrected data. Avg. PPSF not used in article.

Standardized office names (all caps, no punctuation, no trailing spaces). Standardized name of common brokerages like RE/MAX, Redfin, Berkshire Hathaway, eXp, Compass, etc. 

Standardized names of brokerages that were common in Jacksonville lik Florida Homes Realty and Engel & Volkers. Standardized names of offices affiliated with "DJ & Lindsey."

Removed data linked to "NON MLS" office name.

After review, realized that EXIT Real Estate Gallery was acquired by United Real Estate in late 2022, and "United Real Estate" was being used as office name for office IDs that were affiliated with EXIT in years prior to United Real Estate's acquisition. Changed the office name for these office IDs from United Real Estate to EXIT Real Estate Gallery in for rows with listing years prior to 2023.

<h2>Exploratory data analysis and data visualization</h2>

Created office listing group column of company affiliations of each office name. Created market share percentage column of each office listing group's percentage of listings each year.

Created filtered and pivoted tables:
- All stats by geography and listing year
- Jacksonville listing stats by brokerage by year (grouped by company name, all companies that were in the top 100 in any year from 2019 to 2023)
- Jacksonville listing stats by binned rank of office (ranked by # of listings per office ID)
- Stats for iBuyers
- Stats for builders
- Fastest growing brokerages
- Fastest declining brokerages
- Brokerages that did not survive to 2023
- Brokerages that sprung up after 2019

Data visualizations:
- Grid of charts of <a href="https://public.flourish.studio/visualisation/17268498/">all stats by geo</a>
- Grouped hbars by <a href="https://public.flourish.studio/visualisation/17269941/">office rank bins</a>
- Grid of hbars of <a href="https://public.flourish.studio/visualisation/17268433/">2019 vs. 2023 for each geographic bin</a>
- Bar chart race of <a href="https://public.flourish.studio/visualisation/17268383/">top 10 brokerages by listing count each year</a>
- Stacked area chart of <a href="https://public.flourish.studio/visualisation/17300005/">homebuilders' listings</a>
- Stacked area chart of <a href="https://public.flourish.studio/visualisation/17299887/">iBuyers' listings</a>
- Stacked area chart of <a href="https://public.flourish.studio/visualisation/17299595/">fastest-growing brokerages with >= 100 listings in 2023</a>

<h2>Data storytelling</h2>

Wrote <a href="https://public.flourish.studio/visualisation/17299595/">this DD</a>.
