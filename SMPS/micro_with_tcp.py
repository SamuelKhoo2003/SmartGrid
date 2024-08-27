from machine import Pin, I2C, ADC, PWM, Timer
from tcp_client import Tcp_client, connect_to_wifi
import time
import ujson

# Set up some pin allocations for the Analogues and switches
va_pin = ADC(Pin(28))
vb_pin = ADC(Pin(26))
vpot_pin = ADC(Pin(27))
OL_CL_pin = Pin(12, Pin.PULL_UP)
BU_BO_pin = Pin(2, Pin.PULL_UP)

# Set up the I2C for the INA219 chip for current sensing
ina_i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Some PWM settings
pwm = PWM(Pin(9))
pwm.freq(100000)
min_pwm = 1000
max_pwm = 64536
pwm_out = min_pwm
pwm_ref = 30000

# Error signals
trip = 0
OC = 0

# Potentiometer noise filtering
v_pot_filt = [0] * 100
v_pot_index = 0

# PID controller gains
i_ref = 0 
i_err = 0
i_err_int = 0
i_pi_out = 0
kp = 100
ki = 300

# Control logic signals
global timer_elapsed
timer_elapsed = 0
count = 0
first_run = 1
hold_vpot = 1

# Shunt resistance
global SHUNT_OHMS
SHUNT_OHMS = 0.10

# Saturation function
def saturate(signal, upper, lower):
    return max(min(signal, upper), lower)

# Timer callback
def tick(t):
    global timer_elapsed
    timer_elapsed = 1

# INA219 class
class ina219:
    REG_CONFIG = 0x00
    REG_SHUNTVOLTAGE = 0x01
    REG_BUSVOLTAGE = 0x02
    REG_POWER = 0x03
    REG_CURRENT = 0x04
    REG_CALIBRATION = 0x05
    
    def __init__(self, sr, address):
        self.address = address
        self.shunt = sr
            
    def vshunt(self):
        try:
            reg_bytes = ina_i2c.readfrom_mem(self.address, self.REG_SHUNTVOLTAGE, 2)
            reg_value = int.from_bytes(reg_bytes, 'big')
            if reg_value > 2**15:  
                reg_value -= 2**16
            return float(reg_value) * 1e-5
        except Exception as e:
            print(f"INA219 vshunt error: {e}")
            return 0
        
    def vbus(self):
        try:
            reg_bytes = ina_i2c.readfrom_mem(self.address, self.REG_BUSVOLTAGE, 2)
            reg_value = int.from_bytes(reg_bytes, 'big') >> 3
            return float(reg_value) * 0.004
        except Exception as e:
            print(f"INA219 vbus error: {e}")
            return 0
        
    def configure(self):
        try:
            ina_i2c.writeto_mem(self.address, self.REG_CONFIG, b'\x19\x9F')
            ina_i2c.writeto_mem(self.address, self.REG_CALIBRATION, b'\x00\x00')
        except Exception as e:
            print(f"INA219 configure error: {e}")

name = "cell"

try:
    connect_to_wifi()
    print("WiFi connected")

    client = Tcp_client(host='192.168.90.7', port=9998, client_name=name, blocking=True)
    client.connect()
    time.sleep(2)
except Exception as e:
    print(f"TCP client setup error: {e}")

data = {
    'name': name,
    'value': 1234,
    'timestamp': time.time()
}

try:
    while True:
        if first_run:
            ina = ina219(SHUNT_OHMS, 0x40)
            ina.configure()
            first_run = 0
            
            loop_timer = Timer(mode=Timer.PERIODIC, freq=1000, callback=tick)
        
        if timer_elapsed == 1:
            va = 1.017 * (12490 / 2490) * 3.3 * (va_pin.read_u16() / 65536)
            vb = 1.015 * (12490 / 2490) * 3.3 * (vb_pin.read_u16() / 65536)
            
            if 1 <= hold_vpot <= 7500:
                vpot = 1.19
                hold_vpot += 1
            elif hold_vpot > 7500:
                vpot = 1.19
                hold_vpot = 0
            else:
                vpot_in = 1.026 * 3.3 * (vpot_pin.read_u16() / 65536)
                v_pot_filt[v_pot_index] = vpot_in
                v_pot_index = (v_pot_index + 1) % 100
                vpot = sum(v_pot_filt) / 100
                vpot = saturate(vpot, 1.35, 0.75)
            
            Vshunt = ina.vshunt()
            CL = OL_CL_pin.value()
            BU = BU_BO_pin.value()
                
            min_pwm = 0 
            max_pwm = 64536
            iL = Vshunt / SHUNT_OHMS
            pwm_ref = saturate(65536 - int((vpot / 3.3) * 65536), max_pwm, min_pwm)
                  
            if CL != 1:
                i_err_int = 0
                
                if iL > 2:
                    pwm_out = pwm_out - 10
                    OC = 1
                    pwm_out = saturate(pwm_out, pwm_ref, min_pwm)
                elif iL < -2:
                    pwm_out = pwm_out + 10
                    OC = 1
                    pwm_out = saturate(pwm_out, max_pwm, pwm_ref)
                else:
                    pwm_out = pwm_ref
                    OC = 0
                    pwm_out = saturate(pwm_out, pwm_ref, min_pwm)
                    
                duty = 65536 - pwm_out
                pwm.duty_u16(duty)
                
            else:
                i_ref = saturate(vpot - 1.66, 1.5, -1.5)
                i_err = i_ref - iL
                i_err_int = i_err_int + i_err
                i_err_int = saturate(i_err_int, 10000, -10000)
                i_pi_out = (kp * i_err) + (ki * i_err_int)
                
                pwm_out = saturate(i_pi_out, max_pwm, min_pwm)
                duty = int(65536 - pwm_out)
                pwm.duty_u16(duty)
            
            data['value'] = pwm_out
            data['timestamp'] = time.time()
            
            try:
                client.send_data(data)
                time.sleep(1)  # Wait a moment before receiving
                response = client.receive_data()
                print(f"Received response: {response}")
                if response is None:
                    raise ValueError("Received None response")
            except OSError as e:
                print(f"OSError during send/receive: {e}")
                client.maintain_connection()
            except ValueError as e:
                print(f"ValueError: {e}")
                client.maintain_connection()
            except Exception as e:
                print(f"General error during send/receive: {e}")
                client.maintain_connection()
            
            timer_elapsed = 0
            count += 1
            if count > 100:
                print(f"Va = {va:.3f}")
                print(f"Vb = {vb:.3f}")
                print(f"Vpot = {vpot:.3f}")
                print(f"iL = {iL:.3f}")
                print(f"OC = {OC}")
                print(f"CL = {CL}")
                print(f"BU = {BU}")
                print(f"Duty = {duty}")
                print(f"Hold_vpot = {hold_vpot}")
                print(f"i_err = {i_err:.3f}")
                print(f"i_ref = {i_ref:.3f}")
                count = 0

            time.sleep(5)  # Wait for 5 seconds before the next iteration

except Exception as e:
    print(f"Main loop error: {e}")

finally:
    if client:
        client.close()

