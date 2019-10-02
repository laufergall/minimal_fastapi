# FastAPI

This example requires Python 3.7.4.

[FastAPI Documentation](https://fastapi.tiangolo.com/)

Start the app with `uvicorn main:app --reload`.
The Swagger UI can be accessed under `http://127.0.0.1:8000/docs`.


# Trying out one client requests

In these runs we always set `n=5` and `seconds_sleep=1`.

Contrary ot what it was expected, calls to `slow_stuff_async` are not performed concurrently. As a result, one single async request behaves like one single sync request:

These logs were obtained:

```bash
15:28:27.239274 start slow stuff sync, call 0
15:28:28.240715 end slow stuff sync, call 0
15:28:28.240715 start slow stuff sync, call 1
15:28:29.241364 end slow stuff sync, call 1
15:28:29.241364 start slow stuff sync, call 2
15:28:30.242792 end slow stuff sync, call 2
15:28:30.242792 start slow stuff sync, call 3
15:28:31.243283 end slow stuff sync, call 3
15:28:31.243283 start slow stuff sync, call 4
15:28:32.244612 end slow stuff sync, call 4
after calling slow_stuff_sync
```

```bash
15:29:00.268650 start slow stuff async, call 0
15:29:01.259684 end slow stuff async, call 0
15:29:01.259684 start slow stuff async, call 1
15:29:02.264527 end slow stuff async, call 1
15:29:02.264527 start slow stuff async, call 2
15:29:03.269135 end slow stuff async, call 2
15:29:03.269135 start slow stuff async, call 3
15:29:04.245531 end slow stuff async, call 3
15:29:04.246104 start slow stuff async, call 4
15:29:05.248989 end slow stuff async, call 4
after calling slow_stuff_async
```

These logs were expected: 

```bash
start slow stuff async, call 0
start slow stuff async, call 1
start slow stuff async, call 2
start slow stuff async, call 3
start slow stuff async, call 4
    ... sleep 1 second
end slow stuff async, call 0
    ... sleep 1 second
end slow stuff async, call 1
    ... sleep 1 second
end slow stuff async, call 2
    ... sleep 1 second
end slow stuff async, call 3
    ... sleep 1 second
end slow stuff async, call 4
after calling slow_stuff_async
```

# Trying out multiple client requests

Opening the Swagger UI in two browser tabs, simulating 2 clients. 

In these runs we always set `n=5` and `seconds_sleep=1`.

It seems that: two sync requests or two async requests (5 seconds long each, separated ~2 seconds) are processed sequentially. Differently, a sync request and an async request can be processed concurrently. 


## client1: sync request and client2: sync request

```bash
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: Started reloader process [25016]
email-validator not installed, email fields will be treated as str.
To install, run: pip install email-validator
INFO: Started server process [4932]
INFO: Waiting for application startup.
15:15:30.316695 start slow stuff sync, call 0
15:15:31.317202 end slow stuff sync, call 0
15:15:31.319203 start slow stuff sync, call 1
15:15:32.320517 end slow stuff sync, call 1
15:15:32.320517 start slow stuff sync, call 2
15:15:33.321354 end slow stuff sync, call 2
15:15:33.327393 start slow stuff sync, call 3
15:15:34.329699 end slow stuff sync, call 3
15:15:34.329699 start slow stuff sync, call 4
15:15:35.330433 end slow stuff sync, call 4
after calling slow_stuff_sync
INFO: ('127.0.0.1', 52967) - "GET /perform_synchronous/?n=5&seconds_sleep=1 HTTP/1.1" 200
15:15:35.333438 start slow stuff sync, call 0
15:15:36.334975 end slow stuff sync, call 0
15:15:36.334975 start slow stuff sync, call 1
15:15:37.336710 end slow stuff sync, call 1
15:15:37.336710 start slow stuff sync, call 2
15:15:38.338428 end slow stuff sync, call 2
15:15:38.338428 start slow stuff sync, call 3
15:15:39.339341 end slow stuff sync, call 3
15:15:39.339341 start slow stuff sync, call 4
15:15:40.340282 end slow stuff sync, call 4
after calling slow_stuff_sync
INFO: ('127.0.0.1', 52967) - "GET /perform_synchronous/?n=5&seconds_sleep=1 HTTP/1.1" 200
```

## client1: sync request and client2: async request

```bash
15:16:34.558594 start slow stuff sync, call 0
15:16:35.559612 end slow stuff sync, call 0
15:16:35.559612 start slow stuff sync, call 1
15:16:35.940615 start slow stuff async, call 0
15:16:36.563627 end slow stuff sync, call 1
15:16:36.563627 start slow stuff sync, call 2
15:16:36.938042 end slow stuff async, call 0
15:16:36.938042 start slow stuff async, call 1
15:16:37.566044 end slow stuff sync, call 2
15:16:37.566044 start slow stuff sync, call 3
15:16:37.937184 end slow stuff async, call 1
15:16:37.937184 start slow stuff async, call 2
15:16:38.568140 end slow stuff sync, call 3
15:16:38.568140 start slow stuff sync, call 4
15:16:38.937110 end slow stuff async, call 2
15:16:38.937110 start slow stuff async, call 3
15:16:39.569478 end slow stuff sync, call 4
after calling slow_stuff_sync
INFO: ('127.0.0.1', 52971) - "GET /perform_synchronous/?n=5&seconds_sleep=1 HTTP/1.1" 200
15:16:39.936408 end slow stuff async, call 3
15:16:39.936408 start slow stuff async, call 4
15:16:40.937360 end slow stuff async, call 4
after calling slow_stuff_async
INFO: ('127.0.0.1', 52972) - "GET /perform_asynchronous/?n=5&seconds_sleep=1 HTTP/1.1" 200
```

## client1: async request and client2: async request

```bash
15:17:15.261192 start slow stuff async, call 0
15:17:16.267237 end slow stuff async, call 0
15:17:16.267237 start slow stuff async, call 1
15:17:17.274047 end slow stuff async, call 1
15:17:17.274047 start slow stuff async, call 2
15:17:18.264018 end slow stuff async, call 2
15:17:18.264018 start slow stuff async, call 3
15:17:19.268720 end slow stuff async, call 3
15:17:19.268720 start slow stuff async, call 4
15:17:20.273914 end slow stuff async, call 4
after calling slow_stuff_async
INFO: ('127.0.0.1', 52975) - "GET /perform_asynchronous/?n=5&seconds_sleep=1 HTTP/1.1" 200
15:17:20.276486 start slow stuff async, call 0
15:17:21.284196 end slow stuff async, call 0
15:17:21.284196 start slow stuff async, call 1
15:17:22.290575 end slow stuff async, call 1
15:17:22.290575 start slow stuff async, call 2
15:17:23.296526 end slow stuff async, call 2
15:17:23.296526 start slow stuff async, call 3
15:17:24.304329 end slow stuff async, call 3
15:17:24.304329 start slow stuff async, call 4
15:17:25.312981 end slow stuff async, call 4
after calling slow_stuff_async
INFO: ('127.0.0.1', 52975) - "GET /perform_asynchronous/?n=5&seconds_sleep=1 HTTP/1.1" 200
```
