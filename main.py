from flask import Flask, render_template
from flask import request

import sys
import time

import gradients
from ledstrip import LEDStrip

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
        colour_list = gradients.poly_gradient([gradient, gradients.darken(gradient), gradient], step_size)
        while cycler:
            for x in colour_list:
                if cycler == False:
                    return 'Stopped'
                strip.setcolourrgb(x[0],x[1],x[2])
                time.sleep(period)

    else:
        colour_list = gradients.presets(gradient, step_size)
        while cycler:
            for x in colour_list:
                if cycler == False:
                    return 'Stopped'
                strip.setcolourrgb(x[0],x[1],x[2])
                time.sleep(period)


@app.route('/send_req', methods = ['POST'])
def postJsonHandler():
    global cycler
    global period

    print (request.is_json)
    content = request.get_json()

    for key in content:
        print("Key: {} -> Content: {}".format(key,content[key]))

    if 'colour' in content.keys():
        cycler = False
        print(content['colour'])
        strip.setcolourhex(content['colour'][1:])
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
    step_size = int(sys.argv[2])
    period = 0.05
    CLK = 18
    DAT = 17
    strip = LEDStrip(CLK, DAT)

    app.run(host=sys.argv[1], port=80)
