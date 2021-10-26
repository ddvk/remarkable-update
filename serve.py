#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import http.server
import xml.etree.ElementTree as ET
import os,sys, io, socket, hashlib, base64
import binascii


port = 8000
updates_folder = 'updates'

response_ok = """<?xml version='1.0' encoding='UTF-8'?>
<response protocol="3.0" server="prod">
  <daystart elapsed_seconds="42548" elapsed_days="5179"/>
  <app status="ok" appid="{98DA7DF2-4E3E-4744-9DE6-EC931886ABAB}">
    <event status="ok"/>
    <ping status="ok"/>
  </app>
</response>
"""

response_template = """<?xml version="1.0" encoding="UTF-8"?>
 <response protocol="3.0" server="prod">
  <daystart elapsed_seconds="37145" elapsed_days="5179"/>
  <app status="ok" appid="{{98DA7DF2-4E3E-4744-9DE6-EC931886ABAB}}">
    <event status="ok"/>
    <updatecheck status="ok">
      <urls>
        <url codebase="{codebase_url}"/>
      </urls>
      <manifest version="{version}">
        <packages>
          <package required="true" hash="{update_sha1}" name="{update_name}" size="{update_size}"/>
        </packages>
        <actions>
          <action successsaction="default" sha256="{update_sha256}" event="postinstall" DisablePayloadBackoff="true"/>
        </actions>
      </manifest>
    </updatecheck>
    <ping status="ok"/>
  </app>
</response>
"""

def hostname(host):
    url =  f"http://{host}:{port}/"
    return url

def getupdateinfo(platform, version, update_name):
    full_path = os.path.join(updates_folder, update_name)

    update_size = str(os.path.getsize(full_path))

    BUF_SIZE = 8192

    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    with open(full_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
            sha256.update(data)
    update_sha1 = binascii.b2a_base64(sha1.digest(), newline=False).decode()
    update_sha256 = binascii.b2a_base64(sha256.digest(), newline=False).decode()
    return (update_sha1, update_sha256, update_size)


def scan_updates():
    files = os.listdir(updates_folder)
    versions={}
    for f in files:
        p = f.split('_')
        if len(p) != 2:
            continue
        t = p[1].split('.')
        if len(t) != 2:
            continue

        z = t[0].split('-')

        version = p[0]
        print(version)
        product = z[0]

        if not product in versions or versions[product][0] < version:
            versions[product]=(version, f)

    return versions


class MySimpleHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(length).decode('utf-8')
        print(body)
        xml = ET.fromstring(body)
        updatecheck_node = xml.find('app/updatecheck')


        #check for update
        if updatecheck_node is not None:
            version = xml.attrib["version"]
            platform = xml.find('os').attrib['platform']
            print("requested: ", version)
            print("platform: ", platform)


            version, update_name  = available_versions[platform]

            update_sha1, update_sha256, update_size = getupdateinfo(platform, version, update_name)
            params = {
                    "version": version,
                    "update_name": f"{updates_folder}/{update_name}",
                    "update_sha1": update_sha1,
                    "update_sha256": update_sha256,
                    "update_size" : update_size,
                    "codebase_url": host_name,
                    }

            response = response_template.format(**params)
            print("Response:")
            print(response)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())
            return

        event_node = xml.find('app/event')
        event_type = int(event_node.attrib["eventtype"])
        event_result = int(event_node.attrib["eventresult"])

        #post install status
        if event_result != 0:
            print("Update done")
            if "errorcode" in event_node.attrib:
                print("With errorcode:", event_node.attrib["errorcode"])
            return

        #update done
        if event_type == 14:
            print("OK Response:")
            print(response_ok)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response_ok.encode())
            return

available_versions = scan_updates()
host_name = None 

if __name__ == "__main__":
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        print("Using hostname, to override use: ./serve.py hostname")
        host = socket.gethostname()
    host_name = hostname(host)
        
    print("Device should use: ", host_name)
    print("Available updates:", available_versions)

    handler = MySimpleHTTPRequestHandler
    httpd = HTTPServer(('0.0.0.0', port), handler)
    print(f"Starting fake updater: {port}")
    httpd.serve_forever()
