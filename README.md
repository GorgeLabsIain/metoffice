# metoffice

1. Retrieve observation sitelist from MetOffice DataPoint API
2. Find nearest 3 observation sites, and distances to each
3. Connect to Eleksen
4. Repeat hourly:
    a. Read temperature from each of the 3 sites
    b. Calculate weighted average, to approximate local temperature
    c. Write the weighted average into Eleksen
    