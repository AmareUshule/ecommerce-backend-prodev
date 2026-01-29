"""Small script to exercise the running API for quick smoke checks.

Provides `post_json` and `get` helpers and example requests when run
directly. Not intended as a full test suite — use `smoke_test.py` or
`live_api_test.py` for quick manual checks during development.
"""

import json
import urllib.request

BASE = 'http://127.0.0.1:8000'

def post_json(path, data, headers=None):
    """POST JSON to `path` and return `(status, parsed_json)`.

    Adds `Content-Type: application/json` header and merges any extra
    headers provided.
    """
    url = BASE + path
    data_bytes = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, method='POST')
    req.add_header('Content-Type', 'application/json')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.load(resp)

def get(path, headers=None):
    """GET `path` and return `(status, parsed_json_or_text)`."""
    url = BASE + path
    req = urllib.request.Request(url, method='GET')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urllib.request.urlopen(req) as resp:
        try:
            return resp.status, json.load(resp)
        except Exception:
            return resp.status, resp.read().decode('utf-8')

if __name__ == '__main__':
    print('1) GET /api/products/ (public)')
    status, data = get('/api/products/')
    print(status)
    print(json.dumps(data, indent=2)[:1500])

    print('\n2) POST /api/users/login/ (admin)')
    status, data = post_json('/api/users/login/', {'email':'admin@example.com','password':'adminpass'})
    print(status)
    print(json.dumps(data, indent=2))

    access = data.get('access')
    if access:
        print('\n3) GET /api/users/profile/ using access token')
        status, pdata = get('/api/users/profile/', headers={'Authorization': f'Bearer {access}'})
        print(status)
        print(json.dumps(pdata, indent=2))
    else:
        print('No access token returned; skipping profile fetch')
