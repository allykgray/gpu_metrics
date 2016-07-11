#!/usr/bin/env  python
#this script uses nvidia-ml-py to push strings of data to graphite. 
#you need to install nvidia-ml-py to run this script as well as grafana, graphite, and carbon if you want to post the information 
#https://pypi.python.org/pypi/nvidia-ml-py/
 
import socket 
import time
from pynvml import *

#nvmlInit()

DELAY= 10

CARBON_SERVER='127.0.0.1'
CARBON_PORT=2003
timestamp=int(time.time())

#DriverVersion=nvmlSystemGetDriverVersion()
#deviceCount=nvmlDeviceGetCount()

#gpu_number=1

def get_gpumeminfo(gpu_handle):
	gpumeminfo = nvmlDeviceGetMemoryInfo(gpu_handle)
	return gpumeminfo

def get_gpupciethroughput(gpu_handle):
        tx_bytes = nvmlDeviceGetPcieThroughput(gpu_handle, NVML_PCIE_UTIL_TX_BYTES)/10.**3 # units KB/s converted to MB/s
        rx_bytes = nvmlDeviceGetPcieThroughput(gpu_handle, NVML_PCIE_UTIL_RX_BYTES)/10.**3 # unite KB/s converted to MB/s
	return tx_bytes,rx_bytes	

def get_clockinfo(gpu_handle):
	graphic_clocks = nvmlDeviceGetClockInfo(gpu_handle, NVML_CLOCK_GRAPHICS)
	mem_clocks = nvmlDeviceGetClockInfo(gpu_handle, NVML_CLOCK_MEM)
	return graphic_clocks,mem_clocks

def send_message(message):
	print 'sending message:\n%s' % message
	sock = socket.socket()
	sock.connect((CARBON_SERVER, CARBON_PORT))
	sock.sendall(message)
	sock.close()


if __name__ == '__main__':
	while True:
		timestamp = int(time.time())
		nvmlInit()
        	deviceCount = nvmlDeviceGetCount()
		for i in range(deviceCount):
			gpu_handle = nvmlDeviceGetHandleByIndex(i)
			gpumeminfo=get_gpumeminfo(gpu_handle)
			(gpu_tx,gpu_rx)=get_gpupciethroughput(gpu_handle)
			(graph_clk,mem_clk)=get_clockinfo(gpu_handle)
        		lines = [
			'gpu.%s.gpudriver %s %d' % (i,nvmlSystemGetDriverVersion(),timestamp), #posting GPU driver
           		'gpu.%s.gpumem_total %s %d' % (i, gpumeminfo.total/10.**9, timestamp),#posting as GB
            		'gpu.%s.gpumem_free %s %d' % (i, gpumeminfo.free/10.**9, timestamp), #posting as GB
            		'gpu.%s.gpumem_used %s %d' % (i, gpumeminfo.used/10.**9, timestamp), #posting as GB
	    		'gpu.%s.gpu_tx_bytes %s %d' % (i,gpu_tx, timestamp), #posting at MB/s
	    		'gpu.%s.gpu_rx_bytes %s %d' % (i,gpu_rx, timestamp), #Posting as MB/s
			'gpu.%s.gpu_graphic_clk %s %d' % (i,graph_clk, timestamp), #posting as MHz
			'gpu.%s.gpu_mem_clk %s %d'  % (i,graph_clk, timestamp), #posting as MHz
			'gpu.%s.gpu_power_usage %s %d' %(i,nvmlDeviceGetPowerUsage(gpu_handle) / 1000.0,timestamp), #posting as W

        		]
        		message = '\n'.join(lines) + '\n'
        		#print 'sending message:\n%s' % message
			send_message(message)
		nvmlShutdown() 
		#send_message(message1)

		time.sleep(DELAY)

