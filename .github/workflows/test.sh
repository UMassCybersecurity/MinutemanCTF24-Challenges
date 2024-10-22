a="test"
b="test"
if [ ! -z "$a" ] && [ $b == "test" ]
then
    echo "in vm" 
else 
    echo "not in vm"
fi
