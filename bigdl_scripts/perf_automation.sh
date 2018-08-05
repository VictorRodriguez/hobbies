
rm -rf results.log

for i in `seq 1 3`;
    do

    echo Running $i times
    spark-submit \
    --master local[28] \
    --executor-cores 28 \
    --total-executor-cores 28 \
    --driver-memory 60G \
    --executor-memory 90G \
    --driver-class-path /home/vrodri3/BigDL/dist/lib/bigdl-*-jar-with-dependencies.jar \
    --class com.intel.analytics.bigdl.models.inception.TrainInceptionV1 \
    /home/vrodri3/BigDL/dist/lib/bigdl-*-jar-with-dependencies.jar \
    --batchSize 112 \
    --learningRate 0.0896 \
    -f hdfs://localhost:9000/user/root/sequence_1 \
    --maxEpoch 3 \
    --checkpoint /home/vrodri3/checkpoint
    grep Throughput bigdl.log | awk '{sum+=$20} END { print sum, NR, sum/NR} ' >> results.log

    rm -rf bigdl.log
done    
        
for i in `seq 1 3`;
do

    echo Running $i times
    spark-submit \
    --master local[28] \
    --executor-cores 28 \
    --total-executor-cores 28 \
    --driver-memory 60G \
    --executor-memory 90G \
    --driver-class-path /home/vrodri3/prebuild_bigdl/lib/bigdl-*-jar-with-dependencies.jar \
    --class com.intel.analytics.bigdl.models.inception.TrainInceptionV1 \
    /home/vrodri3/prebuild_bigdl/lib/bigdl-*-jar-with-dependencies.jar \
    --batchSize 112 \
    --learningRate 0.0896 \
    -f hdfs://localhost:9000/user/root/sequence_1 \
    --maxEpoch 3 \
    --checkpoint /home/vrodri3/checkpoint
    grep Throughput bigdl.log | awk '{sum+=$20} END { print sum, NR, sum/NR} ' >> results.log

    rm -rf bigdl.log
done    
        
