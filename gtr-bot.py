#!/usr/bin/env python3

import sys
import json
import asyncio
import websockets
from urllib.parse import urlparse

def show_message(parsed):
    print(json.dumps(parsed, indent=4, sort_keys=True))

async def send_response(websocket, option):
    await websocket.send('{"type":"option","option":"' + option + '"}')

async def play(websocket_url):
    async with websockets.connect(websocket_url) as websocket:
        while True:
            message = await websocket.recv()
            parsed_message = json.loads(message)
            show_message(parsed_message)
            message_type = parsed_message['type']

            if message_type == "choose":
                options = parsed_message['options']

                # always use "Add Material" action if it is possible
                if 'add-material' in options:
                    await send_response(websocket, 'add-material')
                    continue

                # default: pick the first available option
                await send_response(websocket, options[0])
                continue

            if message_type == "dispatch":
                print("Game Over")
                exit(0)


if len(sys.argv) == 1:
    print ("Usage: gtr-bot.py <copy_game_url_from_browser_here>")
    exit(0)

browser_url = sys.argv[1]
websocket_url = urlparse(browser_url)._replace(scheme="wss", path="game").geturl()
asyncio.run(play(websocket_url))
