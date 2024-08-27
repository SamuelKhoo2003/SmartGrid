from machine import Pin, I2C, ADC, PWM
from PID import PID
import random
import utime

vret_pin = ADC(Pin(26))
vout_pin = ADC(Pin(28))
vin_pin = ADC(Pin(27))
pwm = PWM(Pin(0))
pwm.freq(100000)
pwm_en = Pin(1, Pin.OUT)
vret_sum = 0
total_vret_readings = 0
tolerance = 5

pid = PID(0.2, 10, 0, setpoint=0.3, scale='ms')

count = 0
pwm_out = 0
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
    pwm_en.value(1)
    required_power = random.randint(1,15)/10
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
        print("Current Power:",current_Power)
        print("Required Power:",required_power)
        if current_Power< required_power*(1-tolerance/100):
            pwm_out+=100
        elif current_Power > required_power*(1+tolerance/100):
            pwm_out-=100
        elif required_power*(1-tolerance/100) <= current_Power <= required_power*(1+tolerance/100):
            print("Power Achieved")
            stop = True
        print(pwm_out)
    


    utime.sleep(1)

    print("Vin = {:.3f}".format(vin))
    print("Vout = {:.3f}".format(vout))
    print("Vret = {:.3f}".format(vret))
    print("Average Vret = {:.3f}".format(average_vret))
    print("Duty = {:.0f}".format(pwm_out))
    
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



