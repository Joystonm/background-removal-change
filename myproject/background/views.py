# import uuid
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
# from rembg import remove

# def upload_image(request):
#     output_image_url = None

#     if request.method == 'POST' and request.FILES.get('image'):
#         image = request.FILES['image']
#         fs = FileSystemStorage()
#         input_path = fs.save(image.name, image)
#         input_path = fs.path(input_path)

#         with open(input_path, 'rb') as input_file:
#             input_image = input_file.read()

#         #remove background
#         output_image = remove(input_image)

#         #unique filename
#         unique_filename = f"{uuid.uuid4().hex}.png"
#         output_path = fs.path(unique_filename)
#         with open(output_path, 'wb') as output_file:
#             output_file.write(output_image)

#         output_image_url = fs.url(unique_filename)

#     return render(request, 'upload.html', {
#         'output_image': output_image_url,
#     })

import uuid
import cv2
import numpy as np
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter

def upload_image(request):
    output_image_url = None

    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        input_path = fs.save(image.name, image)
        input_path = fs.path(input_path)

        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()

        # Remove background
        output_image_data = remove(input_image)

        # Save temporarily
        temp_output_path = fs.path(f"temp_{uuid.uuid4().hex}.png")
        with open(temp_output_path, 'wb') as temp_output_file:
            temp_output_file.write(output_image_data)

        output_image_cv = cv2.imread(temp_output_path)

        # Upscale 
        upscale_factor = 2  
        output_image_cv = cv2.resize(output_image_cv, None, fx=upscale_factor, fy=upscale_factor, interpolation=cv2.INTER_CUBIC)

        # Enhance sharpness
        output_image_cv = cv2.GaussianBlur(output_image_cv, (0, 0), 2)
        output_image_cv = cv2.addWeighted(output_image_cv, 1.5, cv2.GaussianBlur(output_image_cv, (0, 0), 10), -0.5, 0)

        # Convert to PIL image
        output_image_pil = Image.fromarray(cv2.cvtColor(output_image_cv, cv2.COLOR_BGR2RGB))

        # Convert to Pillow Image for further enhancement
        output_image = Image.open(temp_output_path)

        # Save the final output image
        unique_filename = f"{uuid.uuid4().hex}.png"
        output_path = fs.path(unique_filename)
        output_image.save(output_path)

        # Clean up the temporary file
        fs.delete(temp_output_path)

        output_image_url = fs.url(unique_filename)

    return render(request, 'upload.html', {
        'output_image': output_image_url,
    })

import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
from rembg import remove

def process_image(request):
    if request.method == 'POST' and request.FILES['image'] and request.FILES['background']:
        uploaded_image = request.FILES['image']
        uploaded_background = request.FILES['background']

        fs = FileSystemStorage()
        image_path = fs.save(uploaded_image.name, uploaded_image)
        background_path = fs.save(uploaded_background.name, uploaded_background)

        img = cv2.imread(fs.path(image_path), cv2.IMREAD_UNCHANGED)
        new_bg = cv2.imread(fs.path(background_path), cv2.IMREAD_UNCHANGED)

        # Remove the background using rembg
        no_bg = remove(img)

        # Ensure new_bg has an alpha channel
        if new_bg.shape[2] == 3:
            new_bg = cv2.cvtColor(new_bg, cv2.COLOR_BGR2BGRA)

        # Resize the new background image to match the original image size
        new_bg = cv2.resize(new_bg, (img.shape[1], img.shape[0]))

        # Combine the foreground (no_bg) with the new background
        alpha_s = no_bg[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(0, 3):
            new_bg[:, :, c] = (alpha_s * no_bg[:, :, c] + alpha_l * new_bg[:, :, c])

        # Save the resulting image
        result_path = fs.path('result.jpg')
        cv2.imwrite(result_path, new_bg)

        return render(request, 'replace.html', {'result_url': fs.url('result.jpg')})
    
    return render(request, 'replace.html')
