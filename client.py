import sys
import socket

#  GLOBAL VARIABLES
HNS_FILEPATH = "PROJI-HNS.txt"
QUERIES = list()
OUTPUT_FILE = open("RESOLVED.txt", "w")
END_CONN_MSG = "END THIS CONNECTION".encode()


def check_for_input_errors():
    if len(sys.argv) != 4:
        print("[Error] Incorrect number of command line arguments!")
        return True
    return False


def populate_queries():
    try:
        fp = open(HNS_FILEPATH)
        line = fp.readline()
        while line:
            line = line.rstrip().lower()
            QUERIES.append(line)
            line = fp.readline()
    finally:
        fp.close()


def establish_connection(hostname, port):
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        exit()

    localhost_addr = socket.gethostbyname(hostname)
    server_binding = (localhost_addr, port)
    conn.connect(server_binding)
    return conn



def perform_queries(rs_conn):
    for query in QUERIES:
        print("[Client] Now querying: " + query);
        rs_conn.sendall(query.encode())
        rs_reply = rs_conn.recv(2048).split(" ")
        if rs_reply[1] == 'A':
            OUTPUT_FILE.write(query + " " + rs_reply[0] + " " + 'A\n')
        else:
            ts_address = rs_reply[0]
            ts_conn = establish_connection(ts_address,tsListenPort)
            ts_conn.sendall(query.encode())
            ts_reply = ts_conn.recv(2048).split(" ")
            if len(ts_reply) == 2:
                OUTPUT_FILE.write(query + " " + ts_reply[0] + " " + 'A\n')
            else:
                OUTPUT_FILE.write(query + " - Error:HOST NOT FOUND\n")
            ## Send a msg to current ts server to shut down the conn to this client.
            ## This is under the assumption that there will exist mutiple different ts servers in the test cases.
            ts_conn.sendall(END_CONN_MSG.encode());
            ts_conn.close()

    rs_conn.sendall(END_CONN_MSG.encode());
    rs_conn.close()
    print("[Client] All queries completed! Please check RESOLVED.txt for validation.")



if __name__ == "__main__":
    if not check_for_input_errors():
        rsHostName = sys.argv[1]
        rsListenPort = int(sys.argv[2])
        tsListenPort = int(sys.argv[3])

        populate_queries()
        rs_conn = establish_connection(rsHostName, rsListenPort)
        perform_queries(rs_conn)
        OUTPUT_FILE.close()
