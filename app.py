import asyncio
import aiohttp
import requests
from flask import Flask

app = Flask(__name__)


async def fetch(url, session):
    async with session.get(url) as response:
        # The response read is sort of like 
        # a promise. If you await response,
        # well, response is just a regular object,
        # it doesn't have a resolution to wait for.
        # 
        # However, I want to return the whole
        # response, not just the html, so we'll
        # wrap it in a dictionary.
        # 
        # I'd like to catch exceptions here, but it doesn't
        # seem to work.
        html = await response.read()
        return {
            "resp": response,
            "html": html,
            "url": url,
        }


@app.route("/")
def hello():

    urls = [
        "https://whatisjasongoldstein.com/",
        "https://betheshoe.com/",
        "https://theportfolioapp.com/",
        "https://www.theatlantic.com/",
        "https://www.example.org/",
        "https://www.google.com/",
        "https://badurl.whatisjasongoldstein.com/",
    ]

    # Share the session between calls
    session = aiohttp.ClientSession()

    tasks = []
    for url in urls:
        tasks.append(asyncio.ensure_future(fetch(url, session)))

    loop = asyncio.get_event_loop()

    # Gather is like $.when or Promise.all in javascript
    # Return exceptions tells it to add each exception to the list.
    responses = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
    
    output = ""
    for resp in responses:

        # Return exceptions will keep the errors
        # in the list instead of crashing the whole process.
        if isinstance(resp, Exception):
            output += "<p><b>Error:</b> %s<p>" % resp
            continue

        output += "<p>%s loaded with a status %s and a length of %s</p>" % (
                resp["url"], resp["resp"].status, len(resp["html"])
            )

    return output

if __name__ == "__main__":
    app.run(debug=False)  # Only works without DEBUG?
