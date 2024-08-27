from machine import Pin, I2C, ADC, PWM, Timer
import network
import socket
import ujson
import _thread
import machine
import utime
from credentials import SSID, PASSWORD

required_storage = 0
str_data = ""
cap_current = 0
total_current = 0 
ports = range(5550,5560)             

# Function to connect to Wi-Fi
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

# Function to receive data from the server
def receive_from_server(client_socket, client_name):
    global str_data
    try:
        data = client_socket.recv(2048)
        if data and (data != str_data):
            # Decode and parse the received JSON data
            received_json = data.decode('utf-8')
            parsed_data = ujson.loads(received_json)
            
            if parsed_data.get("client") == client_name:
                str_data = data
                print(f"Received from server: {parsed_data}")
                return parsed_data['storage']
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
            client_socket.connect((server_host, server_port))
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
    # Create a socket and connect to the server

    # Start threads for sending and receiving data
    #_thread.start_new_thread(receive_from_server, (client_socket,))
    return maintain_connection(server_host, client_name)

# Set up some pin allocations for the Analogues and switches
va_pin = ADC(Pin(28))
vb_pin = ADC(Pin(26))
vpot_pin = ADC(Pin(27))
OL_CL_pin = Pin(12, Pin.IN, Pin.PULL_UP)
BU_BO_pin = Pin(2, Pin.IN, Pin.PULL_UP)

# Set up the I2C for the INA219 chip for current sensing
ina_i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=2400000)

# Some PWM settings, pin number, frequency, duty cycle limits and start with the PWM outputting the default of the min value.
pwm = PWM(Pin(9))
pwm.freq(100000)
min_pwm = 1000
max_pwm = 64536
pwm_out = min_pwm
pwm_ref = 30000

#Some error signals
trip = 0
OC = 0

# The potentiometer is prone to noise so we are filtering the value using a moving average
v_pot_filt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
v_pot_index = 0

# Gains etc for the PID controller
i_ref = 0 # Voltage reference for the CL modes
i_err = 0 # Voltage error
i_err_int = 0 # Voltage error integral
i_pi_out = 0 # Output of the voltage PI controller
kp = 100 # Boost Proportional Gain
ki = 300 # Boost Integral Gain
duty = 0

# Basic signals to control logic flow
global timer_elapsed
timer_elapsed = 0
count = 0
first_run = 1

# Need to know the shunt resistance
global SHUNT_OHMS
SHUNT_OHMS = 0.10

# saturation function for anything you want saturated within bounds
def saturate(signal, upper, lower): 
    if signal > upper:
        signal = upper
    if signal < lower:
        signal = lower
    return signal

# This is the function executed by the loop timer, it simply sets a flag which is used to control the main loop
def tick(t): 
    global timer_elapsed
    timer_elapsed = 1

# These functions relate to the configuring of and reading data from the INA219 Current sensor
class ina219: 
    
    # Register Locations
    REG_CONFIG = 0x00
    REG_SHUNTVOLTAGE = 0x01
    REG_BUSVOLTAGE = 0x02
    REG_POWER = 0x03
    REG_CURRENT = 0x04
    REG_CALIBRATION = 0x05
    
    def _init_(self,sr, address, maxi):
        self.address = address
        self.shunt = sr
            
    def vshunt(icur):
        # Read Shunt register 1, 2 bytes
        reg_bytes = ina_i2c.readfrom_mem(icur.address, icur.REG_SHUNTVOLTAGE, 2)
        reg_value = int.from_bytes(reg_bytes, 'big')
        if reg_value > 2**15: #negative
            sign = -1
            for i in range(16): 
                reg_value = (reg_value ^ (1 << i))
        else:
            sign = 1
        return (float(reg_value) * 1e-5 * sign)
        
    def vbus(ivolt):
        # Read Vbus voltage
        reg_bytes = ina_i2c.readfrom_mem(ivolt.address, ivolt.REG_BUSVOLTAGE, 2)
        reg_value = int.from_bytes(reg_bytes, 'big') >> 3
        return float(reg_value) * 0.004
        
    def configure(conf):
        #ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x01\x9F') # PG = 1
        #ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x09\x9F') # PG = /2
        ina_i2c.writeto_mem(conf.address, conf.REG_CONFIG, b'\x19\x9F') # PG = /8
        ina_i2c.writeto_mem(conf.address, conf.REG_CALIBRATION, b'\x00\x00')
        
server_host = '192.168.90.163'  # Replace with your server's IP address
server_port = 5551
client_name = 'bidirectional'  # Replace with your client name
data = None
client_socket = start_client(server_host, client_name, SSID, PASSWORD)


