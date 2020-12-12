
import sqlite3

connection = sqlite3.connect("quiz.sqlite")

CURRENT_USER = None


def quiz():
	if not CURRENT_USER:
		print("Please login first")
	else:
		cursor = connection.cursor()
		questions = cursor.execute("SELECT * FROM questions").fetchall()
		score = 0
		print("\n--------------LETS START-----------------")
		print("---------------------------------------------")
		for _, (question, answer) in enumerate(questions):
			# print(question) 
			user_answer=input(question +'\nAnswer: ')
			if user_answer.lower() == answer:
				score += 1
				print("Correct Answer!")
			else:
				print("Incorrect Answer!")
		print(f"You got {score} answer right out of {len(questions)}")
		user = cursor.execute("SELECT * FROM users where name = ?", (CURRENT_USER,)).fetchall()[0]
		last_score = user[-2]
		best_score = user[-1]
		if score > best_score:
			best_score = score
		last_score = score
		cursor.execute("UPDATE users SET last_score = ?, best_score = ? where name = ?", (last_score, best_score, CURRENT_USER))
		connection.commit()



def createAccount():
	global CURRENT_USER
	if CURRENT_USER:
		print("Already logged in")
	else:
		cursor = connection.cursor()
		
		print("\n-----------CREATE ACCOUNT-------------")
		print("---------------------------------------")
		username = input("Enter your USERNAME: ")
		password = input("Enter your PASSWORD: ")
		users = [i[0] for i in cursor.execute("SELECT * FROM users").fetchall()]

		if username in users:
			print("An account of this Username already exists.\nPlease enter the login panel.")
		else:
			cursor.execute("INSERT INTO users values(?,?,?,?,?)", (username, password, 'PLAYER', 0, 0))
			connection.commit()
			print(f"Account with username: {username} created successfully!")	


def loginAccount():
	global CURRENT_USER
	if CURRENT_USER:
		print("Already logged in")
	else:
		cursor = connection.cursor()
		print("\n-----------LOGIN ACCOUNT-------------")
		print("--------------------------------------")
		username = input("USERNAME: ")
		password = input("PASSWORD: ")
		users = dict([(i[0], i[1]) for i in cursor.execute("SELECT * FROM users").fetchall()])

		if username not in users.keys():
			print("An account of that name doesn't exist.\nPlease create an account first.")
		elif username in users.keys():
			if users[username] != password:
				print("Your password is incorrect.\nPlease enter the correct password and try again.")
			elif users[username] == password:
				CURRENT_USER= username
				print("You have successfully logged in.\n")
	

def logout():
	global CURRENT_USER
	CURRENT_USER = None
	print("You have logged out successfully")


def show_score():
	global CURRENT_USER
	if CURRENT_USER:
		cursor = connection.cursor()
		user = cursor.execute("SELECT * FROM users where name = ?", (CURRENT_USER,)).fetchall()[0]
		print(f"Username: {user[0]}, Best Score: {user[-1]}, Last Score: {user[-2]}")
	else:
		print("Please login first")


def addQuestion():
	global CURRENT_USER
	if not CURRENT_USER:
		print("You must first login before adding questions.")
	else:
		cursor = connection.cursor()
		user = cursor.execute("SELECT * FROM users where name = ?", (CURRENT_USER,)).fetchall()[0]

		if user[2] == "ADMIN":
			print('\n-------------ADD QUESTIONS-------------\n')
			print("----------------------------------------")
			question = input("Enter the question that you want to add:\n")
			for i in range(4):
				question += '\n' + input(f"Enter option {i+1}:")
			question += '\n'
			answer = input("Enter correct option").lower()
			cursor.execute("INSERT INTO questions VALUES (?, ?)", (question, answer))
			connection.commit()	
			print("Question successfully added.")		
		else:
			print("You don't have access to adding questions. Only admins are allowed to add questions.")

def rules():
	print('''\n------------------------------RULES-------------------------------\n
1. Each round consists of 10 random questions. To answer, you must press A/B/C/D (case-insensitive).
Your final score will be given at the end.
2. Each question consists of 1 point. There's no negative point for wrong answers.
3. You can create an account from ACCOUNT CREATION panel.
4. You can login using the LOGIN PANEL.
	''')

def about():
	print('''\\n----------------------------ABOUT US-------------------------------\n
This project has been created by Harsh Agarwal and his team.
It is a basic Python Project for my 3rd Semester.''')


##main function to start Quiz
if __name__ == "__main__":
	choice = 1
	while choice != 7:
		print('\n---------------WELCOME TO CURRENT AFFAIRS QUIZ------------------')
		print('-----------------------------------------------------------------')
		print('1. PLAY QUIZ')
		print('2. SHOW SCORE')
		print('3. ADD QUIZ QUESTIONS')
		print('4. CREATE AN ACCOUNT')
		print('5. LOGIN PANEL')
		print('6. LOGOUT PANEL')
		print('7. SEE INSTRUCTIONS ON HOW TO PLAY THE GAME')
		print('8. EXIT')
		print('9. ABOUT US')
		choice = input('ENTER YOUR CHOICE: ')
		if choice == '1':
			quiz()
		elif choice == '2':
			show_score()
		elif choice == '3':
			addQuestion()
		elif choice == '4':
			createAccount()
		elif choice == '5':
			loginAccount()
		elif choice == '6':
			logout()
		elif choice == '7':
			rules()
		elif choice == '8':
			connection.commit()
			connection.close()
			break
		elif choice == 9:
			about()
		else:
			print('WRONG INPUT. ENTER THE CHOICE AGAIN')

