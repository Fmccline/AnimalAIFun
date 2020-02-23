#!/bin/bash
trainer_path=$1
num_trainers=$2

execution_times=()
for i in `seq 1 $num_trainers`;
do
    start=`date +%s`
    python trainer.py -f test$i -d 4 -t $trainer_path'trainer'$i'.yaml' -N &
    backPID=$!
    wait $BACK_PID
    end=`date +%s`
    conv=60
    total_time=`expr $end - $start`
    let minutes=total_time/60
    echo Execution time was $minutes minutes.
    execution_times+=($minutes)
done

echo Finished training models with all trainers!
for time in ${execution_times[@]}; 
do
    echo Execution time was $time minutes.
done