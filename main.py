from csv import DictWriter
import re
import json_repair

field_mapping = {
    "name": "company",
    "company_name": "company",
    "desc": "description",
    "info": "description",
    "labels": "tags",
    "keywords": "tags",
    "site": "website",
    "url": "website",
    "items": "products",
    "product_list": "products",
}

def clean_columns(record, mapping):
    normalized = {}
    for key, value in record.items():
        new_key = mapping.get(key, key)
        normalized[new_key] = value
    return normalized


def score_lead(lead):
    score = 0
    pattern = re.compile(r'\bcorn[-\s]?starch\b', re.IGNORECASE)

    # check for corn starch in description / tags
    for field in ['description', 'tags']:
        text = lead.get(field, '')
        if pattern.search(text):
            score +=2
    
    #  for each product
    for product in lead.get("products", []):
        if pattern.search(product.get('name', '')):
            score += 2
        
        # for each product ingredient, higher score because potentially more relevant?
        for ingredient in product.get('ingredients', []):
            if pattern.search(ingredient):
                score += 3
    
    lead["score"] = score
    return lead


with open('processed_buyer_leads.json', 'r') as leads_file:
    leads_file = leads_file.read()

# fix the json structure using a package
try:
    decoded_object = json_repair.loads(leads_file)
except Exception as e:
    print("Unable to decode file")

merged = {}

for item in decoded_object:
    item = clean_columns(item, field_mapping)
    company = item.get("company")

    # if we have not seen it then add it to the new dictionary
    if company not in merged:
        merged[company] = item.copy()
    # if we have already seen it, check whether this record has any values the original doesnt
    else:
        for field, value in item.items():
            if merged[company].get(field) is None and value is not None:
                merged[company][field] = value

results = [score_lead(item) for item in list(merged.values())]

with open('results.csv', 'w', newline='') as csv_file:
    fieldnames = results[0].keys()
    writer = DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for record in results:
        writer.writerow(record)

