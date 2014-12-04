
'''import module for assignment8'''
from result import result


def main():
  positions = [1,10,100,1000]
  num_trials = 10000
  result(positions, num_trials)

if __name__=="__main__":
  try:
    main()
  except KeyboardInterrupt:
    pass

