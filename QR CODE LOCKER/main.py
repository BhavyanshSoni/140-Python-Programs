import qrcode
from PIL import Image

def generate_qr(data, filename):
    qr = qrcode.make(data)
    qr.save(filename)
    print(f"QR code saved as {filename}")

def read_qr(filename):
    # PIL + pyzbar needed for reading QR; skipping due to complexity
    print("Reading QR code functionality to be added.")

def main():
    print("=== QR Code Locker ===")
    while True:
        choice = input("1. Generate QR\n2. Exit\n> ")
        if choice == '1':
            data = input("Enter data to encode: ")
            filename = input("Enter filename to save (e.g. code.png): ")
            generate_qr(data, filename)
        elif choice == '2':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
