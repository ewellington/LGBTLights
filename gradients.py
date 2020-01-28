#import colour
import colorsys

def colour_conversion(gradient):
    converted_gradient = []
    for x in gradient:
        #time.sleep(0.1)
        #change_colour(int(x.hue * 255))
        #time.sleep(0.1)
        c = colorsys.rgb_to_hsv(x[0]/255, x[1]/255, x[2]/255)
        #print(c)
        converted_gradient.append({ 'hue' : str(int(c[0] * 255)), 'sat' : str(int(c[1] * 255)), 'val' : str(int(c[2] * 255)) })

    return converted_gradient


def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
                "{0:x}".format(v) for v in RGB])


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
        int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
        for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return RGB_list


def poly_gradient(colour_list, step_size):
    gradient = []

    for x in range(len(colour_list)-1):
        gradient += linear_gradient(colour_list[x], colour_list[x+1], step_size)

    return gradient


def darken(hexcolor, factor=0.2):
    rgb = hex_to_RGB(hexcolor)
    h, l, s = colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = colorsys.hls_to_rgb(h, l, s)

    print(r*255,g*255,b*255)

    return RGB_to_hex([round(r*255,0), round(g*255,0), round(b*255,0)])


def presets(key='pride',step_size='10'):
    pride_flags = {
        'bi' : ["#ff0040", "#ff00ff", "#0000ff", "#ff0040"],
        'trans' : ["#55CDFC", "#FFFFFF", "#f96bf5", "#55CDFC"],
        'pan' : ["#FF1B8D", "#FFFF00", "#1BB3FF", "#FF1B8D"],
        'pride' : ["#FF0000", "#ff4800", "#FFFF00", "#00ff00", "#0000ff", "#ff00ff","#FF0000"],
        'lesbian' : ["#D63226","#F17628","#F79858","#FFFFFF","#D162A4","#BA5895","#A42268","#D63226"]
    }

    return poly_gradient(pride_flags[key], step_size)
