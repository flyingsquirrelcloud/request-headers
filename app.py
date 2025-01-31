from flask import Flask, render_template, request
from datetime import datetime
import json

app = Flask(__name__)

def get_request_info(req):
    headers = dict(req.headers)

    request_info = {
        "method": req.method,
        "url": req.url,
        "base_url": req.base_url,
        "path": req.path,
        "full_path": req.full_path,
        "query_string": req.query_string.decode('utf-8'),
        "args": dict(req.args),
        "form": dict(req.form),
        "headers": headers,
        "cookies": dict(req.cookies),
        "remote_addr": req.remote_addr,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "endpoint": req.endpoint,
        "blueprint": req.blueprint,
        "view_args": req.view_args,
        "is_json": req.is_json,
        "content_type": req.content_type,
        "content_length": req.content_length,
        "content_encoding": req.content_encoding,
        "referrer": req.referrer,
        "user_agent": str(req.user_agent)
    }

    # Remove keys with None values
    request_info = {k: v for k, v in request_info.items() if v is not None}

    # Handle JSON body
    if req.is_json and req.data:
        try:
            request_info["json"] = req.get_json()
        except Exception as e:
            request_info["json_error"] = str(e)

    # Convert raw data from bytes to string
    if req.data:
        try:
            request_info["raw_data"] = req.get_data(as_text=True)  # Fix: Convert bytes to string
        except Exception as e:
            request_info["data_error"] = str(e)

    return request_info

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def catch_all(path):
    request_info = get_request_info(request)
    return render_template('debug.html',
                           path=path,
                           request_info=request_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)