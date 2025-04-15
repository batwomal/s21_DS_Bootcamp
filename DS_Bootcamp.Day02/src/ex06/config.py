import logging

num_of_steps = 10
has_header = True

logfile = "analytics.log"

template = (
	"We have made {} observations from tossing a coin:\n"
	"{} of them were tails and {} of them were heads.\n"
	"The probabilities are {:.2f}% and {:.2f}%, respectively.\n"
	"Our forecast is that in the next {} observations we will have:\n"
	"{} tail and {} heads."
)

logging.basicConfig(
  filename=logfile,
  level=logging.INFO,
	filemode='w',
  format='%(asctime)s %(message)s'
)