# Here we go, main function, always executes
while True:
    try:
        required_storage = receive_from_server(client_socket, client_name)
        start = utime.time()
        if required_storage != None:
            print("Required Storage = {:.3f}".format(required_storage))
            if first_run:
                # for first run, set up the INA link and the loop timer settings
                ina = ina219(SHUNT_OHMS, 64, 5)
                ina.configure()
                first_run = 0
                
                # This starts a 1kHz timer which we use to control the execution of the control loops and sampling
                loop_timer = Timer(mode=Timer.PERIODIC, freq=1000, callback=tick)
            
            # If the timer has elapsed it will execute some functions, otherwise it skips everything and repeats until the timer elapses
            if timer_elapsed == 1: # This is executed at 1kHz
                va = 1.017*(12490/2490)*3.3*(va_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
                vb = 1.015*(12490/2490)*3.3*(vb_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
                
                vpot_in = 1.026*3.3*(vpot_pin.read_u16()/65536) # calibration factor * potential divider ratio * ref voltage * digital reading
                v_pot_filt[v_pot_index] = vpot_in # Adds the new reading to our array of readings at the current index
                v_pot_index = v_pot_index + 1 # Moves the index of the buffer for next time
                if v_pot_index == 100: # Loops it round if it reaches the end
                    v_pot_index = 0
                vpot = sum(v_pot_filt)/100 # Actual reading used is the average of the last 100 readings
                
                Vshunt = ina.vshunt()
                CL = OL_CL_pin.value() # Are we in closed or open loop mode
                BU = BU_BO_pin.value() # Are we in buck or boost mode?

                duty = 65536-pwm_out # Invert the PWM because thats how it needs to be output for a buck because of other inversions in the hardware
                pwm.duty_u16(duty) # now we output the pwm
                
            else: # Closed Loop Current Control
                stop = False
                while not stop:
                    if required_storage > 0:
                        total_current = -required_storage/vb
                        cap_current = total_current/5
                        print("Capacitor Current = {:.3f}".format(cap_current))
                        print("Vb = {:.3f}".format(vb))
                    else:
                        total_current = -required_storage/va
                        cap_current = total_current/5
                        print("Capacitor Current = {:.3f}".format(cap_current))
                        print("Va = {:.3f}".format(va))
                   
                    vpot = (required_storage/90)
                    
                if CL != 1: # Buck-OL Open loop so just limit the current but otherwise pass through the reference directly as a duty cycle
                    i_err_int = 0 #reset integrator
                    
                    if iL > 2: # Current limiting function
                        pwm_out = pwm_out - 10 # if there is too much current, knock down the duty cycle
                        OC = 1 # Set the OC flag
                        pwm_out = saturate(pwm_out, pwm_ref, min_pwm)
                    elif iL < -2:
                        pwm_out = pwm_out + 10 # We are now below the current limit so bring the duty back up
                        OC = 1 # Reset the OC flag
                        pwm_out = saturate(pwm_out, max_pwm, pwm_ref)
                    else:
                        pwm_out = pwm_ref
                        OC = 0
                        pwm_out = saturate(pwm_out, pwm_ref, min_pwm)
                        
                    duty = 65536-pwm_out # Invert the PWM because thats how it needs to be output for a buck because of other inversions in the hardware
                    pwm.duty_u16(duty) # now we output the pwm
                    
                else: # Closed Loop Current Control
                    stop = False
                    while not stop:
                        if required_storage > 0:
                            total_current = -required_storage/vb
                            cap_current = total_current/5
                            print("Capacitor Current = {:.3f}".format(cap_current))
                            print("Vb = {:.3f}".format(vb))
                        else:
                            total_current = -required_storage/va
                            cap_current = total_current/5
                            print("Capacitor Current = {:.3f}".format(cap_current))
                            print("Va = {:.3f}".format(va))
                    
                        vpot = (required_storage/90)*3.3
                        print("Vpot = {:.3f}".format(vpot))
                        
                        if duty <= 5000 or duty>= 32300:
                            i_ref = 0
                            print("saturating")
                        else:
                            i_ref = saturate(vpot, 0.2, -0.2)
                            print("charge/discharge")
                        
                        i_err = i_ref-iL # calculate the error in voltage
                        i_err_int = i_err_int + i_err # add it to the integral error
                        i_err_int = saturate(i_err_int, 10000, -10000) # saturate the integral error
                        i_pi_out = (kp*i_err)+(ki*i_err_int) # Calculate a PI controller output
                            
                        pwm_out = saturate(i_pi_out,max_pwm,min_pwm) # Saturate that PI output
                        duty = int(65536-pwm_out) # Invert because reasons
                        pwm.duty_u16(duty) # Send the output of the PI controller out as PWM
                        
                        print("i_ref = {:.3f}".format(i_ref))
                        print("iL = {:.3f}".format(iL))
                        print("duty = {:d}".format(duty))
                        
                        end = utime.time()
                        
                        if end-start >= 5:
                            stop = True

                duty = saturate(duty, 65536, 1000)
                
                # Keep a count of how many times we have executed and reset the timer so we can go back to waiting
                count = count + 1
                timer_elapsed = 0
                
                # This set of prints executes every 100 loops by default and can be used to output debug or extra info over USB enable or disable lines as needed
                if count > 100:
                    
                    print("Va = {:.3f}".format(va))
                    print("Vb = {:.3f}".format(vb))
                    print("Vpot = {:.3f}".format(vpot))
                    print("iL = {:.3f}".format(iL))
                    print("OC = {:b}".format(OC))
                    print("CL = {:b}".format(CL))
                    print("BU = {:b}".format(BU))
                    #print("trip = {:b}".format(trip))
                    print("duty = {:d}".format(duty))
                    print("i_err = {:.3f}".format(i_err))
                    #print("i_err_int = {:.3f}".format(i_err_int))
                    #print("i_pi_out = {:.3f}".format(i_pi_out))
                    print("i_ref = {:.3f}".format(i_ref))
                    #print("v_err = {:.3f}".format(v_err))
                    #print("v_err_int = {:.3f}".format(v_err_int))
                    #print("v_pi_out = {:.3f}".format(v_pi_out))
                    #print(v_pot_filt)
                    count = 0

    except (OSError, socket.error) as e:
        print(f"Connection lost: {e}. Attempting to reconnect...")
        if client_socket:
            client_socket.close()
        client_socket = maintain_connection(server_host, client_name)