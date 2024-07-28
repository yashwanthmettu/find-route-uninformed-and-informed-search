Programming Language: Python

Structure of the code:
A single python file is developed named find_route.py. In this code, there are three main components, find_route function helps in processing and printing results. In class maps, I have implemented 2 search algorithms one that supports uninformed search and the other that supports informed search.  


Libraries used:
sys: Used this library to interact the python file with the command line arguments, sys.argv provides the access for it.

heapq: Used this library to maintain a priority queue of nodes based on their costs, here we have used it in both uninformed and informed algorithms.
How to run the code:

Need to run the code from terminal(command line argument) 

For the uninformed search, the order to follow is <file_name> <input1.txt> <start_node> <end_node>

For the informed search, the order to follow is <file_name> <input1.txt> <start_node> <end_node> <h_kassel.txt>

If you're unable to run the command in the terminal, this is the example to run for it

python find_route.py input1.txt Bremen Kassel

python find_route.py input1.txt Bremen Kassel h_kassel.txt
