import qrcode
import cv2
from pyzbar.pyzbar import decode

def create_id_qr(id_number):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(id_number))
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        filename = f"qrcode/{id_number}.png"
        qr_image.save(filename)
        print(f"QR code yaratildi: {filename}")
        
    except Exception as e:
        print(f"Xatolik: {e}")


def read_qr_code(filename):
    try:
        image = cv2.imread(filename)
        decoded_objects = decode(image)
        for obj in decoded_objects:
            # print("Topilgan ma'lumot:", obj.data.decode('utf-8'))
            return obj.data.decode('utf-8')
            
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None
