import sys
import socket

RS_FILEPATH = "PROJI-DNSRS.txt"
DNS_TABLE = dict()


def check_for_input_errors():
    if len(sys.argv) != 2:
        print("[ERROR] Incorrect number of command line arguments!")
        return True
    try:
        int(sys.argv[1])
    except ValueError:
        print("[ERROR] Expected valid integer as port number!")
        return True
    return False


def populate_DNS_table():
    try:
        fp = open(RS_FILEPATH)
        line = fp.readline()
        while line:
            line = line.rstrip()
            split = line.split(" ")
            DNS_TABLE[split[0].lower()] = [split[1], split[2]]
            if split[2] == 'NS':
                DNS_TABLE['NS'] = [split[0], 'NS']
            line = fp.readline()
    finally:
        fp.close()


def establish_server_and_serve(rsListenPort):
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        exit()
    server_binding = ('', rsListenPort)
    ss.bind(server_binding)
    while True:
        print("[RS] Now listening...")
        ss.listen(1)
        csockid, addr = ss.accept()
        print("[RS] Connected to client {}!".format(addr));
        while True:
            msg = csockid.recv(2048).decode()
            print("[RS] Recieved from client the following message: " + msg)
            if msg:
                if msg == "END THIS CONNECTION":
                    break;
                if msg in DNS_TABLE:
                    reply = DNS_TABLE[msg][0] + " " + DNS_TABLE[msg][1]
                    print("[RS] Replying to client with: " + reply)
                    csockid.send(reply)
                else:
                    reply = DNS_TABLE['NS'][0] + " " + DNS_TABLE['NS'][1]
                    print("[RS] Replying to client with: " + reply)
                    csockid.send(reply)
        print("[RS] Disconnected with client {}!".format(addr))


if __name__ == "__main__":
    if not check_for_input_errors():
        populate_DNS_table()
        rsListenPort = int(sys.argv[1])
        establish_server_and_serve(rsListenPort)
