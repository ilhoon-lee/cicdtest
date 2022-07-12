# -*- coding: utf-8 -*- 
#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
PORT_NUMBER = 8080  
# myHnadler 클래스는 브라우저에서 들어오는 모든 요청을 처리 
class myHandler(BaseHTTPRequestHandler):       
    # GET 요청 handler     
        def do_GET(self):              
        	self.send_response(200)              
        	self.send_header('Content-type','text/html')                      
        	self.end_headers()              
        	# Send the html message              
        	self.wfile.write('Commit & Deploy test !!!!') 
        	return  
try:      
    # 웹 서버를 만들고 핸들러를 정의해 들어오는 요청을 관리      
    server = HTTPServer(('', PORT_NUMBER), myHandler)      
    print 'Started httpserver on port ' , PORT_NUMBER       
   
    # 들어오는 HTTP 요청을 계속 기다리도록 구성      
    server.serve_forever()  
# 바깥쪽 try 문에서 KeyboardInterrupt 예외를 처리 
except KeyboardInterrupt:      
    print '^C received, shutting down the web server'             
    server.socket.close()
