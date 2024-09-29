import qrcode


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
    :param version: The version of the QR code (1-40, higher versions can hold more data).
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
