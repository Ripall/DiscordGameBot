# -*- coding: utf-8 -*-
"""
@author: Dylan Santos de Pinho, Cédric Pahud
"""
import asyncio
import json
import aiohttp

import shlex

import commandebot

URL = "https://discordapp.com/api"
last_sequence = None    

# Spyder hack pour recréer une boucle.
# Pas nécessaire hors de Spyder
loop = asyncio.get_event_loop()
if loop.is_closed():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# fin du hack

async def api_call(path, method="GET", **kwargs):
    """Return the JSON body of a call to Discord REST API."""
    defaults = {
        "headers": {
            "Authorization": f"Bot {TOKEN}",
            "User-Agent": "GameBot (https://medium.com/@greut, 0.1)"
        }
    }
    kwargs = dict(defaults, **kwargs)
    with aiohttp.ClientSession() as session:
        async with session.request(method, f"{URL}{path}", **kwargs) as response:
            if 200 == response.status:
                return await response.json()
            elif 204 == response.status:
                return {}
            else:
                body = await response.text()
                raise AssertionError(f"{response.status} {response.reason} was unexpected.\n{body}")   

 
async def start(url):
    global last_sequence
    with aiohttp.ClientSession() as session:
        async with session.ws_connect(
                f"{url}?v=6&encoding=json") as ws:
            async for msg in ws:
                data = json.loads(msg.data)
                if data["op"] == 10:  # Hello
                    asyncio.ensure_future(heartbeat(
                                ws,
                                data['d']['heartbeat_interval']))
                    await ws.send_json({
                        "op": 2,  # Identify
                        "d": {
                            "token": TOKEN,
                            "properties": {},
                            "compress": False,
                            "large_threshold": 250
                        }
                    })
                elif data["op"] == 0:  # Dispatch
                    last_sequence = data['s']
                    if data['t'] == "MESSAGE_CREATE":
                        if 'bot' not in data['d']['author']: 
                            str = data['d']['content']
                            f = shlex.split(str, posix=False)[0]
                            if f[0]=='!' and hasattr(commandebot,f[1::]) :
                               task = asyncio.ensure_future(send_message(getattr(commandebot,f[1::])(data)))
                            else:
                               print(data)
                        else:
                             print(data)
                            
                        if data['d']['content'] == '!quit':
                            print('Bye bye!')
                            # On l'attend l'envoi du message ci-dessus.
                            await asyncio.wait([task])
                            break
                elif data["op"] == 11:  # Heartbeat ACK
                    pass
                else:
                    print(data)
       
async def heartbeat(ws, interval):
    """Send every interval ms the heatbeat message."""
    while True:
        await asyncio.sleep(interval / 1000)  # seconds
        await ws.send_json({
            "op": 1,  # Heartbeat
            "d": last_sequence
        })
    

async def send_message(data):
    """Send a message with content to the recipient_id."""
    channel_player1 = await api_call("/users/@me/channels", "POST",
                             json={"recipient_id": data[0]})
    await api_call(f"/channels/{channel_player1['id']}/messages",
                          "POST",
                          json={"content": data[1]})
    
    
    channel_player2 = await api_call("/users/@me/channels", "POST",
                             json={"recipient_id": data[2]})
    return await api_call(f"/channels/{channel_player2['id']}/messages",
                          "POST",
                          json={"content": data[3]})
    
            
async def main():
    """Main program."""
    response = await api_call("/gateway")
    await start(response["url"])
    
loop = asyncio.get_event_loop()
loop.set_debug(True)
loop.run_until_complete(main())
loop.close()