import qrcode

def generate_qr_code(user_id, user_name):
    data = f"user_{user_id}"
    img = qrcode.make(data)
    img.save(f"static/qr/{user_name}_qr.png")

if __name__ == '__main__':
    # Example users
    users = [
        (1, "john_doe"),
        (2, "jane_doe")
    ]

    for user_id, user_name in users:
        generate_qr_code(user_id, user_name)
        print(f"QR Code generated for {user_name}.")
