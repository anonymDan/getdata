from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import telnetlib

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/get_data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Fetch SMS messages from remote Tecno device
            sms_messages = self.fetch_sms_messages()

            # Prepare the response data
            data = {'sms_messages': sms_messages}

            # Save data to a .txt file on the server
            self.save_data_to_file(json.dumps(data))

    def fetch_sms_messages(self):
        # Replace with the remote Tecno device's IP address
        remote_ip = '192.168.1.100'

        try:
            tn = telnetlib.Telnet(remote_ip)

            # Replace the command with the appropriate command to fetch SMS messages on the remote Tecno device
            command = 'adb shell content query --uri content://sms'

            tn.write(command.encode('utf-8') + b'\n')
            output = tn.read_all().decode('utf-8')
            return output
        finally:
            tn.close()

    def save_data_to_file(self, data):
        file_path = 'data.txt'  # Specify the file path where you want to save the data
        with open(file_path, 'w') as file:
            file.write(data)
        print(f'Data saved to {file_path}')

def run_server():
    host = 'localhost'
    port = 8000
    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Server running at {host}:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
