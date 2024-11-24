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

def extract_image_from_pdf(pdf_path, page_number, problem_number, output_folder): #PDF의 특정 페이지에서 이미지 추출
    try:
        pdf_document = fitz.open(pdf_path)
        page = pdf_document[page_number - 1]  # 페이지는 0부터 시작
        blocks = page.get_text("dict")["blocks"]

        problem_bbox = None
        for block in blocks:
            for line in block["lines"]:
                for span in line["spans"]:
                    if f"{problem_number}." in span ["text"]:
                        problem_bbox = block["bbox"]
                        break
                if problem_bbox:
                    break
            if problem_bbox:
                break

        if not problem_bbox:
            raise RuntimeError(f"Problem number {problem_number} not found on page {page_number}.")

        pix = page.get_pixmap(clip=problem_bbox)
        image_path = os.path.join(output_folder, f"problem_{page_number}_{problem_number}.png")
        pix.save(image_path)
        return image_path
                
    except Exception as e:
        raise RuntimeError(f"Error extracting image from PDF: {str(e)}")
