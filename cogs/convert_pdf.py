from pdf2image import convert_from_bytes

class Convert:

    def conversion_to_jpg(mem_file):
        images = convert_from_bytes(mem_file)

        for i in range(len(images)):
            images[i].save(f'Schedule_{str(i)}.jpg', 'JPEG')
