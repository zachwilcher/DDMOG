# Script to generate all the tables needed for the "minimal sparsity existence proposition" 

# 1,7
python ./138.py graphs/138-base-graphs/order-13.txt tables/order-13-odd-labelings.tex 1 2
python ./138.py graphs/138-base-graphs/order-13.txt tables/order-13-even-labelings.tex 2 2

# 2
python ./138.py graphs/138-base-graphs/order-14.txt tables/order-14-even-labelings.tex 2 2

# 3,9
python ./138.py graphs/138-base-graphs/order-15.txt tables/order-15-odd-labelings.tex 1 2
python ./138.py graphs/138-base-graphs/order-15.txt tables/order-15-even-labelings.tex 2 2

# 4
python ./138.py graphs/138-base-graphs/order-16.txt tables/order-16-even-labelings.tex 2 2

# 5,11
python ./138.py graphs/138-base-graphs/order-5.txt tables/order-5-odd-labelings.tex 1 2
python ./138.py graphs/138-base-graphs/order-5.txt tables/order-5-even-labelings.tex 2 2

# 6
python ./138.py graphs/138-base-graphs/order-18.txt tables/order-18-even-labelings.tex 2 2

# 8
python ./138.py graphs/138-base-graphs/order-32.txt tables/order-32-even-labelings.tex 2 2

# 10
python ./138.py graphs/138-base-graphs/order-10.txt tables/order-10-even-labelings.tex 2 2
