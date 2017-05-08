import requests

# Get the total number of pages that need to be iterated through
orders=[]
request_string = 'https://backend-challenge-fall-2017.herokuapp.com/orders.json'
r = requests.get(request_string)
data = r.json()
num_pages = data['pagination']['total']
num_cookies = data['available_cookies']
i=1
unfulfilled_orders = []

# Helper method for getting orders which have cookies
def process_order(order):
    if order['fulfilled'] == True:
        return
    products = order['products']
    for item in products:
        if item['title'] == "Cookie":
            temp_dict = {}
            temp_dict['id'] = order['id']
            temp_dict['num_cookies'] = item['amount']
            temp_dict['item'] = item['title']
            orders.append(temp_dict)
            return

# Iterating through pages in the API and processing orders
while i <= num_pages:
    temp_str = request_string+'?page='+str(i)
    r = requests.get(temp_str)
    data = r.json()
    for item in data['orders']:
        process_order(item)
    i += 1

# Sort orders in decreasing number of cookies and increasing id number
sorted_list = sorted(orders, key = lambda item: (item['num_cookies'], -item['id']), reverse=True)

# Process orders which can be done by the company
for item in sorted_list:
    if item['num_cookies'] > num_cookies:
        unfulfilled_orders.append(item['id'])
        continue
    else:
        num_cookies = num_cookies-item['num_cookies']

# Build submission JSON structure
submit_json = {}
submit_json['remaining_cookies'] = num_cookies
submit_json['unfulfilled_orders'] = unfulfilled_orders

print submit_json


