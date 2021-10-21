from pdf2image import convert_from_path

class Convert:

    def conversion_to_jpg(path):
        images = convert_from_path(path)

        for i in range(len(images)):
            images[i].save(f'Schedule_{str(i)}.jpg', 'JPEG')
