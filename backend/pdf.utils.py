import fitz
import PyPDF2

def extract_text_from_pdf(pdf_path): #PDF에서 텍스트 추출
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        raise RuntimeError(f"Error extracting text from PDF: {str(e)}")

def extract_image_from_pdf(pdf_path, page_number, output_folder): #PDF의 특정 페이지에서 이미지 추출
    try:
        pdf_document = fitz.open(pdf_path)
        page = pdf_document[page_number - 1]  # 페이지는 0부터 시작
        images = page.get_images(full=True)

        if not images:
            raise RuntimeError("No images found on the specified page.")

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]

            # 이미지 저장
            image_path = os.path.join(output_folder, f"output_image_{page_number}_{img_index}.png")
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            return image_path
    except Exception as e:
        raise RuntimeError(f"Error extracting image from PDF: {str(e)}")
