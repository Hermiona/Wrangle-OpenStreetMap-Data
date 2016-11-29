# Wrangle OpenStreetMap Data

#### Map Area
Bishkek, Kyrgyzstan

This is map of the city where I was born, so it was interesting to me to see what database querying reveals, and liked the opportunity to contribute to its improvement on OpenStreetMap.org.
Unfortunately, Bishkek wasn't amongst preselected metro areas, so I used MapZen to make custom extract with boudaries 74.5037007989, 42.7787328152, 74.6717525572, 42.9377928738. As extracted area is rectangular, it contains some adjacent to Bishkek areas, so in the following analysis we should keep it in mind. The extract was created on 2016 November 15, at 01:48 AM and could be found [here](https://mapzen.com/data/metro-extracts/your-extracts/14f307f3f854).

## Problems Encountered in the Map

After downloading map of the Bishkek area and running audit functions, I noticed several problems with the data, which I will discuss in the following order:

* Inconsistency in language of street names and types: ```"Tchui Strasse",  "Manas Avenue", "улица Матросова"```
* Over­abbreviated street types with inconsistent position: ```"ул. Масыралиева”, "Асанбай мкр.", "Kiev Str"```
* Street names without street type: ```"Ореховая", "Восток-5", "Щорса"```
* Incorrect postal codes: ```"12345", "7220082", "772200"```
* Inconsistent phone numbers,  ```"+996 555 70 70 74", "(312) 890257", "0(312)54-49-25", "325528"```
* Multiple phone numbers in different formats: ``` "+996 312 596570, +996 312 596494", "0(312)88-14-14 0(556)11-22-33"```
* Incorrect phone numbers: ```"+99655804111", "+9963122115"```
* Format of website links doesn't follow best practices of OpenStreetMap: ```"grenki.kg", "www.android.kg"```

### Streets cleaning
At first, I decided to change street type so the street field had format: ```<street name> <full street type>```. For this I implemented function fix_street_type in street.py. This function checks the beginning and the end of raw street value and correct abbreviated or translated street type to their respective mappings. Also this function handle consistency of street type position: it places corrected street type after street name.





### Postal codes cleaning

### Phones cleaning

### Websites cleaning


## Overview of Data


## Other ideas about dataset
* language of street names
* old and new street names
* check if the three-digit short phone number exists
* check if the websites are reachable using requests
 



