import cv2
import shutil
import os


def detectar_qr_codes(imagem_path):
    detector = cv2.QRCodeDetector()
    imagem = cv2.imread(imagem_path)

    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(imagem)

    if retval and decoded_info:
        return [texto for texto in decoded_info if texto]
    else:
        return []

def move_to_folder(file_folder, file, qr_code):
    file_path = os.path.join(file_folder, file)
    path_success, path_fail = "imgs_new" , "imgs_new/fail"

    if not os.path.exists(path_success):
        os.makedirs(path_success)
        print("Pasta de sucesso criada!")
        os.makedirs(path_fail)
        print("Pasta de falha criada!")

    if qr_code:
        new_name = f"{qr_code}.jpeg"
        new_address = os.path.join(path_success, new_name)
        shutil.copy(file_path , new_address)

    else:
        new_address = os.path.join(path_fail, file)
        shutil.copy(file_path , new_address)

def main():
    
    folder_path = "imgs-raw"
    print("Processando...")
    for file in os.listdir(folder_path):

        try:
            qr_code_text = detectar_qr_codes(os.path.join(folder_path, file))
            code = qr_code_text[0]
            move_to_folder(file_folder = folder_path, file=file, qr_code = code)
            print(f"[✔] QR code detectado em : {file}")

        except:
            qr_code_text = detectar_qr_codes(os.path.join(folder_path, file))
            move_to_folder(file_folder = folder_path, file=file, qr_code = None)
            print(f"[✖] QR code não detectado em {file}")


if __name__ == "__main__":
    main()