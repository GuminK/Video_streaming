import tkinter as tk
import cv2
from PIL import Image, ImageTk
from functools import partial
import threading
import socket
import struct
import pickle
import imutils
import numpy as np
import json


HOST = ''
PORT = 4700

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4, tcp방식
server_socket.bind((HOST, PORT)) # 거의 튜플형식으로 들어감
server_socket.listen(5) # 5명까지 들어올 수 있다

print("Listening . . .")

group = []
user = []
test = []



def sendmsg(message):
    for conn in test:
        conn.send(message.encode())


def recvmsg(sock):  # 데이터를 받아와서 문자열? 화면에 뿌려줌
    while True:
        msg = sock.recv(1024) # 1024바이트만큼 데이터를 받아와
        id = ''
        for user in group: # # {'msg':'어쩌구구', 'id':1}, {'socket':'권ㄷ', 'id':1}
            if(user['socket'] == sock):
                id = str(user['id'])
                break

        if msg:
            string_a = id + "번 사용자: "
            print(msg.decode())  # decode()
            message = msg.decode()
            sdmsg = string_a + message
            sendmsg(sdmsg)
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, string_a + message + "\n")
            chat_text.config(state=tk.DISABLED)
            ent.delete(0, tk.END)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

header = []
header.append(0x20)

def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo

        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(frame)
        stringData = bytes(data)  # str(data)

        # jsonData = { 'data' : data, 'flag' : 'img' }
        # body = json.dumps(jsonData)
        #
        # leng = len(body)
        #
        # message = bytearray(header)
        # ## 보낼 때는 python 3.1 ~에서 슬 수 있는 .to_bytens사용
        # message += bytearray(leng.to_bytes(2, byteorder="big"))
        # message += bytes(body, 'utf-8')
        #
        # for user in group:
        #     user['socket'].sendall(message)
        for user in group:
            user['socket'].sendall((str(len(stringData))).encode().ljust(16) + stringData)

    window.after(10, update)


def pressButton():
    message = ent.get()
    if message:
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, "나: " + message + "\n")
        chat_text.config(state=tk.DISABLED)
        ent.delete(0, tk.END)
        message = "서버 : " + message
        sendmsg(message)


window = tk.Tk()
window.geometry("1150x530")
window.title("server 테스트창")
window.option_add("*Font","고딕체 12")
# 웹캠
cap = cv2.VideoCapture(0)
# 웹캠 라벨
label = tk.Label(window)
label.place(x=0, y=20)
# 채팅 내역
chat_text = tk.Text(window)
chat_text.config(width=50, wrap=tk.WORD, state=tk.DISABLED)
chat_text.place(x=650, y=20)
# 입력창
ent = tk.Entry(window)
ent.config(width=45)
ent.place(x=650, y=480)
# 입력 버튼
btn = tk.Button(window)
btn.place(x=1040, y=475)
btn.config(text="버튼")
btn.config(command=pressButton)
# btn.config(command=partial(pressButton, 5))


update()  # 웹캠 내 화면에만 뿌려줌 ㅋㅋ



def connect_client():
    while True:
        client_socket, addr = server_socket.accept()  # 연결을 허용한다
        size = len(group)
        user = {'socket':client_socket, 'id':size + 1} # {'socket':'김구민', 'id':1}, {'socket':'권ㄷ', 'id':1}
        group.append(user)

        test.append(client_socket)


        if client_socket:
            print(addr[0], addr[1] , "연결 되었음")
            reciever = threading.Thread(target=recvmsg, args=(client_socket,))  # 채팅 받아오는거 클라이언트한테서
            reciever.start()  # 스레드 시작


        print("연결 되었음")


conn_thread = threading.Thread(target=connect_client)  #
conn_thread.start()



window.mainloop()

