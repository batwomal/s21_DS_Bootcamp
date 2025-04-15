import sys
import os
import analytics as an
import config as co

def main():
  analytics = an.Research().Analytics()
  total_observations = analytics.total()
  heads, tails = analytics.counts()
  heads_probability, tails_probability = analytics.fractions()
  forecast_observations = co.num_of_steps
  predicted_heads, predicted_tails = analytics.counts_predicted() 
  report = co.template.format(total_observations,
    tails, heads, tails_probability, heads_probability, forecast_observations,
    predicted_heads, predicted_tails)
  print(report)
  analytics.save_to_file(report, 'report')


if __name__ == "__main__":
  if (len(sys.argv) != 2 or not os.path.exists(sys.argv[1])):
    raise Exception("Wrong usage, try ../../datasets/data.csv")
  research = an.Research()
  if research.file_path == "":
    raise Exception("Invalid file structure or file not found.")
  else:
    main()