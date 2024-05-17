import _thread as thread
import platform
import json
import re

ores = ""

# OpenAI API endpoint here
def handle_v1_completions_default(self, ai, obj, runline2, method):
    if "prompt" in obj:
        res = runline2(ai, obj["prompt"])
        resobj = {}
        resobj["choices"] = [{
            "text": res
        }]
        resjson = json.dumps(resobj)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(f'{resobj}', 'utf-8'))
    self.send_response(404)
    self.end_headers()
    return True

def handle_v1_completions(self, ai, obj, runline2, method):
    global ores
    print("/v1/completions")
    if obj == None:
        print("ObjNone")
        self.send_response(200)
        self.end_headers()
        return True
    if "segments" not in obj:
        return handle_v1_completions_default(self, ai, obj, runline2, method)
    pfx = obj["segments"]["prefix"].strip()
    sfx = obj["segments"]["suffix"].strip()
    lng = obj["language"]
    if pfx == "":
        self.send_response(200)
        self.end_headers()
        return True
    runline2(ai, "-R")
    #codequery = f"What's between `{pfx}` and `{sfx}` in `{lng}`, without including the context"
    codequery = f"Complete the code between `{pfx}` and `{sfx}` in `{lng}`"
    response = json.loads('''{
  "id": "cmpl-9d8aab26-ddc1-4314-a937-6654f2c13932",
  "choices": [
    {
      "index": 0,
      "text": ""
    }
  ]
  }''')
    print(f"PREFIX {pfx}")
    print(f"SUFFIX {sfx}")
    print(f"RES {ores}")
    response["choices"][0]["text"] = ores
    jresponse = json.dumps(response)
    self.send_response(200)
    self.end_headers()
    self.wfile.write(bytes(f'{jresponse}','utf-8'))
    print("compute query")
    ores = runline2(ai, codequery).strip()
    ores = ores.replace(pfx, "")
    ores = ores.replace(sfx, "")
    ores = re.sub(r'```.*$', '', ores)
    ores = ores.replace("```javascript", "")
    ores = ores.replace("```", "")
    ores = ores.replace("\n", "");
    ores = ores.strip()
    print(f"RES2 {ores}")
    print("computed")

def handle_tabby_query(self, ai, obj, runline2, method):
    global ores
    # TODO build proper health json instead of copypasting a stolen one
    model = ai.env["llm.model"]
    healthobj = {
            "model":ai.env["llm.model"],
            "device":"gpu" if ai.env["llm.gpu"] else "cpu",
            "arch": platform.machine(),
            "cpu_info": "",
            "cpu_count": 1,
            "cuda_devices": [],
            "version": {
                "build_date": "2024-05-22",
                "build_timestamp": "2024-05-22",
                "git_sha": "",
                "git_describe": "",
            },
    }
    healthstr=json.dumps(healthobj)
    print(healthstr)
    if method == "GET" and self.path == "/v1/health":
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(f'{healthstr}','utf-8'))
        return True
    # /v1/completions
    if self.path == "/v1/completions":
        return handle_v1_completions(self, ai, obj, runline2, method)

    print(f"UnkPath: {self.path}")
    self.send_response(200)
    self.end_headers()
    return True

def handle_custom_request(self, ai, msg, runline2, method):
    print("CUSTOM")
    if method == "GET":
        if handle_tabby_query(self, ai, None, runline2, method):
            return True
        return False
    if msg.startswith("{"):
        obj = json.loads(msg)
        if "language" in obj:
            handle_tabby_query(self, ai, obj, runline2, method)
            return True
    return True

def start_http_server_now(ai, runline2):
    import http.server
    import socketserver
    WANTCTX = ai.env["http.chatctx"] == "true"
    PORT = int(ai.env["http.port"])
    BASEPATH = ai.env["http.path"]
    Handler = http.server.SimpleHTTPRequestHandler
    class SimpleHTTPRequestHandler(Handler):
        def do_GET(self):
            print("GET")
            if handle_custom_request(self, ai, "", runline2, "GET"):
                return
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes(f'Invalid request. Use POST and /{BASEPATH}', 'utf-8'))
        def do_POST(self):
            print("POST")
            if not WANTCTX:
                runline2(ai, "-R")
            content_length = int(self.headers['Content-Length'])
            msg = self.rfile.read(content_length).decode('utf-8')
            if handle_custom_request(self, ai, msg, runline2, "POST"):
                return
            if self.path.startswith(BASEPATH):
                self.send_response(200)
                self.end_headers()
                res = runline2(ai, msg)
                self.wfile.write(bytes(f'{res}','utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes(f'Invalid request. Use {BASEPATH}'))
    print("[R2AI] Serving at port", PORT)
    Handler.protocol_version = "HTTP/1.0"
    server = socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler)
    server.allow_reuse_address = True
    server.allow_reuse_port = True
    server.serve_forever()

def start_http_server(ai, runline2, background):
    if background:
        thread.start_new_thread(start_http_server_now, (ai, runline2))
    else:
        start_http_server_now(ai, runline2)
