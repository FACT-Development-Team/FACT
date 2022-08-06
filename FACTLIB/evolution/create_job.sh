ROUNDS=$1
NO_POINTS=50

bsub -o lsf.non_evolutionary%J -n 1 -W 24:00  <<END
module load new gcc/4.8.2 python/3.7.1
export points=$NO_POINTS
export expr="$2"

rounds=$ROUNDS python $HOME/code/generate.py
END

