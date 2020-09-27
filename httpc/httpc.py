import socket
import ssl
from tkinter import filedialog as fd
import argparse
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

MAX_TIME = 3
HTTP_PORT = 80
HTTPS_PORT = 443
ENCODE = "utf-8"
TYPE_OF_REQ = 'http'


def req(option, host, typec, path, max_bytes):
    port = HTTPS_PORT if typec == 'https' else HTTP_PORT
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host_ip = socket.gethostbyname(host)
        s.settimeout(MAX_TIME)

        s.connect((host_ip, port))
        message = '%s %s HTTP/1.0\nHost: %s\nAccept: text/html\r\n' \
                  'Connection: close\n\n' % (option, path, host)
        print(message)
        context = ssl.create_default_context()
        if typec == "https":
            with context.wrap_socket(s, server_hostname=host) as ss:
                ss.sendall(message.encode())
                data = ss.recv(max_bytes)
        else:
            s.sendall(message.encode())
            data = s.recv(max_bytes)

        data = data.decode("utf-8")
        head = data[:data.find('\n\n')]
        location_point = head.find('Location')
        if location_point != -1:
            location_line = head[location_point:].split('\n')[0]
            new_addrr = location_line[location_line.find(" ") + 1:]
            return new_addrr[:-1]
        else:
            txt.insert(INSERT, data)
            txt.insert(INSERT, "=" * 100 + '\n')


def get_data_with_transfer():
    data = parse_addr(entr.get())
    option = pentr.get()
    max_byte = hopentr.get()
    host, type_of_req, path = data
    if check_correct(host, type_of_req):
        addr = req(option, host,
                   type_of_req, path, int(max_byte))
        while addr is not None:
            addr_parts = addr.split('://')
            type_r = addr_parts[0]
            if addr_parts[1].find('/') != -1:
                host_r = addr_parts[1][:addr_parts[1].find('/')]
                path_r = addr_parts[1][addr_parts[1].find('/'):]
            else:
                host_r = addr_parts[1]
                path_r = '/'
            addr = req(option, host_r, type_r, path_r, int(max_byte))
    else:
        txt.insert(INSERT, "ERROR\n")
        txt.insert(INSERT, "=" * 100 + '\n')


# def change_type_to_http():
#    global TYPE_OF_REQ
#    TYPE_OF_REQ = 'http'


# def change_type_to_https():
#    global TYPE_OF_REQ
#    TYPE_OF_REQ = 'https'


def custom_req(message, type_data):
    port = HTTPS_PORT if 'https' in type_data else HTTP_PORT
    host = ''
    print(message)
    print(type_data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        for i in message.split('\n'):
            print(i)
            if 'Host: ' in i:
                host = i[6:]
                break
        print(host)
        host_ip = socket.gethostbyname(host)
        s.settimeout(MAX_TIME)

        s.connect((host_ip, port))
        print(message)
        print(host)
        context = ssl.create_default_context()
        if port == HTTPS_PORT:
            with context.wrap_socket(s, server_hostname=host) as ss:
                ss.sendall(message.encode())
                data = ss.recv(int(type_data.split(' ')[1]))
        else:
            s.sendall(message.encode())
            data = s.recv(int(type_data.split(' ')[1]))

        data = data.decode("utf-8")
        txt.insert(INSERT, data)
        txt.insert(INSERT, "=" * 100 + '\n')


def parse_addr(addr):
    raw = addr.split('://')
    if len(raw) < 2:
        type_of_req = 'http'
        path_point = raw[0].find('/')
        if path_point != -1:
            host = raw[0][:raw[0].find('/')]
            path = raw[0][raw[0].find('/'):]
        else:
            host = raw[0]
            path = '/'
    else:
        type_of_req = raw[0]
        path_point = raw[1].find('/')
        if path_point != -1:
            host = raw[1][:raw[1].find('/')]
            path = raw[1][raw[1].find('/'):]
        else:
            host = raw[1]
            path = '/'
    print(host, type_of_req, path)
    return host, type_of_req, path


def check_correct(host, type_of_req):
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        messagebox.showinfo('Ошибка ввода', 'Невозможно получить хост')
        return False
    if type_of_req != 'http' and type_of_req != 'https':
        messagebox.showinfo('Ошибка ввода', 'Невозможно получить тип')
        return False
    return True


def save_req():
    data = parse_addr(entr.get())
    option = pentr.get()
    max_byte = hopentr.get()
    host, type_of_req, path = data
    file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                                ("HTML files", "*.html;*.htm"),
                                                ("All files", "*.*")))
    f = open(file_name, 'w')
    message = '%s %s HTTP/1.1\nHost: %s\nAccept: text/html\r\n' \
              'Connection: close\n\n' % (option, path, host)
    type_data = '%s %s' % (type_of_req, max_byte)
    f.write(message + type_data)
    f.close()


def open_req():
    file_name = fd.askopenfilename()
    f = open(file_name)
    s = f.read()
    message = s[:s.find('\n\n')+2]
    type_data = s[s.find('\n\n')+2:]
    custom_req(message, type_data)
    f.close()


if __name__ == '__main__':
    window = Tk()
    window.title("http-client")
    window.geometry('900x600')
    window['bg'] = 'turquoise'
    window.resizable(width=False, height=False)
    txt = ScrolledText(window, width=100, height=25)
    txt.place(x=45, y=10)
    entr = Entry(window, width=40)
    entr.place(x=400, y=450)
    pentr = Entry(window, width=8)
    pentr.place(x=400, y=475)
    hopentr = Entry(window, width=8)
    hopentr.place(x=500, y=475)
    btn = Button(window, text="GET", bg='green', fg='white',
                 command=get_data_with_transfer)
    btn2 = Button(window, text="Save", bg='White', fg='black',
                  command=save_req)
    btn3 = Button(window, text="Open", bg='White', fg='black',
                  command=open_req)
    btn.place(x=775, y=445)
    btn2.place(x=700, y=500)
    btn3.place(x=775, y=500)
    window.mainloop()
