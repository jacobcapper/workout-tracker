import qrcode
import os

def generate_qr_code(user_id, user_name):
    """Generates a QR code for the user and saves it to the static/qr directory."""
    data = f"user_{user_id}"  # Data encoded into the QR code (user ID in this case)
    img = qrcode.make(data)
    img.save(f"static/qr/{user_name}_qr.png")
    print(f"QR Code generated for {user_name}.")

def main():
    """Prompts the user for input and generates QR codes for each user."""
    
    # Create the static/qr directory if it doesn't exist
    if not os.path.exists('static/qr'):
        os.makedirs('static/qr')
    
    # Ask how many users to add
    num_users = int(input("How many users do you want to add? "))

    for user_id in range(1, num_users + 1):
        user_name = input(f"Enter name for user {user_id}: ")
        generate_qr_code(user_id, user_name)

if __name__ == '__main__':
    main()
