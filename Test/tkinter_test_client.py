import tkinter as tk  # client
import cv2
from PIL import Image, ImageTk
from functools import partial
import threading
import socket

# 127.0.0.1
server_ip = "localhost"
port = 4700

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, port))  # 연결 요청

print("연결 되었습니다 . . .")



def chat_text_upload(message):
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, message + "\n")
    chat_text.config(state=tk.DISABLED)
    ent.delete(0, tk.END)


def sendmsg(sock):
    pass
def recvmsg(sock):
    while True:
        msg = sock.recv(1024)
        if msg:
            print(msg.decode())
            message = msg.decode()
            chat_text.config(state=tk.NORMAL)
            chat_text.insert(tk.END, "" + message + "\n")
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
    msg = ent.get()
    print("text_get()으로 가져온 값 : ", msg)

    message = ent.get()

    chat_text_upload("나: "+message)

    client_socket.send(message.encode())


window = tk.Tk()
window.geometry("1150x530")
window.title("client 테스트창")
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

reciever = threading.Thread(target=recvmsg, args=(client_socket,))
reciever.start()


# update()

window.mainloop()