import spidev
from gpiozero import LED
import struct
import time

class tlc5947():
    def __init__(self,spiport=0,latchpin=25):
        self.latchpin = LED(latchpin)
        self.latchpin.off()
        self.spi = spidev.SpiDev()
        self.spi.open(spiport,0)#chip does not feature chip select for daisy chaining
        self.spi.max_speed_hz = 1000000
        self.pwmbuffer = [0,]*24#24 channels and 12 Bit wide

    
    def _latch(self):
        self.latchpin.on()
        self.latchpin.off()
        return

    def _write(self):
        msg = bytearray()
        for i in range(len(self.pwmbuffer)-1,-1,-1):
            if i % 2:
                msg.extend(struct.pack(">H",(self.pwmbuffer[i]&0xFFF)<<4))
            else:
                msg[-1] |= (self.pwmbuffer[i]>>8) & 0xF
                msg.append(self.pwmbuffer[i]&0xFF)
        xferbuff = list(msg)
        self.spi.xfer(xferbuff)
        self._latch()
        return
        

    def write_pwm(self,list_of_num_val_tuples):
        for num,val in list_of_num_val_tuples:
            if num > 23 or val > 4095:
                raise ValueError
            self.pwmbuffer[num] = val
        return self._write()

    def destroy(self):
        self.spi.close()

def selftest(testmode = "testchannels"):
    tlc_obj = tlc5947()
    maxdim = 50
    stepdim = 4

    if testmode == "testchannels":
        for chan in range(24):
            print("Channel {0}".format(chan))
            for dim in range(0,maxdim,stepdim):
                tlc_obj.write_pwm([(chan,dim)])
                time.sleep(0.1)
            tlc_obj.write_pwm([(chan,0)])

    elif testmode == "rgb":
        #chan0-2 = red,green,blue
        tlc_obj.write_pwm([(0,maxdim),(1,0),(2,0)])#red
        time.sleep(1)
        tlc_obj.write_pwm([(0,0),(1,maxdim),(2,0)])#green
        time.sleep(1)
        tlc_obj.write_pwm([(0,0),(1,0),(2,maxdim)])#blue
        time.sleep(1)
        tlc_obj.write_pwm([(0,maxdim),(1,maxdim),(2,0)])#red and green = yellow
        time.sleep(1)
        tlc_obj.write_pwm([(0,maxdim),(1,0),(2,maxdim)])#red and blue = violett
        time.sleep(1)
        tlc_obj.write_pwm([(0,0),(1,maxdim),(2,maxdim)])#green and blue = celeste
        time.sleep(1)
        tlc_obj.write_pwm([(0,maxdim),(1,maxdim),(2,maxdim)])#red,green and blue = white


    elif testmode == "randomrgb":
        from random import randint
        cnt = 100
        try:
            while cnt:
                tlc_obj.write_pwm([(0,randint(0,maxdim)),(1,randint(0,maxdim)),(2,randint(0,maxdim))])
                time.sleep(1)
                cnt -= 1
        except KeyboardInterrupt:
            tlc_obj.write_pwm([(0,0),(1,0),(2,0)])

    tlc_obj.destroy()
    return    

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-c", "--command", dest="command",
                      default='rgb',
                      help="COMMAND to execute", metavar="COMMAND")     
    (options, args) = parser.parse_args()
    
    selftest(testmode = options.command)
    



        
        
