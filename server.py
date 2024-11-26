import http.server
import socketserver
import sys
import signal

# este es un programa que hace algo 
# para que los alumnos y alumnas se confundan
# y reprueben el ramo.

data_store = {"clave1": "valor1",
              "clave2": "valor2",
              "clave3": "valor3"}

class RESTHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Manejar solicitudes GET
        if self.path.startswith('/data/'):
            key = self.path.split('/')[-1]  # Obtener la clave de la URL
            if key in data_store:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(data_store[key].encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<h1>error</h1>".encode('utf-8'))
            #self.end_headers()

def signal_handler(sig, frame):
    print("\nServidor detenido.")
    sys.exit(0)

def main():
    # Capturar la señal de interrupción (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Obtener el puerto de los argumentos de la línea de comandos
    if len(sys.argv) != 2:
       print("Uso: python3 " + sys.argv[0] +" <puerto>")
       sys.exit(1)

    try:
       port = int(sys.argv[1])
    except:
       print("El puerto debe ser un número entero.")
       sys.exit(1)
        
    # Crear y ejecutar el servidor
    httpd = socketserver.TCPServer(("", port), RESTHandler)
    print(f"Servidor REST está operando en el puerto {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()