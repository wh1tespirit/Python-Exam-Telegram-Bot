import re
import json

def load_questions_from_file(path: str) -> list[dict]:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    raw_questions = content.split("________________________________________")
    questions = []

    for block in raw_questions:
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        if not lines or len(lines) < 6:
            continue  # пропускаем неполные блоки

        question_text = lines[0]
        options = [line.replace("🔹 ", "") for line in lines[1:5]]

        match = re.search(r'✅ Правильный ответ:\s*([A-D])\)', block)
        if not match:
            continue  # если нет правильного ответа — пропускаем

        correct_letter = match.group(1)

        questions.append({
            "question": question_text,
            "options": options,
            "correct": correct_letter
        })

    return questions

def load_questions_from_json(path: str) -> list[dict]:
    with open(path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return questions
