import uuid
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rembg import remove

def upload_image(request):
    output_image_url = None

    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        input_path = fs.save(image.name, image)
        input_path = fs.path(input_path)

        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()

        #remove the background
        output_image = remove(input_image)

        #unique filename
        unique_filename = f"{uuid.uuid4().hex}.png"
        output_path = fs.path(unique_filename)
        with open(output_path, 'wb') as output_file:
            output_file.write(output_image)

        output_image_url = fs.url(unique_filename)

    return render(request, 'upload.html', {
        'output_image': output_image_url,
    })
