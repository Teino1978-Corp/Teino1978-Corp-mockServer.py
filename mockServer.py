from __future__ import print_function #from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import http.server, urllib, datetime, json
#=================================================================
sUrl="/testServer"     #server url
port=8000       #server port
#=================================================================
# data
#=================================================================
jsonDict = {
    "login" : {  # sent at login
        "userName" : "testUser",
        "token"   : "dd408147f19bffa435f5253f76d210cb",
    },        
    "user" : [   # GET /user/userName
        {
            "userName" : "testUser",
            "name"  : "test",
            "email" : "testuser@mailinator.com",
        }
    ],
    "project" : [ #GET /project/projectId
        { 
            "projectId" : "",
            "projectNumber" : 0,
            "name" : "",
            "userName" : "testUser",
            "userEmail" : "testUser@mailinator.com",
            "userPhone" : "1234567890",
            "userAddress" : "",
            "userZipcode" : ""


        },
    ],
    "controller" : [ #GET /controller/controllerId
        {
            "controllerSerialNo" : 0,
            "controllerLocalIp" : "",
            "controllerMaster" : ""
        }
    ]
}
#=================================================================
# run server
#=================================================================
class RequestHandler(http.server.BaseHTTPRequestHandler): #handler here
    def do_GET(self): #show form and messages
        if "/user" in self.path :
            print(jsonDict['user'])
            userList = jsonDict['user']
            for i in userList:
                if i['userName'] in self.path :
                    op=json.dumps(i)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Content-length', len(op))
                    self.end_headers()
                    self.wfile.write(bytes(op, 'utf-8'))
                    return
        else:
            self.send_response(404)
            return

    def do_POST(self) : 
        if self.path == "/login" :
            l=int(self.headers['Content-length'])
            pdata=json.loads(self.rfile.read(l).decode('utf-8'))
            print(pdata)
            if pdata['userName'] == jsonDict['login']['userName'] : 
                op = json.dumps(jsonDict['login'])
                print(op)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-length', len(op))
                self.end_headers()
                self.wfile.write(bytes(op, 'utf-8'))
                return
        else:
            self.send_response(404)
            return

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, HEAD, DELETE, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

#=================================================================
# run server
#=================================================================
print("Server running on port: ", port)
httpd=http.server.HTTPServer(("", port), RequestHandler)
try: httpd.serve_forever()
except KeyboardInterrupt:
    print("Shutting down server");
    httpd.socket.close()
