import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview

watson_url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/d33e4275-142b-48c7-a34b-8f63e864fb15"
watson_api_key = "R7mVJtfgf1egPjro6ryQjz2etGNSm_nVAl83K080HiUd"

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    #params = dict()
    #params["text"] = kwargs["text"]
    #params["version"] = kwargs["version"]
    #params["features"] = kwargs["features"]
    #params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if watson_api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs,
                                    auth=('apikey', watson_api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], 
                                   city=dealer_doc["city"], 
                                   full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], 
                                   lat=dealer_doc["lat"], 
                                   long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], 
                                   state=dealer_doc["state"],
                                   zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

# def get_dealer_by_id_from_cf(url, dealerId):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url)
#     if json_result:
#         # Get the row list in JSON as dealers
#         dealers = json_result
#         for ind in range(0, len(dealers)):
#             if dealers[ind]["dealership"] == dealerId:
#                 dealer_doc = dealers[ind]
        
#         dealer_obj = CarDealer(address=dealer_doc["address"], 
#                                city=dealer_doc["city"], 
#                                full_name=dealer_doc["full_name"],
#                                 id=dealer_doc["id"], 
#                                lat=dealer_doc["lat"], 
#                                long=dealer_doc["long"],
#                                short_name=dealer_doc["short_name"],
#                                st=dealer_doc["st"], 
#                                state=dealer_doc["state"],
#                                zip=dealer_doc["zip"])
#         results.append(dealer_obj)
#     return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, id=kwargs["dealerId"])
    if json_result:
        reviews = json_result
        #print(reviews)
        for review in reviews:
            dealer_review = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment="",
                id=review["id"],
            )
            dealer_review.sentiment = analyze_review_sentiments(dealer_review.review)
            results.append(dealer_review)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealerreview):
    body = {"text": dealerreview, "features": {"sentiment": {"document": True}}}
    #print(dealerreview)
    response = requests.post(
        watson_url + "/v1/analyze?version=2019-07-12",
        headers={"Content-Type": "application/json"},
        json=body,  # Use json parameter for automatic conversion
        auth=HTTPBasicAuth("apikey", watson_api_key),
    )

    # Check if request was successful
    if response.status_code == 200:
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
    return "N/A"


def post_requests(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(
            url, headers={"Content-Type": "application/json"}, json=json_payload
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_review(url, review_json_payload):
    response = post_requests(url, review_json_payload)
    return response