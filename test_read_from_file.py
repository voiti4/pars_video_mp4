# Открываем файл в режиме "rb" (бинарный режим чтения)
with open('1.hex', 'rb') as f:
    # Читаем содержимое файла в виде байтов
    f.seek(4)
    data = f.read(4)
    str = 'ftyp'
    if data == b'ftyp':
        print('Okk')
    print(data)
    print(f'b{str}')
    print(int.from_bytes(data))
   # print(data)
   # print(str(data))
    str = data.decode()   
    if str == 'ftyp':
        print("Ok")
print(data.hex())
""" for bt in range(0, len(data) - 4):
    if data[bt:(bt + 4)] == (b'\x62\x65\x61\x6d'):
        print(f'Find pos = {bt}') """

# print(b'isom')
# Преобразуем байты в список шестнадцатеричных чисел
# hex_list = [hex(b)[2:] for b in data]

# Выведем список на экран
# print(hex_list)