from flask import Flask, render_template_string, request
import socket
import time

app = Flask(__name__)

# store last "proxied" request info, using key value pairs
last_request = {
    "ip": None,
    "method": None,
    "user_agent": None,
    "client_sent_at": None,         # key to store when sent from client
    "proxy_received_at": None,      # key to store when arrived at proxy
    "server_received_at": None,     # key to store when arrived at webserver
    "client_to_proxy_time": None,   # key used to calculate time to go from client to proxy
    "proxy_to_server_time": None,   # key used to calculate time to go from proxy to webserver
    "total_time": None,             # key used to calculate time to go from client to webserver
}

PAGE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>CloudLab Web Server</title>
    <style>
      body {
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background: #0f172a;
        color: #e5e7eb;
        margin: 0;
        padding: 2rem;
      }
      .card {
        max-width: 720px;
        margin: 0 auto;
        background: #020617;
        border-radius: 1rem;
        padding: 1.5rem 2rem;
        box-shadow: 0 20px 40px rgba(15,23,42,0.7);
        border: 1px solid #1f2937;
      }
      h1 { margin-top: 0; color: #38bdf8; }
      code {
        background: #111827;
        padding: 0.15rem 0.3rem;
        border-radius: 0.25rem;
        font-size: 0.9rem;
        white-space: pre-wrap;
      }
      .meta {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #1f2937;
        font-size: 0.9rem;
        color: #9ca3af;
      }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>CloudLab Web Server</h1>
      <p>This page is being served from your CloudLab node:</p>
      <ul>
        <li><strong>Server hostname:</strong> {{ hostname }}</li>
        <li><strong>Server IP (as seen by this request):</strong> {{ server_ip }}</li>
      </ul>

      <h2>Last packet received via proxy</h2>
      {% if proxied_ip %}
        <ul>
          <li><strong>Client IP (as seen by Flask):</strong> {{ proxied_ip }}</li>
          <li><strong>HTTP method:</strong> {{ proxied_method }}</li>
          <li><strong>User-Agent:</strong> {{ proxied_user_agent }}</li>
        </ul>

        <h3>Timing information</h3>
        <ul>
          <li><strong>Client → Proxy:</strong>
            {% if client_to_proxy_time is not none %}
              {{ "%.3f" % client_to_proxy_time }} ms
            {% else %}
              unknown
            {% endif %}
          </li>
          <li><strong>Proxy → Server:</strong>
            {% if proxy_to_server_time is not none %}
              {{ "%.3f" % proxy_to_server_time }} ms
            {% else %}
              unknown
            {% endif %}
          </li>
          <li><strong>Client → Server (total):</strong>
            {% if total_time is not none %}
              {{ "%.3f" % total_time }} ms
            {% else %}
              unknown
            {% endif %}
          </li>
        </ul>
      {% else %}
        <p><em>No packets have been received from the proxy yet.</em></p>
      {% endif %}

      <div class="meta">
        <p>You are viewing this page from: <code>{{ viewer_ip }}</code></p>
      </div>
    </div>
  </body>
</html>
"""


# route the PROXY hits
@app.route("/probe", methods=["GET", "POST"])
def probe():

    # this runs only when your proxy forwards a request here
    last_request["ip"] = request.remote_addr
    last_request["method"] = request.method
    last_request["user_agent"] = request.headers.get("User-Agent", "unknown")

    # getting the times from the client, proxy and webserver and storing them
    # if the headers are not there (like in a request from a browser which doesn't have those headers)
    #then set the values to 0
    sent_at_header = request.headers.get("Client-Sent-At", "0")
    proxy_received_header = request.headers.get("Proxy-Received-At", "0")
    server_received = time.time()

    # store the times in the dictionary
    last_request["client_sent_at"] = sent_at_header
    last_request["proxy_received_at"] = proxy_received_header
    last_request["server_received_at"] = server_received

    # computing the times in milliseconds
    client_to_proxy = (float(last_request["proxy_received_at"]) - float(last_request["client_sent_at"])) * 1000
    proxy_to_server = (float(last_request["server_received_at"]) - float(last_request["proxy_received_at"])) * 1000
    total = (float(last_request["server_received_at"]) - float(last_request["client_sent_at"])) * 1000

    # store the computed times in the dictionary
    last_request["client_to_proxy_time"] = client_to_proxy
    last_request["proxy_to_server_time"] = proxy_to_server
    last_request["total_time"] = total

    return "OK\n"

# route your BROWSER hits
@app.route("/", methods=["GET"])
def index():
    hostname = socket.gethostname()
    server_ip = request.host.split(":")[0]
    viewer_ip = request.remote_addr   # your laptop when viewing

    return render_template_string(
        PAGE,
        hostname=hostname,
        server_ip=server_ip,
        viewer_ip=viewer_ip,
        proxied_ip=last_request["ip"],
        proxied_method=last_request["method"],
        proxied_user_agent=last_request["user_agent"],
        client_to_proxy_time=last_request["client_to_proxy_time"],    # passing the values computed in /probe handeler into the jinja template
        proxy_to_server_time=last_request["proxy_to_server_time"],    #
        total_time=last_request["total_time"],                        #
    )

def main() -> None:
    app.run(
        host="0.0.0.0",
        port=8080,
        ssl_context=("MyCert.crt", "MyKey.key")
    )

if __name__ == "__main__":
    main()
