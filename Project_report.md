# Wrangle OpenStreetMap Data

#### Map Area
Bishkek, Kyrgyzstan

This is map of the city where I was born, so it was interesting to me to see what database querying reveals, and I liked the opportunity to contribute to its improvement on OpenStreetMap.org.
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

To deal with correcting streets without street types I did two things:
* tried to get obbreviated street type by street name from [offical kyrgyz post site](http://kyrgyzpost.kg/ru/zipcodes-search.html?e%5B_itemcategory%5D%5B%5D=&e%5B6e61c763-659a-4bf2-8d0b-1fd1151b357f%5D=&limit=all&order=alpha&logic=and&send-form=%D0%98%D1%81%D0%BA%D0%B0%D1%82%D1%8C&controller=search&Itemid=356&option=com_zoo&task=filter&exact=0&type=otdelenie-svyazi&app_id=9)
* got street type from manually prepared map of 30 existing street names

So the street correction function looked like:
```python 
def fix_street(raw_street, expected_streets):
    # Check manually prepared map of existing raw streets
    if raw_street in manual_street_name_mapping:
        return manual_street_name_mapping[raw_street]
    # Try to fix street type to standard format
    fixed_street = fix_street_type(raw_street)
    if fixed_street == None:
        # Try to get street type from expected streets (from kyrgyz post website)
        matched_street = None
        for street in expected_streets:
            if street.find(raw_street.strip()) != -1:
                matched_street = street
                break
        fixed_street = fix_street_type(matched_street)
        if fixed_street == None:
            return None
    return fixed_street
```

### Postal codes cleaning
As was mentioned above, processed dataset contains data for Bishkek and some adjacent areas. So I didn't require postal code to be valid only for Bishkek. Otherwise, I only checked if it's valid for Kyrgyzstan: it has to be exacly six digits and first two digits should be "72". So here is the postcode validity function:
```python
def is_valid_postcode(postcode):
    if len(postcode) != 6 or postcode[:2] != "72":
        return False
    return postcode.isdigit()
```

After look of invalid postcodes we can see that some of them are probably just typos, but some are clearly a randomly typed digits:
```python
postcode | count
1234     | 1
11       | 1
772200   | 3
7220082  | 11
1        | 1
12345    | 1
730077   | 2
```

Anyway, I removed all invalid postcodes, because they are useless.

### Phones cleaning

### Websites cleaning


## Overview of Data


## Other ideas about dataset
* language of street names
* old and new street names
* add postcodes by street address
* check if the three-digit short phone number exists
* check if the websites are reachable using requests
 



