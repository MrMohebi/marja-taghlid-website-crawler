import re

# Path to your questions.jonl file
file_path = "files/questions.jsonl"

def find_missing_questions(file_path, total_questions=2118):
    question_numbers = set()
    
    # Read the file and extract question numbers
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(r"س\s*(\d+)", line)
            if match:
                question_numbers.add(int(match.group(1)))
    
    # Find missing numbers
    all_numbers = set(range(1, total_questions + 1))
    missing_numbers = sorted(all_numbers - question_numbers)
    
    return missing_numbers

# Run the function
missing = find_missing_questions(file_path)

# Print missing question numbers
print("Missing question numbers:", missing)
print("len:", len(missing))
