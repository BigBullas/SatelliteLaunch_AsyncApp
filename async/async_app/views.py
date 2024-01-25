import json
import time
import random
import requests
from concurrent import futures
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

executor = futures.ThreadPoolExecutor(max_workers=1)
ServerToken = "qwertyuiop[]=-0987654321!@#$%^"
url = "http://127.0.0.1:8080/rocket_flights/finish_calculating"

def calculate_price(req_body):
    calculated_price = random.randint(1e6, 100e6)
    time.sleep(5)
    req_body['calculated_price'] = calculated_price
    req_body['token'] = ServerToken
    return req_body

def status_callback(task):
    try:
      result = task.result()
      print(result)
    except futures._base.CancelledError:
      return
    requests.put(url, data=json.dumps(result), timeout=3)

@api_view(['Put'])
def price_calculation(request):
    req_body = json.loads(request.body)
    task = executor.submit(calculate_price, req_body)
    task.add_done_callback(status_callback)        
    return Response(status=status.HTTP_200_OK)
