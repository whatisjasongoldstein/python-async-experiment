import asyncio
import aiohttp
from quart import Quart

app = Quart(__name__)


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
async def hello():

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

    futures = [asyncio.ensure_future(fetch(url, session)) for url in urls]

    output = ""
    for future in futures:

        try:
            resp = await future
        except Exception as error:
            # Return exceptions will keep the errors
            # in the list instead of crashing the whole process.
            output += "<p><b>Error:</b> %s<p>" % error
            continue
        else:
            output += "<p>%s loaded with a status %s and a length of %s</p>" % (
                resp["url"], resp["resp"].status, len(resp["html"])
            )

    return output

if __name__ == "__main__":
    app.run()
