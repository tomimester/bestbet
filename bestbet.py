from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = 'to_be_changed'
import numpy as np

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
	starting_stack = 10000
	current_stack = starting_stack
	roundi = 1
	
	#draw
	expected_value, multiplier, chance_of_winning, outcome = luck_of_the_draw()

	#passing values
	session["roundi"] = roundi
	session["multiplier"] = multiplier
	session["current_stack"] = current_stack
	session["outcome"] = outcome
	session["chance_of_winning"] = chance_of_winning

	#print
	roundnr = str(roundi)
	cow = "{:.0f}".format(chance_of_winning * 100)
	current_stack_flask = str(current_stack)
	cow_flask = str(cow)
	multiplier_flask = str(multiplier)

	return render_template('test.html', 
		roundnr=roundnr, 
		current_stack_flask=current_stack_flask, 
		cow_flask=cow_flask, 
		multiplier_flask=multiplier_flask)

@app.route("/", methods=['POST'])
def game():
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
		color_code = 'red'
	elif risked_money > current_stack:
		message = "YOU DONT HAVE THAT MUCH MONEY, DUDE!"
		color_code = 'red'
	elif risked_money < 0:
		message = "YOU CANT RISK NEGATIVE MONEY, MAN"
		color_code = 'red'
	else:
		roundi = roundi + 1
		risked_money = int(risked_money)
		current_stack = current_stack - risked_money

		result = risked_money * multiplier * outcome
		result = int(result)
		current_stack = current_stack + result
		if result == 0:
			message = 'Woops, you lost!'
			color_code = 'red'
		else:
			message = 'Yay, you won!'
			color_code = 'green'

	#draw
		expected_value, multiplier, chance_of_winning, outcome = luck_of_the_draw()

	#passing values
	session["roundi"] = roundi
	session["multiplier"] = multiplier
	session["current_stack"] = current_stack
	session["outcome"] = outcome

	#print
	roundnr = str(roundi)
	cow = "{:.0f}".format(chance_of_winning * 100)
	current_stack_flask = str(current_stack)
	cow_flask = str(cow)
	multiplier_flask = str(multiplier)
	message_flask = str(message)
	return render_template('test.html',
		message_flask=message_flask, 
		roundnr=roundnr, 
		current_stack_flask=current_stack_flask, 
		cow_flask=cow_flask, 
		multiplier_flask=multiplier_flask, 
		color_code=color_code)


if __name__ == "__main__":
	app.run(host='0.0.0.0')