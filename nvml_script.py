#!/usr/bin/env python

import socket
import time
from pynvml import *

nvmlInit()
strResult=''
gpu=0 #GPU 0
handle = nvmlDeviceGetHandleByIndex(gpu)
print 'GPU name ' + str(nvmlDeviceGetName(handle))
print 'Driver Version ' + str(nvmlSystemGetDriverVersion())
print 'VBOIS Version '+str(nvmlDeviceGetVbiosVersion(handle))
util = nvmlDeviceGetUtilizationRates(handle)
print 'GPU Utilization ' + str(util.gpu) + ' %'
print 'GPU Memory Utilization ' +  str(util.memory) + ' %'
#GPU PCIe Throughput
tx_bytes = nvmlDeviceGetPcieThroughput(handle, NVML_PCIE_UTIL_TX_BYTES)
strResult += 'PCIe Throughput tx ' + str(tx_bytes) + ' KB/s' 

rx_bytes = nvmlDeviceGetPcieThroughput(handle, NVML_PCIE_UTIL_RX_BYTES)
strResult += '        PCIe Throughput rx ' + str(rx_bytes) + ' KB/s'
print strResult
nvmlShutdown()

