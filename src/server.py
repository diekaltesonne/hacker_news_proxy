from flask import Flask, request, Response
from parser import parse_html
import requests
import logging

app = Flask(__name__.split(".")[0])
logging.basicConfig(level=logging.INFO)
APPROVED_HOSTS = " https://news.ycombinator.com/"
LOG = logging.getLogger("app.py")
REQUEST_SESSION = requests.Session()


@app.route("/", defaults={"url_path": ""}, methods=["GET"])
@app.route("/<path:url_path>", methods=["GET"])
def proxy(url_path):

    redirect_url = "%s%s" % (
        url_path,
        ("?" + request.query_string.decode("utf-8") if request.query_string else ""),
    )

    url = "{}{}".format(APPROVED_HOSTS, redirect_url)
    resp = REQUEST_SESSION.get(url, headers=request.headers)
    LOG.debug("%s %s with headers: %s", request.method, url, request.headers)

    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]

    headers = [
        (name, value)
        for (name, value) in resp.headers.items()
        if name.lower() not in excluded_headers
    ]
    content = resp.content

    if resp.headers.get("Content-Type", "").startswith("text/html"):
        content = parse_html(resp.content, request.host_url.strip("/"))

    return Response(
        content,
        content_type=resp.headers["Content-Type"],
        headers=headers,
        status=resp.status_code,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
