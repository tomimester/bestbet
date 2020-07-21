from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = 'to_be_changed'

import numpy as np
from scipy.stats import skewnorm

@app.route("/")
def hi():
	starting_stack = 10000
	current_stack = starting_stack
	roundi = 1

	#random
	multiplier = 0
	while multiplier < 1:
		multiplier = skewnorm.rvs(10, 0.2, 1.3)
		multiplier = round(multiplier,1)

	chance_of_winning = 0
	while chance_of_winning <= 0 or chance_of_winning >= 1:
		mu = 0.47 #mean
		sigma = 0.16#stddev
		chance_of_winning = np.random.normal(mu, sigma)

	#draw
	chance_of_losing = 1 - chance_of_winning
	outcome = np.random.choice([True, False], p=[chance_of_winning, chance_of_losing])
	outcome = bool(outcome)
		
	#expected_value
	expected_value = chance_of_winning * multiplier

	#passing values
	session["roundi"] = roundi
	session["multiplier"] = multiplier
	session["current_stack"] = current_stack
	session["outcome"] = outcome
	session["chance_of_winning"] = chance_of_winning

	#print
	roundnr = 'ROUND #'+ str(roundi)
	cow = "{:.0f}".format(chance_of_winning * 100)+'%'
	current_stack_flask = 'You have ' + str(current_stack) + ' money!'
	cow_flask = 'You have ' + str(cow) + ' chance to ' + str(multiplier) + '* your money!'
	question_flask = 'How much of your money are you willing to risk?'

	return render_template('test.html', roundnr=roundnr, current_stack_flask=current_stack_flask, cow_flask=cow_flask, question_flask=question_flask)

@app.route("/", methods=['POST'])
def hi2():
	roundi = session["roundi"]
	multiplier = session["multiplier"]
	current_stack = session["current_stack"]
	outcome = session["outcome"]
	chance_of_winning = session["chance_of_winning"]

	risked_money = request.form['text']
	
	wrong_input = False
	try:
		risked_money = int(risked_money)
	except ValueError:
		wrong_input = True

	if wrong_input == True:
		message = 'WRONG INPUT, MATE!'
	elif risked_money > current_stack:
		message = "YOU DONT HAVE THAT MUCH MONEY, MATE!"
	elif risked_money < 0:
		message = "YOU CANT RISK NEGATIVE MONEY, MATE"
	else:
		roundi = roundi + 1
		risked_money = int(risked_money)
		current_stack = current_stack - risked_money

		result = risked_money * multiplier * outcome
		result = int(result)
		current_stack = current_stack + result
		if result == 0:
			message = 'woops, you lost, you have this much money left: '
		else:
			message = 'yay, you won, now you have this much money: '

	#	return(message + str(current_stack))

		#random
		multiplier = 0
		while multiplier < 1:
			multiplier = skewnorm.rvs(10, 0.2, 1.3)
			multiplier = round(multiplier,1)

		chance_of_winning = 0
		while chance_of_winning <= 0 or chance_of_winning >= 1:
			mu = 0.47 #mean
			sigma = 0.16#stddev
			chance_of_winning = np.random.normal(mu, sigma)

		#draw
		chance_of_losing = 1 - chance_of_winning
		outcome = np.random.choice([True, False], p=[chance_of_winning, chance_of_losing])
		outcome = bool(outcome)
			
		#expected_value
		expected_value = chance_of_winning * multiplier

	#passing values
	session["roundi"] = roundi
	session["multiplier"] = multiplier
	session["current_stack"] = current_stack
	session["outcome"] = outcome

	#print
	roundnr = 'ROUND #'+ str(roundi)
	cow = "{:.0f}".format(chance_of_winning * 100)+'%'
	current_stack_flask = 'You have ' + str(current_stack) + ' money!'
	cow_flask = 'You have ' + str(cow) + ' chance to ' + str(multiplier) + '* your money!'
	question_flask = 'How much of your money are you willing to risk?'

	message_flask = str(message)
	return render_template('test.html', message_flask=message_flask, roundnr=roundnr, current_stack_flask=current_stack_flask, cow_flask=cow_flask, question_flask=question_flask)


if __name__ == "__main__":
	app.run(host='0.0.0.0')