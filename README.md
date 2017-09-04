# Very simple async http requests

## Why?

Learning Node, the one thing that's interesting is the ability to make
lots of requests asynchronously. This would be useful if:

1. You depending on many microservices or API's
2. You want to download all the files in a blogpost, like [Django Draftin](https://github.com/whatisjasongoldstein/django-draftin/blob/2f8e6641e622bcda54e1c8d31b4f3bc967418f75/draftin/models.py#L180-L222) does.

## Can Python do this?

It does have new async features. Some inspiration and sample code:

1. <http://skipperkongen.dk/2016/09/09/easy-parallel-http-requests-with-python-and-asyncio/>
1. <https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html>
1. <http://www.giantflyingsaucer.com/blog/?p=5557>
1. <https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html>
1. <https://docs.python.org/3/library/asyncio-task.html#asyncio.gather>
1. <http://stackabuse.com/python-async-await-tutorial/>

## What works well

Making very small async tasks and pulling them into a synchronous function.
Kept simple, this could give us 95% of the benefits of async with the minimum confusion.

## What barely works

Asyncio's docs are overwhelming. The fact that this also 
[confuses Armin Ronacher](http://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/)
suggests its not just my tiny imposter brain that finds it unapproachable.

[aiohttp](https://aiohttp.readthedocs.io) helps, but seems to leave out the simplest
use case: the equivelant of:

```
try:
    resp = request.get("https://myurl.com")
except Exception:
    msg = "Help! Something went horribly wrong!"
```

I hacked around it. It's not great.

## What doesn't work at all

If you're running Flask in debug mode, as one does, you
get a mysterious error:

```
RuntimeError: There is no current event loop in thread 'Thread-1'.
```

I can't find any useful insight into this.

## Other Approaches

There's an asyncio-based microframework called [Quart](https://gitlab.com/pgjones/quart) that follows the Flask API. [Example branch](https://github.com/whatisjasongoldstein/python-async-experiment/tree/quart) courtesy of @pgjones
