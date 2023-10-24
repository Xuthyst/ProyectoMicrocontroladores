#!/usr/bin/python3
import serial
from matplotlib import pyplot as plt
import numpy as np
import struct
from PIL import Image
ser = serial.Serial(
    port='COM3',  # Use the correct serial port
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2  # Adjust the timeout as needed
)

print("Connected to: " + ser.portstr)


num_datos = 30  
#num_datos = int(input("Please enter the number of data points to collect: "))

contador_datos = 0

while contador_datos < num_datos:
    linea_serie = ser.readline().decode().strip()
    if linea_serie:
        cleaned_line = linea_serie.replace(' ', '')
        hex_values = cleaned_line.split(',')
        result_list = [int(value, 16) for value in hex_values if value]
        raw_bytes = np.array(result_list, dtype="i2")
        image = np.zeros((len(raw_bytes),3), dtype=int)

        # Loop through all of the pixels and form the image
        for i in range(len(raw_bytes)):
            #Read 16-bit pixel
            pixel = struct.unpack('>h', raw_bytes[i])[0]

            #Convert RGB565 to RGB 24-bit
            r = ((pixel >> 11) & 0x1f) << 3;
            g = ((pixel >> 5) & 0x3f) << 2;
            b = ((pixel >> 0) & 0x1f) << 3;
            image[i] = [r,g,b]


        image = np.reshape(image,(144, 176, 3)) #QCIF resolution
        #plt.imshow(image, cmap='gray', vmin=0, vmax=65535)  # Adjust vmin and vmax as needed
        #plt.show()
        # Save the image as a JPG file
        image_pil = Image.fromarray(image.astype(np.uint8))
        image_pil.save(f"imagenes/output_image{contador_datos}.jpg")
        contador_datos += 1

ser.close()