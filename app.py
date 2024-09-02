import os
import platform
import time

import GPUtil
import psutil
from termcolor import colored
from flask import Flask, render_template

app = Flask(__name__)

def unit(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def clr(text):
    colorgrn = colored(f"{text}", "green")
    return colorgrn

def monitor():
    time.sleep(1.5)
    gpus = GPUtil.getGPUs()
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    gpus = GPUtil.getGPUs()
    internet = psutil.net_io_counters()
    sys = uname.system
    core = psutil.cpu_count(logical=True)
    cpu_freq_mx = cpufreq.max
    mem_total = (int(mem.total)) / (1024 * 1024 * 1024)

    gpu_list = []
    for gpu in gpus:
        gpu_name = gpu.name
        gpu_total_memory = f"{gpu.memoryTotal}MB"
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_list.append((gpu_name, gpu_total_memory))

    g_pu = (gpu_list[0])[0]
    g_pu_mem = (gpu_list[0])[1]

def monitor():
    time.sleep(1.5)
    gpus = GPUtil.getGPUs()
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    internet = psutil.net_io_counters()
    sys = uname.system
    core = psutil.cpu_count(logical=True)
    cpu_freq_mx = cpufreq.max
    mem_total = (int(mem.total)) / (1024 * 1024 * 1024)

    gpu_list = GPUtil.getGPUs()

    if not gpu_list:
        # If there are no GPUs, set default values
        g_pu = "No GPU"
        g_pu_mem = "N/A"
    else:
        # If there are GPUs, extract information
        g_pu = gpu_list[0].name
        g_pu_mem = f"{gpu_list[0].memoryTotal}MB"

    os.system("clear")
    return {
      "sys": sys,
      "core": core,
      "cpu_percent": psutil.cpu_percent(),
      "cpu_freq_mx": cpu_freq_mx,
      "mem_total": round(mem_total),
      "mem_used": unit(mem.used),
      "mem_percent": mem.percent,
      "gpu": g_pu,
      "gpu_mem": g_pu_mem,
      "data_sent": unit(internet.bytes_sent),
      "data_recv": unit(internet.bytes_recv),
    }


@app.route('/')
def index():
    data = monitor()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)