import openai
import os
openai.api_key=os.getenv("OPENAI_API_KEY")
from pdf_utils import extract_text_from_pdf

def query_gpt(prompt):
    """
    GPT 모델과 상호작용.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for analyzing PDF documents."},
                {"role": "user", "content": prompt}
            ],
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Error while querying GPT: {str(e)}")


def find_similar_problem(pdf_path):
    """
    GPT를 사용해 유사한 문제를 찾고 페이지 및 문제 번호 반환.
    """
    pdf_text = extract_text_from_pdf(pdf_path)
    user_prompt = (
        "Given the following PDF content, identify the page and problem number most similar to the example question. "
        "Provide your answer strictly in the format: 'Page: <page_number>, Problem: <problem_number>'.\n\n"
        f"PDF content:\n{pdf_text[:1000]}\n...(truncated)..."
    )

    gpt_response = query_gpt(user_prompt)
    print(f"Raw GPT response: {gpt_response}")

    try:
        parts = gpt_response.strip().split(',')
        page_number = int(parts[0].split(':')[1].strip())
        problem_number = int(parts[1].split(':')[1].strip())
        return page_number, problem_number
    except Exception as e:
        raise ValueError(f"GPT response parsing error: {str(e)}")
