import socket
import time

mail_server = input("Server address ou FQDN: ")

# Get the IP address of "mail_server"
mail_server_ip = socket.gethostbyname(mail_server)

# Mail Variables
helo_command = 'HELO ' + mail_server + '\r\n'
mail_from = b'MAIL FROM:'
rcpt_to = b'RCPT TO:'
mail_data = b'DATA\r\n'
bytes_separator = b'\r\n'

# Messages
oh_no = 'Oops ... Server is Open Relay! Please check...'
oh_good = 'Great Point! '

# Dictionary
# sender and receiver addresses used in MAIL FROM and RCPT TO

sender1 = "<spamtest1@protonmail.com>"
receiver1 = "<relaytest@protonmail.com>"
sender2 = "<spamtest2@protonmail.com>"
receiver2 = "relaytest@protonmail.com"
sender3 = "<spamtest3>"
receiver3 = '<relaytest@protonmail.com>'
sender4 = "<>"
receiver4 = "<relaytest@protonmail.com>"
sender5 = "<spamtest4@[" + mail_server_ip + "]>"
receiver5 = "<relaytest@protonmail.com>"
sender6 = "<spamtest5@" + mail_server + ">"
receiver6 = "<relaytest@protonmail.com>"
sender7 = "<spamtest6@[" + mail_server_ip + "]>"
receiver7 = "<relaytest%protonmail.com@[" + mail_server_ip + "]>"
sender8 = "<spamtest7@[" + mail_server_ip + "]>"
receiver8 = "<relaytest%protonmail.com" + mail_server + ">"
sender9 = "<spamtest8@[" + mail_server_ip + "]>"
receiver9 = "<\"relaytest@protonmail.com\">"
sender10 = "<spamtest9@[" + mail_server_ip + "]>"
receiver10 = "<\"relaytest%protonmail.com\">"
sender11 = "<spamtest10@[" + mail_server_ip + "]>"
receiver11 = "<relaytest@protonmail.com@[" + mail_server_ip + "]>"
sender12 = "<spamtest11@[" + mail_server_ip + "]>"
receiver12 = "<\"relaytest@protonmail.com\"@[" + mail_server_ip + "]>"
sender13 = "<spamtest12@[" + mail_server_ip + "]>"
receiver13 = "<relaytest@protonmail.com" + mail_server + ">"
sender14 = "<spamtest13@[" + mail_server_ip + "]>"
receiver14 = "<@[" + mail_server_ip + "]:relaytest@protonmail.com>"
sender15 = "<spamtest14@[" + mail_server_ip + "]>"
receiver15 = "<" + mail_server + ":relaytest@protonmail.com>"
sender16 = "<spamtest15@[" + mail_server_ip + "]>"
receiver16 = "<protonmail.com!relaytest>"
sender17 = "<spamtest16@[" + mail_server_ip + "]>"
receiver17 = "<protonmail.com!relaytest@[" + mail_server_ip + "]>"
sender18 = "<spamtest17@[" + mail_server_ip + "]>"
receiver18 = "<protonmail.com!relaytest" + mail_server + ">"
sender19 = "<spamtest18@[" + mail_server_ip + "]>"
receiver19 = "<relaytest%protonmail.com@>"
sender20 = "<spamtest19@[" + mail_server_ip + "]>"
receiver20 = "<relaytest@protonmail.com@>"

# Preparation of the dictionary
concat_dict = {sender1: receiver1, sender2: receiver2, sender3: receiver3, sender4: receiver4, sender5: receiver5,
               sender6: receiver6, sender7: receiver7, sender8: receiver8, sender9: receiver9, sender10: receiver10,
               sender11: receiver11, sender12: receiver12, sender13: receiver13, sender14: receiver14,
               sender15: receiver15, sender16: receiver16, sender17: receiver17, sender18: receiver18,
               sender19: receiver19}

# Dictionary declaration
mail_dict_str = {}

# Update the dictionary
mail_dict_str.update(concat_dict)

# Declare variable for the loop. Count the number of test
i = 1

# Loop begin
for key in mail_dict_str:

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def init_con():
        """
        Connection initialisation. Open the socket.
        """
        clientSocket.connect((mail_server, 25))
        time.sleep(0.2)
        recv = clientSocket.recv(1024).decode('utf-8')
        print("<<< " + str(recv))


    def rset():
        """
        Send a RSET before a new try
        """
        clientSocket.sendall(b"RSET" + bytes_separator)
        time.sleep(0.2)
        recv_rset = clientSocket.recv(1024)
        print(">>> RSET")
        print("<<< " + recv_rset.decode('utf-8'))


    def hello():
        """
        Send a HELO
        """
        clientSocket.sendall(helo_command.encode('utf-8'))
        time.sleep(0.2)
        recv1 = clientSocket.recv(1024).decode('utf-8')
        print(">>> " + str(helo_command))
        print("<<< " + str(recv1))

    print("---------- Relay Test#" + str(i) + "----------")
    init_con()
    hello()
    rset()

    time.sleep(0.5)

    clientSocket.sendall(mail_from + key.encode('utf-8') + bytes_separator)
    time.sleep(0.2)
    recv2 = clientSocket.recv(1024).decode('utf-8')
    print(">>> MAIL FROM: " + str(key))
    print("<<< " + str(recv2))

    clientSocket.sendall(rcpt_to + mail_dict_str[key].encode('utf-8') + bytes_separator)
    time.sleep(0.2)
    recv3 = clientSocket.recv(1024)
    print(">>> RCPT TO: " + str(mail_dict_str[key]))
    print("<<< " + recv3.decode('utf-8'))

    clientSocket.send(mail_data)
    time.sleep(0.2)
    recv4 = clientSocket.recv(1024)
    if recv4[:3].decode('utf-8') == "354":
        print(">>> " + mail_data.decode('utf-8'))
        print("<<< " + recv4.decode('utf-8'))
        print(">>> ")
        print(">>> " + oh_no)
        print(">>> ")
        print()
        exit("Configure your server and stay safe!")
    elif recv4[:3].decode('utf-8') == "501" or recv4[:3].decode('utf-8') == "504" or recv4[:3].decode('utf-8') == "554":
        print("<<< " + recv4.decode('utf-8'))
        print(">>> ")
        print(">>> " + oh_good + str(i) + "/19 tests passed")
        print(">>> ")
        print()
        i = i + 1
    elif recv4[:9].decode('utf-8') == "503 5.5.1":
        print("<<< " + recv4.decode('utf-8'))
        print(">>> ")
        print(">>> " + oh_good + str(i) + "/19 tests passed")
        print(">>> ")
        print()
        i = i + 1
    else:
        print("Unknown issue...")
        print("Unknown value is: " + recv4[:3].decode('utf-8'))
        print()
        i = i + 1

    time.sleep(0.5)
    clientSocket.close()

print()
print("Congratulation!!! All tests passed!!!")
print()
