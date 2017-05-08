import requests

orders=[]
request_string = 'https://backend-challenge-fall-2017.herokuapp.com/orders.json'
r = requests.get(request_string)
data = r.json()
num_pages = data['pagination']['total']
num_cookies = data['available_cookies']
i=1
unfulfilled_orders = []

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

while i <= num_pages:
    temp_str = request_string+'?page='+str(i)
    print temp_str
    r = requests.get(temp_str)
    data = r.json()
    for item in data['orders']:
        process_order(item)

    i += 1

for item in orders:
    print item
print "---------"
sorted_list = sorted(orders, key = lambda item: (item['num_cookies'], -item['id']), reverse=True)
for item in sorted_list:
    print item
print "---------"

for item in sorted_list:
    if item['num_cookies'] > num_cookies:
        unfulfilled_orders.append(item['id'])
        print item
        continue
    else:
        num_cookies = num_cookies-item['num_cookies']

submit_json = {}
submit_json['remaining_cookies'] = num_cookies
submit_json['unfulfilled_orders'] = unfulfilled_orders
# print num_cookies
# print num_unfulfilled
print submit_json
# for item in sorted_list:
#     print item

