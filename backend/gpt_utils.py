import openai
from pdf_utils import extract_text_from_pdf

def query_gpt(prompt): #GPT와 상호작용하는 함수
  try:
    response = openai.ChatCompletion.create(
      model = "gpt-4",
      messages=[
        {"role" : "system", "content" : "You are a helpful assistant for analyzing PDF documents."},
        {"role": "user", "content": prompt}
      ],
    )
    return response.choices[0].message['content']
  except Exception as e:
    raise RuntimeError(f"Error while querying GPT: {str(e)}")

def find_sililar_problem(pdf_path): #GPT를 사용하여 유사한 문제를 찾고 그 페이지 및 문제 번호를 반환
  pdf_text = extract_text_from_pdf(pdf_path)
  user_prompt = (
    "Given the following PDF content, find the page and problem number most similar to the example question. "
    "PDF content:\n" + pdf_text[:500] + "\n...(truncated)..."
  )
  gpt_response = query_gpt(user_prompt)

try:
  parts = gpt_response.strip().split(',')
  page_number = int(parts[0].split(':')[1].strip())
  problem_number = int(parts[1].split(':')[1].strip())
  return page_number, problem_number
except Exception as e:
  raise ValueError(f"GPT response parsing error: {str(e)}")
