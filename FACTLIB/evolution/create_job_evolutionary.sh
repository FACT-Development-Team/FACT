ROUNDS=$1
POPULATION=$2
TOURNAMENT=$3
CROSSOVER=$4
MUTATION=$5

NO_POINTS=50

bsub -o lsf.evolutionary%J -n 1 -W 24:00  <<END
module load new gcc/4.8.2 python/3.7.1
export points=$NO_POINTS
export expr="$6"
export population=$POPULATION
export tournament=$TOURNAMENT
export crossover_rate=$CROSSOVER
export mutation_rate=$MUTATION
export rounds=$ROUNDS
python $HOME/code/generate_evolutionary.py
END

