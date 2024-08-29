import json
import socket
import os
from jsonschema import validate, ValidationError
import datetime


def check_and_send_json_file(server_address, port, file_path, schema_path):
    try:
        # Шаг 1: Открываем JSON-файл
        with open(file_path, 'r', encoding='utf-8') as file:
            # Шаг 2: Загружаем данные из файла
            data = json.load(file)

        # Шаг 1.2: Открываем файл схемы
        with open(schema_path, 'r', encoding='utf-8') as schema_file:
            schema = json.load(schema_file)

        # Шаг 3: Проверяем структуру
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            print(f"Файл не имеет структуры JSON: {e}")
            return

        # Шаг 4: Устанавливаем соединение с сервером и отправляем данные
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет
        client_socket.connect((server_address, port))  # Подключаемся к серверу

        client_socket.sendall(json.dumps(data).encode())  # Отправляем данные на сервер
        print("JSON файл успешно отправлен")

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode()
        print(f"Ответ от сервера: {response}")

    except FileNotFoundError:
        print("Файл не найден")
    except json.JSONDecodeError:
        print("Файл не является действительным JSON")
    except Exception as e:
        print(f"Произошла ошибка: {e}")  # Отправляем сообщение о том, что произошла какая-то ошибка
    finally:
        client_socket.close()  # Закрываем сокет

