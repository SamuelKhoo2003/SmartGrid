from machine import Pin, I2C, ADC, PWM
from PID import PID
import network
import socket
import ujson
import _thread
import random
import utime
from credentials import SSID, PASSWORD
required_power = 0
# Function to connect to Wi-Fi
#server_port = 5552
str_data = ""
newdata = False
ports = range(5550,5560)

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Connecting to Wi-Fi...", end="")
    
    # Wait for the connection to complete
    while not wlan.isconnected():
        print(".", end="")
        utime.sleep(1)
    
    print(" Connected!")
    print("Network configuration:", wlan.ifconfig())

def receive_from_server(client_socket, client_name):
    global newdata
    global powerreading
    global str_data
    try:
        data = client_socket.recv(2048)
        if data and (data != str_data):
            # Decode and parse the received JSON data
            received_json = data.decode('utf-8')
            parsed_data = ujson.loads(received_json)
            
            if parsed_data.get("client") == client_name:
                str_data = data
                #print(f"Received from server: {parsed_data}")
                return parsed_data['power']
            else:
                print(f"Ignored message for {parsed_data.get('client')}")
    except Exception as e:
        print(f"Error receiving data: {e}")
        print(data)
        #break

# Function to send dummy data to the server
def send_to_server(client_socket, data):
    while True:
        # Generate dummy data with client name
        try:
            client_socket.sendall(ujson.dumps(data).encode('utf-8'))
            print(f"Sent to server: {data}")
        except Exception as e:
            print(f"Error sending data: {e}")
        utime.sleep(5)

def connect_server(server_host, client_name):
    for port in ports:
        try:
            print(f"Attempting to connect to port {port}...")
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Attempt to connect to the server
            sock.connect((server_host, port))
            client_socket.connect((server_host, port))
            print(client_name.encode('utf-8'))
            client_socket.sendall(client_name.encode('utf-8'))  # Send the client's name to the server
            print(f"Successfully connected to port {port}!")
            return sock  # Return the socket if connection is successful
        except OSError as e:
            print(f"Failed to connect to port {port}: {e}")
            if sock:
                sock.close()
    
    print("Could not connect to any port in the range.")
    return None  # Return None if no connection was successful

def maintain_connection(server_host, client_name):
    while True: 
        client_socket = connect_server(server_host, client_name)
        if client_socket:
            return client_socket
        else:
            print(f"retrying to connect to server...")
            utime.sleep(3)


# Function to start the client
def start_client(server_host, client_name, ssid, password):
    # Connect to Wi-Fi
    connect_wifi(ssid, password)
    
    return maintain_connection(server_host, client_name)
    
server_host = '192.168.90.163'  # Replace with your server's IP address

client_name = 'load1'  # Replace with your client name
client_socket = start_client(server_host, client_name, SSID, PASSWORD)
data = None

vret_pin = ADC(Pin(26))
vout_pin = ADC(Pin(28))
vin_pin = ADC(Pin(27))
pwm = PWM(Pin(0))
pwm.freq(100000)
pwm_en = Pin(1, Pin.OUT)
vret_sum = 0
total_vret_readings = 0
tolerance = 5

firstRun = True

pid = PID(0.2, 10, 0, setpoint=0.3, scale='ms')

count = 0
pwm_out = 15000
pwm_ref = 0
setpoint = 0.0
delta = 0.01
max_sp = 0.07

def saturate(duty):
    if duty > 62500:
        duty = 62500
    if duty < 100:
        duty = 100
    return duty

def power_Calc(vout, vret):
    return vout*vret/1.02

while True:
    try:
        required_power = receive_from_server(client_socket, client_name)
        start = utime.time()
        if required_power != None:
            print(required_power)
            pwm_en.value(1)
            stop = False
            while not stop:
                vin = 1.026*(12490/2490)*3.3*(vin_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
                vout = 1.026*(12490/2490)*3.3*(vout_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
                vret = 1*3.3*((vret_pin.read_u16()-350)/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
                count = count + 1      
                pwm_ref = pid(vret)
                pwm_ref = int(pwm_ref*65536)
                pwm.duty_u16(pwm_out)
                vret_sum+=vret
                total_vret_readings+=1
                average_vret = vret_sum/total_vret_readings
                current_Power = power_Calc(vout, vret)        
                if current_Power< required_power*(1-tolerance/100):
                    pwm_out+=100
                elif current_Power > required_power*(1+tolerance/100):
                    pwm_out-=100
                elif required_power*(1-tolerance/100) <= current_Power <= required_power*(1+tolerance/100):
                    print("Power Achieved")

            end = utime.time()
            if end - start >= 5:
                stop = True

            print("Current Power:",current_Power)
            print("Duty Cycle:",pwm_out)
                    
            if count > 2000:
                
                count = 0
                setpoint = setpoint + delta
                        
                if setpoint > max_sp:
                    setpoint = max_sp
                    delta = - delta
                
                if setpoint <= 0:
                    setpoint = 0
                    delta = -delta
                    
                pid.setpoint = setpoint
    except (OSError, socket.error) as e:
        print(f"Connection lost: {e}. Attempting to reconnect...")
        if client_socket:
            client_socket.close()
        client_socket = maintain_connection(server_host, client_name)