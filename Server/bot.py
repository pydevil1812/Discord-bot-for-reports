

import json
import discord
import socket
import asyncio
max_length = 19


with open('ds_config.json') as ds_config_old:
    ds_config_new = json.load(ds_config_old)
    TOKEN = ds_config_new["TOKEN"]
    CHANNEL_ID = int(ds_config_new['CHANNEL_ID'])




intents = discord.Intents.default()
intents.messages = True
bot = discord.Client(intents=intents)

# Переменные для хранения состояния сервера и бота
server_socket = None
stop_event = asyncio.Event()

async def send_to_discord_channel(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

def process_json_and_send(notification_message, CHANNEL_ID): #Пересылает сообщение в дискорд
    asyncio.run_coroutine_threadsafe(send_to_discord_channel(CHANNEL_ID, notification_message), bot.loop)                                                                                    

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    asyncio.create_task(start_server(ip_address, port))  # Запуск сервера после готовности бота
    asyncio.create_task(terminal_input_loop())  # Запуск обработки команд в терминале

async def handle_client(conn, addr): #Делает и Json файла адекватное сообщение
    print(f"Подключено к {addr}")

    data = conn.recv(1024)
    if not data:
        return

    save_path = 'received_data.json'
    with open(save_path, 'wb') as file:
        file.write(data)

    print(f"Файл успешно сохранен: {save_path}")

    with open(save_path, 'r') as file:
        json_data = json.load(file)
        #print(json_data)
        host = json_data["report"][0]["host"]
        time = json_data["report"][0]["time"]
        time = time[:max_length]
        text = json_data["report"][0]["text"]

        notification_message = f'''Хост: {host} ; 
Время {time} ; 
Текст: {text}'''
        #print(notification_message)

        process_json_and_send(notification_message, CHANNEL_ID)

    conn.close()

async def start_server(ip_address, port):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(1)
    server_socket.setblocking(False)
    print(f"Сервер запущен на {ip_address}:{port}")

    loop = asyncio.get_event_loop()

    while not stop_event.is_set():
        try:
            conn, addr = await loop.sock_accept(server_socket)
            loop.create_task(handle_client(conn, addr))
        except asyncio.CancelledError:
            break

    server_socket.close()
    print("Сервер закрыт.")

async def stop_bot():
    print("Остановка бота...")
    stop_event.set()
    await bot.close()  # Используйте bot.close() для выхода

async def terminal_input_loop():
    while not stop_event.is_set():
        # Получение результата выполнения input() из run_in_executor
        command = await asyncio.get_event_loop().run_in_executor(None, input)
        command = command.strip().lower()  # Обработка результата
        if command == 'stop':
            await stop_bot()
            break

# Пример использования функции на сервере
ip_address = 'localhost'
port = 1234

bot.run(TOKEN)
