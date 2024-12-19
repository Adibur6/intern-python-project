import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError


class NetworkRequest:
    @staticmethod
    def _create_request(url,method,data = None,headers = {}):
        if data:
            data = json.dumps(data).encode('utf-8')
        req = Request(url=url, method=method,data=data)
        if data:
            req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        for key, value in headers.items():
            req.add_header(key, value)
        
        result = {}
        try:
            with urlopen(req) as res:
                body = res.read().decode('utf-8')
                result['body'] = json.loads(body)
                result['code'] = res.status
        except HTTPError as e:
            result['body'] = json.loads(e.read().decode('utf-8'))
            result['code'] = e.code
        except Exception as e:
            result['body'] = str(e)
            result['code'] = 500
        return result
        
    @staticmethod
    def get(url, headers = {}):
        return NetworkRequest._create_request(url,'GET',headers=headers)    
    @staticmethod
    def post(url, data, headers = {}):
        return NetworkRequest._create_request(url,'POST',data,headers)
    @staticmethod
    def put(url, data, headers = {}):
        return NetworkRequest._create_request(url,'PUT',data,headers)
    @staticmethod
    def delete(url, headers = {}):
        return NetworkRequest._create_request(url,'DELETE',headers=headers)
        

print(NetworkRequest.get('http://localhost:8000/api/uses/1'))