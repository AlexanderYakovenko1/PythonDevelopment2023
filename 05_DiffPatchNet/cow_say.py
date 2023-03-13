import asyncio
import shlex

clients = {}

from cowsay import cowsay, list_cows

async def cow_write(writer, message):
    writer.write((message + '\n').encode())
    await writer.drain()


async def cow_chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())

    cont = True
    while cont and not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

        for q in done:

            if q is send:
                message = q.result().decode().strip()
                send = asyncio.create_task(reader.readline())

                split = shlex.split(message)
                if me not in list_cows():
                    if split[0] == 'login':
                        if split[1] not in list_cows():
                            await cow_write(writer, "Not a valid cow name, use 'cows' to learn of available names")
                        elif split[1] in clients:
                            await cow_write(writer, "This name is already taken use 'who' to see registered cows")
                        else:
                            del clients[me]
                            me = split[1]

                            send.cancel()
                            receive.cancel()

                            clients[me] = asyncio.Queue()
                            send = asyncio.create_task(reader.readline())
                            receive = asyncio.create_task(clients[me].get())

                            await cow_write(writer, f"Welcome aboard {me}")
                    elif split[0] == 'who':
                        await cow_write(writer, f"Currently online {[cow for cow in clients if cow in list_cows()]}")
                    elif split[0] == 'cows':
                        cownames = set(list_cows()) - clients.keys()
                        if len(cownames) == 0:
                            await cow_write(writer, "All the cownames have been taken")
                        else:
                            await cow_write(writer, f"Available cownames: {cownames}")
                    elif split[0] == 'exit':
                        cont = False
                        await cow_write(writer, "See ya!")
                    else:
                        await cow_write(writer, "Unknown command")   

                else:
                    if split[0] == 'yield':
                        for name, queue in clients.items():
                            if name in list_cows() and name != me:
                                await queue.put(cowsay(split[1], cow=me))
                    elif split[0] == 'say':
                        if split[1] not in list_cows() and split[1] not in clients.keys():
                            await cow_write(writer, f"No such cow: {split[1]}")
                        else:
                            await clients[split[1]].put(cowsay(split[2], cow=me))
                    elif split[0] == 'who':
                        await cow_write(writer, f"Currently online {[cow for cow in clients if cow in list_cows()]}")
                    elif split[0] == 'cows':
                        cownames = set(list_cows()) - clients.keys()
                        if len(cownames) == 0:
                            await cow_write(writer, "All the cownames have been taken")
                        else:
                            await cow_write(writer, f"Available cownames: {cownames}")
                    elif split[0] == 'exit':
                        cont = False
                        await cow_write(writer, "See ya!")
                    else:
                         await cow_write(writer, "Unknown command")  

            elif q is receive:
                message = q.result()
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{message}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(cow_chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())