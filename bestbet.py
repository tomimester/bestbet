from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = 'to_be_changed'
import numpy as np
import random

def luck_of_the_draw():
    multiplier = 0
    while multiplier < 1:
        #setting the expected value with a normal distribution (cant be less than 0)
        expected_value = 0
        while expected_value <= 0:
            mu = 1 #mean
            sigma = 0.4 #stdev
            expected_value = np.random.normal(mu, sigma)

        #setting the chance of winning with a normal distribution (float between 0 and 1)
        chance_of_winning = 0
        while chance_of_winning <= 0 or chance_of_winning >= 1:
            mu = 0.5 #mean
            sigma = 0.3 #stdev
            chance_of_winning = np.random.normal(mu, sigma)

        #calculating the multiplier (cant be less than 1 -- fixed by a while loop at the beginning)
        multiplier = (expected_value / chance_of_winning)
        multiplier = float(multiplier)
        multiplier = round(multiplier,1)

    chance_of_losing = 1 - chance_of_winning
    outcome = np.random.choice([True, False], p=[chance_of_winning, chance_of_losing])
    outcome = bool(outcome)
    
    return(expected_value, multiplier, chance_of_winning, outcome)

@app.route("/")
def welcome():
	session_id = random.randint(100000000000000,(1000000000000000-1))
	starting_stack = 10000
	current_stack = starting_stack
	roundi = 1
	log_info = []
	
	#draw
	expected_value, multiplier, chance_of_winning, outcome = luck_of_the_draw()

	#passing values
	session["session_id"] = session_id
	session["current_stack"] = current_stack
	session["roundi"] = roundi
	session["expected_value"] = expected_value
	session["chance_of_winning"] = chance_of_winning
	session["multiplier"] = multiplier
	session["outcome"] = outcome
	session["log_info"] = log_info

	#print
	roundnr = str(roundi)
	cow = "{:.0f}".format(chance_of_winning * 100)
	current_stack_flask = str(current_stack)
	cow_flask = str(cow)
	multiplier_flask = str(multiplier)

	return render_template('game.html', 
		roundnr=roundnr, 
		current_stack_flask=current_stack_flask, 
		cow_flask=cow_flask, 
		multiplier_flask=multiplier_flask,
		session_id=session_id,
		log_info=log_info)

@app.route("/", methods=['POST'])
def game():
	session_id = session["session_id"]
	current_stack = session["current_stack"]
	roundi = session["roundi"]
	expected_value = session["expected_value"]
	chance_of_winning = session["chance_of_winning"]
	multiplier = session["multiplier"]
	outcome = session["outcome"]
	log_info = session["log_info"]

	risked_money = request.form['text']
	
	wrong_input = False
	try:
		risked_money = int(risked_money)
	except ValueError:
		wrong_input = True

	if wrong_input == True:
		message = 'WRONG INPUT, MATE!'
		color_code = 'red'
	elif risked_money > current_stack:
		message = "YOU DONT HAVE THAT MUCH MONEY, DUDE!"
		color_code = 'red'
	elif risked_money < 0:
		message = "YOU CANT RISK NEGATIVE MONEY, MAN"
		color_code = 'red'
	else:
		risked_money = int(risked_money)
		current_stack = current_stack - risked_money

		result = risked_money * multiplier * outcome
		result = int(result)
		current_stack = current_stack + result
		if risked_money == 0:
			message = "You didn't risk anything."
			color_code = 'grey'
		elif result == 0:
			message = 'Woops, you lost!'
			color_code = 'red'
		else:
			message = 'Yay, you won!'
			color_code = 'green'

		#logging the values
		log_info.append([roundi, risked_money, "{:.2f}".format(expected_value), multiplier, "{:.0f}".format(chance_of_winning * 100), outcome, result, current_stack])

		#new round starts
		roundi = roundi + 1

		#draw
		expected_value, multiplier, chance_of_winning, outcome = luck_of_the_draw()

	#passing values
	session["session_id"] = session_id
	session["current_stack"] = current_stack
	session["roundi"] = roundi
	session["expected_value"] = expected_value
	session["chance_of_winning"] = chance_of_winning
	session["multiplier"] = multiplier
	session["outcome"] = outcome
	session["log_info"] = log_info

	if roundi > 10:
		return redirect("/result/", code=302)

	#print
	roundnr = str(roundi)
	cow = "{:.0f}".format(chance_of_winning * 100)
	current_stack_flask = str(current_stack)
	cow_flask = str(cow)
	multiplier_flask = str(multiplier)
	message_flask = str(message)
	return render_template('game.html',
		message_flask=message_flask, 
		roundnr=roundnr, 
		current_stack_flask=current_stack_flask, 
		cow_flask=cow_flask, 
		multiplier_flask=multiplier_flask, 
		color_code=color_code,
		session_id=session_id,
		log_info=log_info)

@app.route("/result/")
def result():
	session_id = session["session_id"]
	current_stack = session["current_stack"]
	roundi = session["roundi"]
	expected_value = session["expected_value"]
	chance_of_winning = session["chance_of_winning"]
	multiplier = session["multiplier"]
	outcome = session["outcome"]
	log_info = session["log_info"]

	current_stack_flask = str(current_stack)

	return render_template('result.html',
		current_stack_flask=current_stack_flask, 
		session_id=session_id,
		log_info=log_info)

if __name__ == "__main__":
	app.run(host='0.0.0.0')