from main import *

def test_clean_column_names():
    record = {"name": "company 22", "desc": "test-description", "labels": "test; tag"}
    expected = {"company": "company 22", "description": "test-description", "tags": "test; tag"}
    assert clean_column_names(record, field_mapping) == expected

def test_score_lead_description_and_tags():
    lead = {"description": "Uses corn starch", "tags": ""}
    assert score_lead(lead)["score"] == 2

def test_score_lead_products():
    lead = {"products": [{"name": "Corn-Starch Product", "ingredients": ["corn starch", "sugar"]}]}
    assert score_lead(lead)["score"] == 5

def test_merge_leads():
    leads = [
        {"company": "Company 29", "description": None},
        {"company": "Company 29", "description": "We produce everyday snacks."}
    ]
    merged = merge_leads(leads)
    assert merged[0]["description"] == "We produce everyday snacks."