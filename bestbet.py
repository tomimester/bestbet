from flask import Flask, render_template
app = Flask(__name__)
import numpy as np
from scipy.stats import skewnorm

@app.route("/")
def hello():
    return '<p style="font-size:2em; margin:40px; background-color:yellow">Here comes a game that will help you to understand the concept of *expected value*. \
    <br> Also, why most people lose in casinos. \
    <br><br> Stay tuned! \
    <br><br> (Stack: Python + Flask + nginx)</p>'

@app.route("/test/", methods=['POST'])
def hi():
	starting_stack = 10000
	current_stack = starting_stack
	i = 1
	while i < 51:
	    #setting the base values
	    
	    #multiplier
	    #beginner mode (10, 0.4, 2)
	    #advanced mode
	    multiplier = skewnorm.rvs (10, 0.2, 1.3)
	    multiplier = round(multiplier,1)
	    if multiplier < 1:
	        continue

	    #chance_of_winning
	    mu = 0.47 #mean
	    sigma = 0.16#stddev
	    chance_of_winning = np.random.normal(mu, sigma)
	    if chance_of_winning < 0 or chance_of_winning > 1:
	        continue
	        
	    #expected_value
	    expected_value = chance_of_winning * multiplier
	
	    #sentence
	    roundnr = 'ROUND #'+ str(i)

	    cow = "{:.0f}".format(chance_of_winning * 100)+'%'
	    current_stack_flask = 'You have ' + str(current_stack) + ' money!'
	    cow_flask = 'You have ' + str(cow) + ' chance to ' + str(multiplier) + '* your money!'
	    question_flask = 'How much of your money are you willing to risk?'
	    return render_template('test.html', roundnr=roundnr, current_stack_flask=current_stack_flask, cow_flask=cow_flask, question_flask=question_flask)
	    i = i + 1

if __name__ == "__main__":
    app.run(host='0.0.0.0')