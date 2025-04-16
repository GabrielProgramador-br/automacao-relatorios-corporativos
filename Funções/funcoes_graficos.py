import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


def salvando_imagem(plt, image_name):
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return image