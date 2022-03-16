import requests


def get_base_url(base_url):
    # find the wordpress batch request number
    for i in range(30, 0, -1):
        test_base_url = base_url + str(i)
        request = requests.get(test_base_url)
        print(test_base_url, request)
        if request.status_code == 200:
            url = test_base_url
            break 
    return url





def get_request(base_url):
    url = get_base_url(base_url)
    request = requests.get(url)
    while request.status_code != 200:
        url = get_base_url(base_url)
        request = requests.get(get_base_url(base_url))
    return request