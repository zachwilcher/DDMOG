# Script to generate all the tables needed for the "minimal sparsity existence proposition" 

# 0
python ./138.py graphs/138-base-graphs/order-0.txt 2 2

# 1,7
python ./138.py graphs/138-base-graphs/order-13.txt 0 2
python ./138.py graphs/138-base-graphs/order-13.txt 1 2

# 2
python ./138.py graphs/138-base-graphs/order-14.txt 0 2

# 3,9
python ./138.py graphs/138-base-graphs/order-15.txt 1 2
python ./138.py graphs/138-base-graphs/order-15.txt 0 2

# 4
python ./138.py graphs/138-base-graphs/order-16.txt 0 2

# 5,11
python ./138.py graphs/138-base-graphs/order-5.txt 1 2
python ./138.py graphs/138-base-graphs/order-5.txt 2 2

# 6
python ./138.py graphs/138-base-graphs/order-18.txt 0 2

# 8
python ./138.py graphs/138-base-graphs/order-32.txt 0 2

# 10
python ./138.py graphs/138-base-graphs/order-10.txt 0 2
