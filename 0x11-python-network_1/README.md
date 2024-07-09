## How to Fetch Internet Resources with the Python Package `urllib`

The `urllib` package in Python is a powerful tool for fetching internet resources. It offers a simple interface for making HTTP requests, handling cookies, proxies, and more. Here’s a guide to using `urllib`:

### Basic Fetching with `urllib.request`

To fetch a URL, use the `urlopen` function from `urllib.request`:

```python
import urllib.request

with urllib.request.urlopen('http://python.org/') as response:
    html = response.read()
    print(html)

```

### Handling Data and Headers

You can create a `Request` object to send additional data or headers:

```python
import urllib.parse
import urllib.request

url = 'http://www.someserver.com/cgi-bin/register.cgi'
values = {'name': 'Michael Foord', 'location': 'Northampton', 'language': 'Python'}
headers = {'User-Agent': 'Mozilla/5.0'}

data = urllib.parse.urlencode(values).encode('ascii')
req = urllib.request.Request(url, data, headers)

with urllib.request.urlopen(req) as response:
    result = response.read()
    print(result)

```

## How to Decode `urllib` Body Response

When you receive a response from a server, it might need decoding. Here's how to decode the body response:

```python
import urllib.request

with urllib.request.urlopen('http://python.org/') as response:
    html = response.read().decode('utf-8')
    print(html)

```

## How to Use the Python Package `requests`

The `requests` package is a simpler alternative to `urllib` for making HTTP requests. It’s more user-friendly and handles many aspects of HTTP for you.

### Installing `requests`

First, ensure you have the `requests` package installed:

```
pip install requests

```

### Making HTTP GET Requests with `requests`

```python
import requests

response = requests.get('http://python.org/')
print(response.text)

```

### Making HTTP POST Requests with `requests`

```python
import requests

url = 'http://www.someserver.com/cgi-bin/register.cgi'
values = {'name': 'Michael Foord', 'location': 'Northampton', 'language': 'Python'}

response = requests.post(url, data=values)
print(response.text)

```

### Making HTTP PUT Requests with `requests`

```python
import requests

url = 'http://www.someserver.com/api/update'
values = {'name': 'Michael Foord', 'location': 'Northampton', 'language': 'Python'}

response = requests.put(url, data=values)
print(response.text)

```

## How to Fetch JSON Resources

Fetching JSON data from a web service is straightforward with both `urllib` and `requests`.

### Using `urllib` to Fetch JSON

```python
import urllib.request
import json

url = 'http://api.example.com/data'
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
    print(data)

```

### Using `requests` to Fetch JSON

```python
import requests

response = requests.get('http://api.example.com/data')
data = response.json()
print(data)

```

## How to Manipulate Data from an External Service

Once you have fetched data from an external service, you might want to manipulate it. Here's an example of filtering JSON data:

### Using `urllib`

```python
import urllib.request
import json

url = 'http://api.example.com/data'
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())

# Example manipulation: filter data
filtered_data = [item for item in data if item['attribute'] == 'value']
print(filtered_data)

```

### Using `requests`

```python
import requests

response = requests.get('http://api.example.com/data')
data = response.json()

# Example manipulation: filter data
filtered_data = [item for item in data if item['attribute'] == 'value']
print(filtered_data)

```


## Additional Resources

- [Python urllib Documentation](https://docs.python.org/3/library/urllib.html)
- Requests Documentation
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [RFC 2616 - HTTP/1.1](https://www.w3.org/Protocols/rfc2616/rfc2616.html)