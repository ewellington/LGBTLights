from flask import Flask, render_template
from flask import request

import serial
import sys
import time

import gradients

app = Flask(__name__)
cycler = False

#def sendHSLtoSerial(hslcolor):
#    ser = serial.Serial(port)
#    hslcolor = int(hslcolor)
#    hslcolor = str(hslcolor) + '\n'
#    print(hslcolor)
#
#    print(ser.readline())
#    print(ser.name)
#    ser.write(hslcolor.encode())
#    #ser.write(b'constant')
#    print(ser.readline())
#    ser.close()

def gradient_cycler(gradient):
    global cycler
    global step_size
    global period

    if gradient[0] == '#':
        colour_list = gradients.colour_conversion(gradients.poly_gradient([gradient, "#000000", gradient], step_size))
        while cycler:
            for x in colour_list:
                if cycler == False:
                    return 'Stopped'
                hsv_color = "{},{},{}\n".format( x['hue'], x['sat'], x['val'] )
                ser.write(hsv_color.encode())
                time.sleep(period)

    else:
        colour_list = gradients.presets(gradient, step_size)
        while cycler:
            for x in colour_list:
                if cycler == False:
                    return 'Stopped'
                hsv_color = "{},{},{}\n".format( x['hue'], x['sat'], x['val'] )
                ser.write(hsv_color.encode())
                time.sleep(period)


@app.route('/send_req', methods = ['POST'])
def postJsonHandler():
    global cycler
    global period

    print (request.is_json)
    content = request.get_json()

    for key in content:
        print("Key: {} -> Content: {}".format(key,content[key]))

    if 'h' in content:
        cycler = False
        hsv_color = "{0:.0f},{1:.0f},{2:.0f}\n".format( ((content['h']/360)*255), ((content['s']/100)*255), ((content['v']/100)*255) )
        print(hsv_color)
        ser.write(hsv_color.encode())
        return 'Completed Successfully'
    elif 'period' in content.keys():
        period = float(content['period'])
        print("Period set")
        return 'Set period time to {}s'.format(period)
    else:
        cycler = False
        print(content)

        cycler = True
        print(gradient_cycler(content['gradient']))

        return 'Stopped gradient'


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == "__main__":
    step_size = int(sys.argv[3])
    period = 0.05

    ser = serial.Serial(sys.argv[2], 19200, timeout=0,                     parity=serial.PARITY_EVEN, rtscts=1)
    print(ser.read(100))

    app.run(host=sys.argv[1], port=80)
    ser.close()
