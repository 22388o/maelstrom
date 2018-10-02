from rpyc.utils import factory
from rpyc.core.service import ClassicService
from rpyc.core.stream import SocketStream
import rpyc
import ssl, os, socket


def ssl_connect(host, port, server_cert, client_cert, client_key, family=socket.AF_INET, socktype = socket.SOCK_STREAM, proto = 0):
    # context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    context.load_verify_locations(server_cert)

    context.load_cert_chain(certfile = client_cert, keyfile = client_key)

    family, socktype, proto, _, sockaddr = socket.getaddrinfo(host, port, family, socktype, proto)[0]
    s = socket.socket(family, socktype, proto)
    s.settimeout(3)
    s.connect(sockaddr)
    s.connect((host, port))
    s2 = ssl.wrap_socket(s, do_handshake_on_connect = False, server_side = False, ssl_version=ssl.PROTOCOL_TLSv1_2, certfile = client_cert, keyfile = client_key)
    try:
        s2.do_handshake()
    except ssl.SSLError as e:
        print(e)
    return factory.connect_stream(SocketStream(s2), service = ClassicService, config = {"allow_public_attrs" : True})

ssl_connect('127.0.0.1', 8002, os.path.abspath('../c-simple/certs/node.crt'),
            os.path.abspath('../c-simple/certs/client.crt'), os.path.abspath('../c-simple/certs/client.key'))

#c.get_balance()

