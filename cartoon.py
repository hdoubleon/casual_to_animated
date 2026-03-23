import cv2
import numpy as np


def cartoonize_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        print(f"'{image_path}' 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return

    # 화면에 한눈에 들어오도록 크기 조정 (옵션)
    height, width = img.shape[:2]
    max_size = 800
    if max(height, width) > max_size:
        scale = max_size / max(height, width)
        img = cv2.resize(img, None, fx=scale, fy=scale)

    # --- Step 1: 윤곽선(Edge) 추출 ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )

    # --- Step 2: 색상 단순화(수채화 느낌) ---
    color = cv2.bilateralFilter(img, 9, 300, 300)

    # --- Step 3: 윤곽선과 색상 합치기 ---
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    output_filename = (
        "cartoon_" + image_path.split("/")[-1]
    )  # 원본 이름 앞에 'cartoon_'을 붙여서 저장
    cv2.imwrite(output_filename, cartoon)
    print(f"🎉 성공! 변환된 이미지가 '{output_filename}' 파일로 저장되었습니다.")

    # 결과 출력
    cv2.imshow("Original Image", img)
    cv2.imshow("Cartoon Rendering", cartoon)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # 맥북 윈도우 닫기 버그 방지용


# 함수 실행
cartoonize_image("dog.jpeg")
