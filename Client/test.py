import json
import datetime
from client_new import check_and_send_json_file

input_file = 'example.json'
output_file = 'test.json'


host = 'Vasi'
error_message = 'Hello world!' # В эту переменную записывается текст

server_address = 'localhost'
port = 1234
file_path = 'test.json'
schema_path = 'example.json'

def generate_json(host, dt_now, error_message, input_file, output_file):
    # Читаем структуру данных из input_file
    with open(input_file, 'r') as example_file:
        report_data = json.load(example_file)

    # Наполняем данными
    report_data["report"][0]["host"] = host
    report_data["report"][0]["time"] = dt_now
    report_data["report"][0]["text"] = error_message

    # Записываем обновленные данные в output_file
    with open(output_file, 'w') as json_file:
        json.dump(report_data, json_file, indent=4, ensure_ascii=False)

    print("JSON файл создан успешно.")

x = int(input())
if x == 1:
    dt_now = str(datetime.datetime.now())
    generate_json(host, dt_now, error_message, input_file, output_file)
    check_and_send_json_file(server_address, port, file_path, schema_path)
    print(dt_now)
else:
    print('OK')
