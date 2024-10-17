# Background Removal & Replacement

This project is a Django-based web application for removing image backgrounds and replacing them with a new background. It leverages image processing techniques, using `rembg` for background removal and OpenCV for image enhancement and replacement.

## Features

- **Background Removal**: Removes the background of uploaded images using the `rembg` library.
- **Image Upscaling**: Upscales the image to improve clarity.
- **Sharpness Enhancement**: Enhances the sharpness using OpenCV.
- **Background Replacement**: Blends a new background with the image after removing the original.
- **Web Interface**: Simple and user-friendly interface for file uploads and image processing.

## Requirements

- Python 
- Django 
- OpenCV
- rembg
- Pillow
- NumPy

## Installation

1. Activate the environment:

    ```bash
    ./project/Scripts/Activate                                            
    ```

2. Navigate to the project directory:

    ```bash
    cd  myproject   
    ```

3. Run the Django server:

    ```bash
    python manage.py runserver
    ```

## Usage

### 1. Background Removal

Navigate to `/process_image/` to upload an image. The app removes the background, upscales the image, and enhances its sharpness. The processed image will be available for download.

### 2. Background Replacement

Navigate to `/replace/` to upload an image and a new background. The app will remove the background from the image and blend it with the new background.
