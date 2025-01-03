import requests


if __name__ == "__main__":
    url = "https://httpbin.org/anything"

    response = requests.get(url)

    status_code = response.status_code
    headers = response.headers

    if "Content-Type" in headers and headers["Content-Type"] == "application/json":
        data = response.json()

    print(f"Status code: {status_code}")
    print(f"Headers: {headers}")
    print(f"Content: {response.content}")
    if data:
        print(f"Data: {data}")
