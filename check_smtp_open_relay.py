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

# Foreign to Foreign
sender1 = "TestUser1<testuser1@gmail.com>"
receiver1 = "TestUser2<testuser2@gmail.com>"

# Foreign to Victim
sender2 = "TestUser1<testuser1@gmail.com>"
receiver2 = "TestUser2<testuser2@{}>".format(mail_server)

# Victim to Foreign
sender3 = "TestUser1<testuser1@{}>".format(mail_server)
receiver3 = "TestUser2<testuser2@gmail.com>"

# Victim to Victim
sender4 = "TestUser1<testuser1@{}>".format(mail_server)
receiver4 = "TestUser2<testuser2@{}>".format(mail_server)

# Preparation of the dictionary
concat_dict = [
    ["Foreign to Foreign", sender1, receiver1],
    ["Foreign to Victim", sender2, receiver2],
    ["Victim to Foreign", sender3, receiver3],
    ["Victim to Victim", sender4, receiver4]
]


# Declare variable for the loop. Count the number of test
i = 1

# Loop begin
for item in concat_dict:

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

    testcase = item[0]
    sender = item[1]
    receiver = item[2]

    print("---------- Relay Test#" + str(i) + ": " + testcase)
    init_con()
    hello()
    rset()

    time.sleep(0.5)

    clientSocket.sendall(mail_from + sender.encode('utf-8') + bytes_separator)
    time.sleep(0.2)
    recv2 = clientSocket.recv(1024).decode('utf-8')
    print(">>> MAIL FROM: " + str(sender))
    print("<<< " + str(recv2))

    clientSocket.sendall(rcpt_to + receiver.encode('utf-8') + bytes_separator)
    time.sleep(0.2)
    recv3 = clientSocket.recv(1024)
    print(">>> RCPT TO: " + str(receiver))
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
