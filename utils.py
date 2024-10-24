import sqlite3
import qrcode
import os


def gen_qr_code(
    data,
    filename,
    size=10,
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
):
    """
    Generates a high-resolution QR code.

    :param data: The data to encode in the QR code.
    :param filename: The filename to save the QR code image.
    :param size: The size of each individual QR code box (default is 10).
    :param version: The version of the QR   code (1-40, higher versions can hold more data).
    :param error_correction: Error correction level (L, M, Q, H).
    """
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=size,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code as a high-resolution PNG file
    img.save(filename)


def get_image(fullname=None, _uuid=None):
    _, cursor = get_db()
    if fullname:
        cursor.execute(
            "SELECT image_path FROM certificates WHERE fullname LIKE ?",
            (f"%{fullname}%",),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return False
    elif _uuid:
        return os.path.join("media", "certificates", f"{_uuid}.png")





def get_db():
    conn = sqlite3.connect("certificates.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            image_path TEXT NOT NULL
        )
    """
    )
    conn.commit()
    return conn, cursor


if __name__ == "__main__":
    gen_qr_code("https://suzani-abdulhakim.uz/biz-haqimizda", "about_us.png")