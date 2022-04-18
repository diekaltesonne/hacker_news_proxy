from flask import Flask, request
from parser import parse_html
import requests
import logging

app = Flask(__name__.split(".")[0])
logging.basicConfig(level=logging.INFO)
APPROVED_HOSTS = " https://news.ycombinator.com/"
LOG = logging.getLogger("app.py")


@app.route("/", defaults={"url_path": ""}, methods=["GET"])
@app.route("/<path:url_path>", methods=["GET"])
def proxy(url_path):
    redirect_url = "%s%s" % (
        url_path,
        ("?" + request.query_string.decode("utf-8") if request.query_string else ""),
    )
    url = "{}{}".format(APPROVED_HOSTS, redirect_url)

    req = requests.Request(
        method=request.method,
        url=url,
        headers=request.headers,
        data=request.data,
    )
    LOG.debug("%s %s with headers: %s", request.method, url, request.headers)
    resp = requests.Session().send(req.prepare(), stream=True)
    content = parse_html(resp.content)
    return content


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
