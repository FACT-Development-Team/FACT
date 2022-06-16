import glob
import os

def read_logs(folder):
  files = glob.glob(os.path.join(folder, '*'), recursive=True)
  runs = []
  
  for file in files:
    try:
      with open(file, 'r+') as f:
        run = {}

        for line in f:
          if line.startswith('export rounds'):
            run['rounds'] = int(line.split('export rounds=')[-1].strip())
          elif line.startswith('E V O L U T I O N A R Y'):
            run['mode'] = 'evolutionary'
          elif line.startswith('N O N - E V O L U T I O N A R Y'):
            run['mode'] = 'non-evolutionary'
          elif line.startswith('Polynomial'):
            run['polynomial'] = line.split('Polynomial:')[-1].strip()
          elif line.startswith('Population'):
            run['population'] = int(line.split('Population:')[-1].strip())
          elif line.startswith('Tournament'):
            run['tournament'] = int(line.split('Tournament:')[-1].strip())
          elif line.startswith('Mutation rate'):
            run['mutation_rate'] = float(line.split('Mutation rate:')[-1].strip())
          elif line.startswith('Crossover rate'):
            run['crossover_rate'] = float(line.split('Crossover rate:')[-1].strip())
          elif line.startswith('Average'):
            run['avg'] = float(line.split('Average:')[-1].strip())
          elif line.startswith('Variance'):
            run['var'] = float(line.split('Variance:')[-1].strip())
          elif line.startswith('Standard deviation'):
            run['std'] = float(line.split('Standard deviation:')[-1].strip())
          elif line.startswith('Elapsed time'):
            run['time'] = float(line.split('Elapsed time (s):')[-1].strip())

        runs.append(run)
    except Exception as err:
      print('Unable to read file:', err)
  
  return runs


if __name__ == '__main__':
  directory = '../experiments'
  print(read_logs(directory))