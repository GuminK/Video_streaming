import tkinter as tk  # server
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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ipv4, tcp방식
server_socket.bind((HOST, PORT))  # 튜플이 들어감
server_socket.listen(5)  # 5명까지 허용

print("Listening . . .")

group = []
client_socket_list = []


def chat_text_upload(message):
    chat_text.config(state=tk.NORMAL)
    chat_text.insert(tk.END, message + "\n")
    chat_text.config(state=tk.DISABLED)
    ent.delete(0, tk.END)

host_overlap = 0

def sendmsg(message):
    for conn in client_socket_list:
        if conn:
            conn.send(message.encode())


def recvmsg(sock, id):  # msg를 받아와서 출력까지
    while True:
        msg = sock.recv(1024) # 1024바이트만큼 데이터를 받아와
        # id = ''
        # for user in group:  # user 특정
        #     if user['socket'] == sock:
        #         id = str(user['id'])
        #         break
        if msg:
            message = str(id) + "번 사용자: " + msg.decode()  # 수신한 메시지 사용자를 특정지어 이름 붙임s
            sendmsg(message)  # 수신한 메시지 모든 클라이언트에게 전송
            chat_text_upload(message)  # tkinter text창에 message 업로드


def send_screen():  # 화면 클라이언트에게 전송
    pass


def update():  # 웹캠 정보 받아와서 화면에 뿌리기
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        label.config(image=photo)
        label.image = photo
    window.after(10, update)


def pressButton():  # 버튼 이벤트
    message = ent.get()
    if message:
        # chat_text.config(state=tk.NORMAL)
        # chat_text.insert(tk.END, "나: " + message + "\n")
        # chat_text.config(state=tk.DISABLED)
        chat_text_upload("나: " + message)
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


update()  # 웹캠 내 화면에만 뿌려줌



def connect_client():
    while True:
        client_socket, addr = server_socket.accept()  # 연결을 허용한다
        size = len(group)
        user = {'socket': client_socket, 'id': size + 1}  # {'socket':'김구민', 'id':1}
        group.append(user)
        client_socket_list.append(client_socket)


        if client_socket:
            print(addr[0], addr[1] , "연결 되었음")
            reciever = threading.Thread(target=recvmsg, args=(client_socket, size + 1))  # 채팅 수신 스레드
            reciever.start()  # 스레드 시작


        print("연결 되었음")


conn_thread = threading.Thread(target=connect_client)  #
conn_thread.start()



window.mainloop()

