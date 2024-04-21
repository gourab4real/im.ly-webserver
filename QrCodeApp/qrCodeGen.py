import qrcode
import qrcode.image.svg
from io import BytesIO
from PIL import Image
import base64

class QRCodeGen:
    def generate_qr(url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert the PyPNGImage to a PIL Image
        img_pil = img.get_image()
        
        # Create a BytesIO object to hold the image data
        img_buffer = BytesIO()
        # Save the PIL Image to the BytesIO object
        img_pil.save(img_buffer, format='PNG')
        # Seek to the beginning of the BytesIO object
        img_buffer.seek(0)
        img_data = img_buffer.read()

        img_base64 = base64.b64encode(img_data).decode('utf-8')

        return img_base64