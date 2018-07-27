rm -rf /tmp/corefile-*
rm -rf log.txt
gcc -g main.c -o main
./main || :
FILE=$(ls /tmp/corefile*)
sudo gdb ./main $FILE -x script.t &> log.txt 
cat log.txt
PATERN="main.c:5"
if grep -q $PATERN $FILE;then
    echo "PASS"
fi

