from config import reviews, usedreviews

def get_first_review():
    try:
        with open(reviews, "r", encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                review_info = lines[0].strip()
                with open(reviews, "w", encoding='utf-8') as updated_file:
                    updated_file.writelines(lines[1:])
                return review_info
            else:
                print("No more reviews in the file.")
                return None
    except FileNotFoundError:
        print(f"Error: {reviews} file not found.")
        return None
    except Exception as e:
        print(f"An error occurred while getting review info: {e}")
        return None

def move_review_to_used(review_info):
    try:
        with open(usedreviews, "a", encoding='utf-8') as used_file:
            used_file.write(review_info + "\n")
            print(f"Moved review to used: {review_info}")  # Debugging line
    except FileNotFoundError:
        print(f"Error: {usedreviews} file not found.")
    except Exception as e:
        print(f"An error occurred while moving review info to the used file: {e}")

