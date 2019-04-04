from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import io
import urllib, base64


def retrieve_image_uri(x_data, y_data):
    plt.clf()
    x, y = plot_by_day(x_data, y_data)
    plt.plot(x, y)

    x_display = [''] * (len(x) - 2)
    x_display.insert(0, x[0])
    x_display.append(x[-1])

    plt.xlabel("Date")
    plt.xticks(x, x_display)
    plt.ylabel("No. Requests")

    image = plt.gcf()

    buf = io.BytesIO()
    image.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    
    return 'data:image/png;base64,' + urllib.parse.quote(string)


def fix_x_axis(x):
    updated_axis = []
    for entry in x:
        updated_axis.append(datetime.utcfromtimestamp(float(entry)).strftime('%Y-%m-%d'))
    return updated_axis


def plot_by_day(x, y):
    x = fix_x_axis(x)

    return_dict = {}

    for index, value in enumerate(x):
        if value not in return_dict:
            return_dict[value] = 1
        else:
            return_dict[value] += 1

    return list(return_dict.keys()), list(return_dict.values())

