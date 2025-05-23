print("Hi! Want to take a fun quiz about computers? (yes/no)")

# Get user's choice to start the quiz
choice = input().lower()

if choice != "yes":
    print("No problem! Maybe next time. Goodbye!")
    exit()

# Questions and answers stored in a list of tuples
questions = [
    ("What does CPU stand for?", "central processing unit"),
    ("What does RAM stand for?", "random access memory"),
    ("Which device is used for clicking and pointing on a computer screen?", "mouse"),
    ("What is the main purpose of an operating system?", "manage computer resources"),
    ("What type of device is a laptop?", "portable computer"),
    ("What does WiFi stand for?", "wireless fidelity"),
    ("What is the purpose of a keyboard?", "input device"),
    ("What type of storage device is an SSD?", "solid state drive"),
    ("What does USB stand for?", "universal serial bus"),
    ("What is the brain of the computer?", "cpu")
]

# Initialize score
score = 0
total_questions = len(questions)

print("\nGreat! Let's test your computer knowledge. Answer these questions to the best of your ability.")
print("Note: All answers should be in lowercase.\n")

# Ask each question
for question, correct_answer in questions:
    print("\n" + question)
    user_answer = input("Your answer: ").lower()
    
    if user_answer == correct_answer:
        print("Correct! Well done!")
        score += 1
    else:
        print(f"Sorry, that's not correct. The correct answer is: {correct_answer}")

# Calculate percentage
percentage = (score / total_questions) * 100

# Display final results
print("\n--- Quiz Complete! ---")
print(f"You got {score} out of {total_questions} questions correct!")
print(f"Your score: {percentage:.1f}%")

# Give feedback based on score
if percentage >= 90:
    print("Excellent! You're a computer expert!")
elif percentage >= 70:
    print("Good job! You have solid computer knowledge!")
elif percentage >= 50:
    print("Not bad! Keep learning about computers!")
else:
    print("Keep studying! There's always room for improvement!")

