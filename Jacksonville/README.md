# Jacksonville analysis for March 27, 2024 DD

<h3>Data from CL:</h3>

<strong>869,252 rows & 7 columns</strong>

Listing counts, office names, office ids, average price per sq. ft., avg. derived days on market, and avg. sales price: list price ratio for Jacksonville, Florida from 2019 through 2023 grouped by year, geography and listing office id. Geography consists of three bins: Jacksonville, the rest of Florida (Florida minus Jacksonville), and the rest of the U.S. (U.S. minus Florida).

Data compiled by CL from <a href="https://discovery.corelogic.com/exchange/products/hKh1jSjJTwCvgbw5f4tOww">this dataset</a>. Shared in <a href="https://discovery.corelogic.com/collection">this collection</a>.

<h3>Data wrangling:</h3>

Discovered error in CL price per sq. ft. data. Values were extremely high and volatile (max of >$11M, Keller Williams at ~$4K in 2022 and $223 in 2023). Notified CL of error and was told they would work on it; did not receive any corrected data. Avg. PPSF not used in article.

Standardized office names (all caps, no punctuation, no trailing spaces). Standardized name of common brokerages like RE/MAX, Redfin, Berkshire Hathaway, eXp, Compass, etc. 

Standardized names of brokerages that were common in Jacksonville lik Florida Homes Realty and Engel & Volkers. Standardized names of offices affiliated with "DJ & Lindsey."

Removed data linked to "NON MLS" office name.

After review, realized that EXIT Real Estate Gallery was acquired by United Real Estate in late 2022, and "United Real Estate" was being used as office name for office IDs that were affiliated with EXIT in years prior to United Real Estate's acquisition. Changed the office name for these office IDs from United Real Estate to EXIT Real Estate Gallery in for rows with listing years prior to 2023.

