/* 
Exmple can be built with this command 
nvcc -I /usr/local/cuda-8.0/include -lnvidia-ml -L /usr/lib/nvidia-361 CheckDevice.c -o CheckDeviceParameters
*/
#include <stdio.h>
#include <nvml.h>


int main()
{
    nvmlReturn_t result;
    unsigned int device_count, i,temp, power;
    // First initialize NVML library
    result = nvmlInit();
    if (NVML_SUCCESS != result)
    {
        printf("Failed to initialize NVML: %s\n", nvmlErrorString(result));

       return 1;
    }

    result = nvmlDeviceGetCount(&device_count);
    if (NVML_SUCCESS != result)
    {
        printf("Failed to query device count: %s\n", nvmlErrorString(result));
        
    }
    printf("Found %d device%s\n\n", device_count, device_count != 1 ? "s" : "");

    printf("Listing devices:\n");
    for (i = 0; i < device_count; i++)
    {
        nvmlDevice_t device;
	nvmlUnit_t unit;
	//Buffer size guaranteed to be large enough for nvmlDeviceGetName
        char name[NVML_DEVICE_NAME_BUFFER_SIZE];
        nvmlPciInfo_t pci;
        nvmlComputeMode_t compute_mode;
        nvmlMemory_t memory;
	nvmlPSUInfo_t psu;
	nvmlTemperatureSensors_t sensorType;
	nvmlUtilization_t utilization;
	
	result = nvmlDeviceGetHandleByIndex(i, &device);
        if (NVML_SUCCESS != result)
        {
            printf("Failed to get handle for device %i: %s\n", i, nvmlErrorString(result));     
        }

        result = nvmlDeviceGetName(device, name, NVML_DEVICE_NAME_BUFFER_SIZE);
        if (NVML_SUCCESS != result)
        {
            printf("Failed to get name of device %i: %s\n", i, nvmlErrorString(result));
            
        }
	//Get GPU pci information
        result = nvmlDeviceGetPciInfo(device, &pci);
        if (NVML_SUCCESS != result)
        {
            printf("Failed to get pci info for device %i: %s\n", i, nvmlErrorString(result));
        }
	else
	{
        printf("%d. %s [%s]\n", i, name, pci.busId);
        }
	//GPU utilization
        result = nvmlDeviceGetUtilizationRates(device, &utilization);
        if (NVML_SUCCESS != result)
        {
            printf("Failed to get utilization info for device %i: %s\n", i, nvmlErrorString(result));
        }
	else
	{
        printf("GPU Utilization  %d%%\n", utilization.gpu);
        printf("Memory Utilization  %d%%\n", utilization.memory);
	}
	//Get GPU memory information
	result = nvmlDeviceGetMemoryInfo(device, &memory);
        if (NVML_SUCCESS != result)
        {
            printf("Failed to get memory info for device %i: %s\n", i, nvmlErrorString(result));
        }
	else
	{
            printf("GPU Memory In Use MB %f\n", memory.used/1000000.);
           // printf("GPU Memory Free MB %f\n", memory.free/1000000.);
	}
	//Get GPU power usage
        result=nvmlDeviceGetPowerUsage (device,&power);
	if (NVML_SUCCESS!=result)
        {
            printf("Failed to get power info for device %i: %s\n", i, nvmlErrorString(result));
	}
	else
	{
	    printf("Power used (W) %dW\n", power/1000);
        }
	//Get GPU Temp
	result=nvmlDeviceGetTemperature (device, 0, &temp);
	if (NVML_SUCCESS!=result)
        {
            printf("Failed to get temperature info for device %i: %s\n", i, nvmlErrorString(result));
        }
	else
	{
	printf("GPU Temperature (C) %d\n", temp);
	}
    }
    //Shutdown nvml library
    result = nvmlShutdown();
    if (NVML_SUCCESS != result)
        printf("Failed to shutdown NVML: %s\n", nvmlErrorString(result));

    printf("All done.\n");

    return 0;
}
