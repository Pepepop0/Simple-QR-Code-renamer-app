import cv2
import shutil
import os


def detectar_qr_codes(imagem_path):
    """Detector robusto usando somente OpenCV (compatível com Python 3.13)."""

    imagem = cv2.imread(imagem_path)
    if imagem is None:
        return []

    # Pré-processamento para melhorar detecção
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # melhora contraste

    detector = cv2.QRCodeDetector()

    # Tenta detectar múltiplos QR Codes
    retval, decoded_info, points, _ = detector.detectAndDecodeMulti(gray)

    resultados = []

    if retval and decoded_info:
        for texto in decoded_info:
            if texto.strip():
                resultados.append(texto)

    # Fallback: tenta versão single QR se falhar
    if not resultados:
        texto, pts, _ = detector.detectAndDecode(gray)
        if texto.strip():
            resultados.append(texto)

    return resultados



def move_to_folder(file_folder, file, qr_code):
    file_path = os.path.join(file_folder, file)
    path_success, path_fail = "imgs_new", "imgs_new/fail"

    if not os.path.exists(path_success):
        os.makedirs(path_success)
        print("Pasta de sucesso criada!")
        os.makedirs(path_fail)
        print("Pasta de falha criada!")

    if qr_code:
        safe_name = qr_code.replace("/", "_").replace("\\", "_").replace(":", "_")
        new_name = f"{safe_name}.jpeg"
        new_address = os.path.join(path_success, new_name)
        shutil.copy(file_path, new_address)
    else:
        new_address = os.path.join(path_fail, file)
        shutil.copy(file_path, new_address)



def main():
    folder_path = "imgs-raw"
    print("Processando...")

    for file in os.listdir(folder_path):
        caminho = os.path.join(folder_path, file)

        try:
            qr_code_text = detectar_qr_codes(caminho)

            if len(qr_code_text) == 0:
                raise Exception("Nenhum código encontrado")

            code = qr_code_text[0]
            move_to_folder(file_folder=folder_path, file=file, qr_code=code)
            print(f"[✔] QR code detectado em: {file} → {code}")

        except:
            print(f"[✖] QR code NÃO detectado em: {file}")
            move_to_folder(file_folder=folder_path, file=file, qr_code=None)



if __name__ == "__main__":
    main()
