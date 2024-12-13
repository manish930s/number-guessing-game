import tkinter as tk
from PIL import Image, ImageTk
import random
from tkinter import ttk
from tkinter import messagebox
import pymysql

def connect_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Admin@21',
        database='number',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def init_db():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    score INT DEFAULT 0,
                    level VARCHAR(50) DEFAULT 'Easy'
                )
            ''')
        connection.commit()
    finally:
        connection.close()

def resizeImage(image_path, width, height):
    pil_image = Image.open(image_path)
    resized = pil_image.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized)

window = tk.Tk()
window.title("Number Guessing Game")
window.geometry("450x350+560+230")
window.config(bg="#f0f0f0")

def clear_screen():
    for widget in window.winfo_children():
        widget.destroy()

def mainfream():
    clear_screen()
    main = tk.Frame(window, bg="#fff")
    main.pack(fill="both", expand=True)

    global image, image2, image3, image4

    image = Image.open('cross.png')
    image = ImageTk.PhotoImage(image)
    team = tk.Label(master=main, image=image, bg="#fff")
    team.place(x=20, y=20)

    image2 = Image.open('play.png')
    image2 = ImageTk.PhotoImage(image2)
    b1 = tk.Label(master=main, image=image2, bg="#fff")
    b1.place(x=150, y=100)

    text1 = tk.Button(main, text="Play", font=('Arial', 20), bg="#fff", bd=0,
                      activebackground='#FFF', activeforeground='black', cursor='hand2', command=get_detail)
    text1.place(x=210, y=93)

    image3 = resizeImage("achievement.png", 50, 50)
    logo_label = tk.Label(main, image=image3, borderwidth=0, bg="#fff")
    logo_label.place(x=145, y=150)
    text2 = tk.Button(main, text="Score", font=('Arial', 20), bg="#fff", bd=0, activebackground='#FFF',
                      activeforeground='black', cursor='hand2', command=show_scores)
    text2.place(x=210, y=150)

    image4 = resizeImage("instruction.png", 40, 40)
    logo_label2 = tk.Label(main, image=image4, borderwidth=0, bg="#fff")
    logo_label2.place(x=145, y=210)
    text3 = tk.Button(main, text="How to Play", font=('Arial', 20), bg="#fff", bd=0, activebackground='#FFF',
                      activeforeground='black', cursor='hand2',command=info)
    text3.place(x=210, y=210)


def info():
    # Create a new top-level window for instructions
    clear_screen()
    info_window = tk.Frame(window, bg="#fff")
    info_window.pack(fill='both', expand=True)

    # Title Label
    title_label = tk.Label(info_window, text="How to Play", font=("Helvetica", 20, "bold"), bg="#fff", fg="#333333")
    title_label.pack(pady=10)

    # Instructions
    instructions_text = (
        "1. The game will select a random number between 1 and 100.\n"
        "2. You have to guess the number within a limited number of attempts.\n"
        "3. After each guess, you will receive feedback:\n"
        "   - 'Too low!' if your guess is less than the number.\n"
        "   - 'Too high!' if your guess is greater than the number.\n"
        "   - 'Correct!' if you guess the number correctly.\n"
        "4. If you run out of attempts, the game is over, and you will see the correct number.\n"
    )
    instructions_label = tk.Label(info_window, text=instructions_text, font=("Helvetica", 9), bg="#fff", fg="#555555", justify="left")
    instructions_label.pack(pady=9)

    # Difficulty Levels
    levels_text = (
        "Difficulty Levels:\n"
        "1. Easy: You have 10 attempts to guess the number.\n"
        "2. Medium: You have 5 attempts to guess the number.\n"
        "3. Hard: You have 3 attempts to guess the number.\n"
        "\n"
        "Choose your difficulty level wisely to maximize your chances of winning!"
    )
    levels_label = tk.Label(info_window, text=levels_text, font=("Helvetica", 9), bg="#fff", fg="#555555", justify="left")
    levels_label.pack(pady=1)

    # Close Button
    close_button = tk.Button(info_window, text="Close", command=mainfream, font=("Helvetica", 12), bg="#4caf50", fg="white")
    close_button.pack(pady=10)


def store_or_update_name(name, level):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO players (name, score, level) VALUES (%s, 0, %s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id), level=VALUES(level)', (name, level))
            connection.commit()
            return cursor.lastrowid  # Return the player's id
    finally:
        connection.close()

def update_score(player_id, score):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute('UPDATE players SET score = GREATEST(score, %s) WHERE id = %s', (score, player_id))
        connection.commit()
    finally:
        connection.close()

def show_scores():
    clear_screen()
    score_frame = tk.Frame(window, bg="#fff")
    score_frame.pack(fill='both', expand=True)

    header_label = tk.Label(score_frame, text="Player Scores", font=("Helvetica", 18, "bold"), bg="#fff", fg="#333333")
    header_label.pack(pady=10)

    levels = ["Easy", "Medium", "Hard"]
    selected_level = tk.StringVar()
    level_combobox = ttk.Combobox(score_frame, textvariable=selected_level, values=levels, state='readonly', width=30)
    level_combobox.place(x=50,y=50)
    level_combobox.set("Select Difficulty Level")

    # Create a Treeview widget to display scores
    tree = ttk.Treeview(score_frame, columns=('Name', 'Level', 'Score'), show='headings')
    tree.heading('Name', text='Name')
    tree.heading('Level', text='Level')
    tree.heading('Score', text='Score')
    tree.column('Name', anchor='center',width=100)
    tree.column('Level', anchor='center',width=100)
    tree.column('Score', anchor='center',width=100)

    scrollbar = ttk.Scrollbar(score_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    tree.pack(pady=20, fill='both', expand=True)

    def display_scores():
        selected = selected_level.get()
        if not selected or selected == "Select Difficulty Level":
            messagebox.showerror("Error", "Please select a difficulty level.")
            return

        # Clear previous scores
        for item in tree.get_children():
            tree.delete(item)

        # Fetch scores from the database based on selected level
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT name, level, score FROM players WHERE level = %s ORDER BY score DESC', (selected,))
                scores = cursor.fetchall()
                for score in scores:
                    tree.insert('', 'end', values=(score['name'], score['level'], score['score']))
        finally:
            connection.close()

    back = tk.Button(score_frame, text="< Back", command=mainfream)
    back.place(x=5, y=5)

    display_button = tk.Button(score_frame, text="Show Scores", font=("Helvetica", 12), bg="#4caf50", fg="white", command=display_scores)
    display_button.place(x=290,y=40)


def get_detail():
    clear_screen()  # Clear the current screen
    get_frame = tk.Frame(window, bg="#fff")
    get_frame.pack(fill='both', expand=True)

    header_label = tk.Label(get_frame, text="Enter Your Name", font=("Helvetica", 18, "bold"), bg="#fff", fg="#333333")
    header_label.place(x=120, y=50)

    entry = tk.Entry(get_frame, font=("Helvetica", 14), justify="center", bd=2)
    entry.place(x=120, y=120, width=200)  # Set width for better visibility

    global selected_level  # Ensure selected_level is global
    selected_level = None

    def check():
        global player_id  # Declare player_id as global
        name = entry.get()
        if name == "":
            messagebox.showerror("Error", "Please enter your Name")
        elif not name.isalpha():
            messagebox.showerror("Error", "Please enter alphabet characters only")
        else:
            # Proceed to difficulty selection after validating the name
            select_difficulty(name)  # Pass the name to the difficulty selection

    back = tk.Button(get_frame, text="< Back", command=mainfream)
    back.place(x=5, y=5)

    next_button = tk.Button(get_frame, text="Next", font=("Helvetica", 14), bg="#4caf50", fg="white", command=check)
    next_button.place(x=180, y=160, width=100, height=40)  # Adjust size and position


def select_difficulty(name):
    clear_screen()
    difficulty_frame = tk.Frame(window, bg="#fff")
    difficulty_frame.pack(fill='both', expand=True)

    header_label = tk.Label(difficulty_frame, text="Select Difficulty Level", font=("Helvetica", 18, "bold"), bg="#fff",
                            fg="#333333")
    header_label.pack(pady=10)

    def start_game(difficulty):
        global max_attempts, selected_level
        selected_level = difficulty  # Store selected difficulty level
        if difficulty == "Easy":
            max_attempts = 10
        elif difficulty == "Medium":
            max_attempts = 5
        else:  # Hard
            max_attempts = 3

        # Store the player's name and selected difficulty level
        global player_id
        player_id = store_or_update_name(name, selected_level)  # Store the name and level
        messagebox.showinfo("Success", f"Welcome, {name}! You have selected {difficulty} level.")

        play_game()  # Start the game after saving the player

    back = tk.Button(difficulty_frame, text="< Back", command=mainfream)
    back.place(x=5, y=5)

    easy_button = tk.Button(difficulty_frame, text="Easy", command=lambda: start_game("Easy"), font=("Helvetica", 14),
                            bg="#4caf50", fg="white")
    easy_button.pack(pady=5)

    medium_button = tk.Button(difficulty_frame, text="Medium", command=lambda: start_game("Medium"),
                              font=("Helvetica", 14), bg="#ff9800", fg="white")
    medium_button.pack(pady=5)

    hard_button = tk.Button(difficulty_frame, text="Hard", command=lambda: start_game("Hard"), font=("Helvetica", 14),
                            bg="#f44336", fg="white")
    hard_button.pack(pady=5)


def play_game():
    clear_screen()
    play_frame = tk.Frame(window, bg="#fff")
    play_frame.pack(fill="both", expand=True)

    global remaining_attempts  # Make remaining_attempts global
    remaining_attempts = max_attempts  # Initialize remaining attempts
    global number
    number = random.randint(1, 100)  # Random number for guessing

    def check_guess():
        global remaining_attempts  # Make remaining_attempts global
        try:
            guess = int(entry.get())
            remaining_attempts -= 1  # Decrease remaining attempts
            if guess < number:
                result_label.config(text=f"Too low! Try again. Attempts left: {remaining_attempts}", fg="#ff6347")
            elif guess > number:
                result_label.config(text=f"Too high! Try again. Attempts left: {remaining_attempts}", fg="#ff6347")
            else:
                result_label.config(text="Correct! You guessed it!", fg="#32cd32")
                update_score(player_id, remaining_attempts)  # Update score in the database
                return
            if remaining_attempts <= 0:
                result_label.config(text=f"Game Over! The number was {number}.", fg="#ff6347")
                entry.config(state='disabled')  # Disable entry after game over
        except ValueError:
            result_label.config(text="Please enter a valid number.", fg="#ff6347")

    def reset_game():
        global number
        number = random.randint(1, 100)
        global remaining_attempts
        remaining_attempts = max_attempts  # Reset remaining attempts
        entry.delete(0, tk.END)
        result_label.config(text="Guess a number between 1 and 100", fg="#333333")

    header_label = tk.Label(play_frame, text="Number Guessing Game", font=("Helvetica", 18, "bold"), bg="#fff", fg="#333333")
    header_label.pack(pady=10)

    back = tk.Button(play_frame,text="< Back",command=mainfream)
    back.place(x=5,y=5)

    instructions_label = tk.Label(play_frame, text="Guess a number between 1 and 100", font=("Helvetica", 12), bg="#fff", fg="#555555")
    instructions_label.pack(pady=5)

    entry = tk.Entry(play_frame, font=("Helvetica", 14), justify="center", bd=2, relief="solid")
    entry.pack(pady=10)

    guess_button = tk.Button(play_frame, text="Check", command=check_guess, font=("Helvetica", 12), bg="#4caf50", fg="white", bd=0, padx=10, pady=5, cursor="hand2")
    guess_button.pack(pady=5)

    result_label = tk.Label(play_frame, text="", font=("Helvetica", 12), bg="#fff", fg="#333333")
    result_label.pack(pady=10)

    reset_button = tk.Button(play_frame, text="Reset Game", command=reset_game, font=("Helvetica", 12), bg="#ff6347", fg="white", bd=0, padx=10, pady=5, cursor="hand2")
    reset_button.pack(pady=10)

# Initialize the database
init_db()

# Start the main frame
mainfream()

# Run the application
window.mainloop()
