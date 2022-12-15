#!/usr/bin/env python
# coding: utf-8

# # Libraries are imported

# In[ ]:


# All the required libraries are imported.

import requests
from bs4 import BeautifulSoup
import pandas as pd


# # Two functions are defined

# In[ ]:


# function data_retrival is created to retrieve data from the assigned website.

def data_retrival(page_number):
    url = f'https://www.contractsfinder.service.gov.uk/Search/Results?&page={page_number}#dashboard_notices'
    data = requests.get(url)
    text_storage = BeautifulSoup(data.content, 'html.parser')
    
    return text_storage


# In[ ]:


# function data_arrangement is created to clean and arrange the data 
# in a clean and proper manner and stored in a dictionary.

def data_arrangement(contract):
    data_dict = {}
    title = contract.find('div', attrs = {'class':'search-result-header'})['title']
    description = contract.find_all('div', attrs = {'class' : 'wrap-text'})
    data_dict['Contract Title'] = title
    data_dict['Contract Sub-Title'] = description[0].text
    data_dict['Contract Description'] = description[1].text
    
    return data_dict


# # Final Step

# In[ ]:


# here both the functions defined above are used to scrape the data from 
# the given number of pages on the website and are stored in a list.

data_frame = []
final_data = data_retrival(1)
last_page = final_data.find_all(attrs = {'class' : 'standard-paginate'})
max_value = last_page[-1].text.lstrip()

for page_number in range(1, int(max_value) + 1):
    if page_number != 1:
        final_data = data_retrival(page_number)
    tenders = final_data.find_all(attrs = {'class' : 'search-result'})
    for tender in tenders:
        final_output = data_arrangement(tender)
        contract_details = tender.find_all('div', attrs = {'class' : "search-result-entry"})
        for details in contract_details:
            key = details.contents[0].text
            value = details.contents[1].lstrip()
            final_output[key] = value
        data_frame.append(final_output)

df = pd.DataFrame(data_frame)
df.to_csv('solution.csv', index = False)


# In[ ]:




