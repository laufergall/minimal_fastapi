
import asyncio
import time
from datetime import datetime

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def slow_stuff_sync(seconds: int, i: int):
    print(f'{datetime.now().time()} start slow stuff sync, call {i}')
    time.sleep(seconds)
    print(f'{datetime.now().time()} end slow stuff sync, call {i}')


async def slow_stuff_async(seconds: int, i: int):
    print(f'{datetime.now().time()} start slow stuff async, call {i}')
    await asyncio.sleep(seconds)
    print(f'{datetime.now().time()} end slow stuff async, call {i}')


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/perform_synchronous/")
def perform_synchronous(n: int, seconds_sleep: int):
    start = time.time()

    [slow_stuff_sync(seconds_sleep, i) for i in range(n)]
    print('after calling slow_stuff_sync')

    end = time.time()
    return {"total_seconds": end-start}


@app.get("/perform_asynchronous/")
async def perform_asynchronous(n: int, seconds_sleep: int):
    start = time.time()

    [await slow_stuff_async(seconds_sleep, i) for i in range(n)]
    print('after calling slow_stuff_async')

    end = time.time()
    return {"total_seconds": end - start}


@app.get("/perform_background_tasks/")
async def perform_background_tasks(n: int, seconds_sleep: int,
                                   background_tasks: BackgroundTasks):
    start = time.time()

    # to be run after returning a response
    [background_tasks.add_task(slow_stuff_async, seconds_sleep, i) for i in range(n)]
    print('background_tasks set')

    end = time.time()
    return {"total_seconds": end-start}
