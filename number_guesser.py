import random

def evaluate_performance(guesses):
    if guesses == 1:
        return "Incredible! You're a mind reader! 🎯"
    elif guesses <= 3:
        return "Great job! You're a natural at this! 🌟"
    elif guesses <= 5:
        return "Not bad! Keep practicing! 👍"
    else:
        return "Better luck next time! Practice makes perfect! 🎲"

def play_game():
    print("\n=== Number Guessing Game ===")
    print("I'm thinking of a number between 1 and 10...")
    
    secret_number = random.randint(1, 10)
    guesses = 0
    
    while True:
        try:
            guess = int(input("\nEnter your guess (1-10): "))
            guesses += 1
            
            if guess < 1 or guess > 10:
                print("Please enter a number between 1 and 10!")
                continue
                
            if guess < secret_number:
                print("Too low! Try a higher number.")
            elif guess > secret_number:
                print("Too high! Try a lower number.")
            else:
                print(f"\nCongratulations! You've guessed the number {secret_number} correctly! 🎉")
                print(f"Number of guesses: {guesses}")
                print(evaluate_performance(guesses))
                break
                
        except ValueError:
            print("Please enter a valid number!")

def main():
    print("Welcome to the Number Guessing Game! 🎮")
    
    while True:
        play_choice = input("\nWould you like to play? (yes/no): ").lower()
        
        if play_choice in ['yes', 'y']:
            play_game()
        elif play_choice in ['no', 'n']:
            print("\nThanks for stopping by! Hope to see you again! 👋")
            break
        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
