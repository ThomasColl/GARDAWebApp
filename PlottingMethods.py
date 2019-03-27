from datetime import datetime

import matplotlib.pyplot as plt
import io
import urllib, base64


def retrieve_image_uri(x_data, y_data):
    x_data = fix_x_axis(x_data)
    print(x_data)
    plt.scatter(x_data, y_data)
    plt.grid(True)
    display_axis = []
    for x in range(len(x_data)):
        if x == 0 or x == len(x_data)-1:
            display_axis.append(x_data[x])
        else:
            display_axis.append("")
    plt.xticks(x_data, display_axis)
    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return 'data:image/png;base64,' + urllib.parse.quote(string)


def fix_x_axis(x):
    updated_axis = []
    for entry in x:
        updated_axis.append(datetime.utcfromtimestamp(float(entry)).strftime('%H:%M:%S %d-%m-%Y'))
    return updated_axis
