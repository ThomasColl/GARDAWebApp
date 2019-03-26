import matplotlib.pyplot as plt
import io
import urllib, base64


def retrieve_image_uri(x_data, y_data):
    plt.plot(x_data, y_data)
    fig = plt.gcf()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())

    return 'data:image/png;base64,' + urllib.parse.quote(string)

