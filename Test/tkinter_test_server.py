import tkinter as tk
import cv2
from PIL import Image, ImageTk
from functools import partial
import threading
import socket
import struct
import pickle
import imutils

HOST = ''
PORT = 4700

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("Listening . . .")


def recvmsg(sock):
    while True:
        msg = sock.recv(1024)
        if msg:
            print(msg.decode())
            # message = ent.get()
            message = msg.decode()
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, "상대방: " + message + "\n")
            chat_text.config(state=tk.DISABLED)
            ent.delete(0, tk.END)


def update():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)


def pressButton():
    message = ent.get()
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, "나: " + message + "\n")
    chat_text.config(state=tk.DISABLED)
    ent.delete(0, tk.END)


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


update()


def connclient():
    while True:
        conn, (conn_host, conn_port) = server_socket.accept()
        if conn:
            reciever = threading.Thread(target=recvmsg, args=(conn,))
            reciever.start()

            # if cap.isOpened():
            #     img, frame = cap.read()
            #     frame = imutils.resize(frame, width=640)
            #     frame_bytes = pickle.dumps(frame)
            #     msg = struct.pack("Q",len(frame_bytes)) + frame_bytes
            #     conn.sendall(msg)
            #
            #     cv2.imshow('s', frame)
            #     key = cv2.waitKey(1) & 0xFF
            #     if key == ord('q'):
            #         conn.close()

        print("연결 되었음")


conn_thread = threading.Thread(target=connclient)
conn_thread.start()


window.mainloop()

