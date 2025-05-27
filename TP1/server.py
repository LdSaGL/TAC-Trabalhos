from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from jwt_utils import generate_jwt, verify_jwt
import user_db as db
import ssl

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/login":
            self.handle_login()
        elif self.path == "/register":
            self.handle_register()
        else:
            self.send_error(404, "Route not found")
    
    def do_GET(self):
        if self.path == "/protected":
            self.handle_protected()
        else:
            self.send_error(404, "Route not found")
            
    def handle_protected(self):
        auth_header = self.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Missing or invalid Authorization header")
            return

        token = auth_header.split(" ")[1]

        payload = verify_jwt(token)
        if not payload:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Invalid or expired token")
            return

        # Valid Token
        username = payload.get("sub")  
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        response = {"message": f"Welcome {username}! You accessed a protected resource."}
        self.wfile.write(json.dumps(response).encode())

    def handle_login(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
            username = data.get("username")
            password = data.get("password")
            alg = data.get("alg", "HS256")

            if not db.verify_user(username, password):
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"Invalid credentials")
                return

            token = generate_jwt({"sub": username}, exp_minutes=5, alg=alg)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"token": token, "alg": alg}).encode())

        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error while logging in: {e}".encode())

    def handle_register(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Username and password are required")
                return

            if db.create_user(username, password):
                self.send_response(201)
                self.end_headers()
                self.wfile.write(b"User registered successfully")
            else:
                self.send_response(409)
                self.end_headers()
                self.wfile.write(b"User already exists")

        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error while registering: {e}".encode())

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHandler)

    # Wrap the socket with TLS
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile='cert.pem',
                                   keyfile='key.pem',
                                   ssl_version=ssl.PROTOCOL_TLS)

    print("Servidor HTTPS rodando em https://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
