import RPi.GPIO as gpio
import time,picamera,requests

def send_img(n):
    global total_area;
    global host
    global url
    global p_no
    
    files = {
        "filename" : open(url,"rb")
        }
    values = {
        "project_no" : p_no,
        "total_area" : total_area,
        "using_area" : n
        }

    requests.post(host,files=files,data=values)

    print "Infomation sending completed "

''' ----------------------------------------------------------------'''

def capture_camera(n):
    global url
    print "Update Parking spaces Picture"
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(3)
        camera.capture(url)
        camera.stop_preview()

        print "Infomation sending completed "
        #send_img(n)

''' ----------------------------------------------------------------'''

def ultrasono(total):
    
    temp = 0
    gpio.setmode(gpio.BCM)

    trig = 6
    echo = 13
    trig2 = 16
    echo2 = 20

    print "start"
    
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    gpio.setup(trig2, gpio.OUT)
    gpio.setup(echo2, gpio.IN)

    try :
        while True :
            num = 0
            
            gpio.output(trig, False)
            time.sleep(0.5)

            gpio.output(trig, True)
            time.sleep(0.00001)
            gpio.output(trig, False)
            
            while gpio.input(echo) == 0 :
                pulse_start = time.time()
            while gpio.input(echo) == 1 :
                pulse_end = time.time()

                
            gpio.output(trig2, False)
            time.sleep(0.5)

            gpio.output(trig2, True)
            time.sleep(0.00001)
            gpio.output(trig2, False)

            
            while gpio.input(echo2) == 0 :
                pulse_start2 = time.time()
            while gpio.input(echo2) == 1 :
                pulse_end2 = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance,2)
            
            pulse_duration2 = pulse_end2 - pulse_start2
            distance2 = pulse_duration2 * 17000
            distance2 = round(distance2,2)

            if(distance <= 20) :
                num = num + 1
            if(distance2 <= 20) :
                num = num + 1
                
            print "Available spaces : " + str((total-num))

            if(temp != num):
                print "Parking spaces number changed!"
                time.sleep(3)
                capture_camera(num)
            
            
            temp = num
            
    except :
        gpio.cleanup()


''' ----------------------------------------------------------------'''

p_no = "1"
c_no = "1"
total_area = 10

host = "http://117.17.187.138:12345/adminWeb/upload.jsp"
url = "/home/pi/Desktop/" + p_no + "_" + c_no + ".jpg"

ultrasono(total_area)
