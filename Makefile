all:
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case1.txt --time 20
1 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case1.txt --time 5
2 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case2.txt --time 5
3 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case3.txt --time 3
4 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case4.txt --time 5
5 :
	python3 -m connect4.ConnectFour ai ai connect4/initial_states/case4.txt --time 5
6 :
	python3 -m connect4.ConnectFour ai human connect4/initial_states/case4.txt --time 5
7 :
	python3 -m connect4.ConnectFour random ai connect4/initial_states/case4.txt --time 5
8 :
	python3 -m connect4.ConnectFour human ai connect4/initial_states/case4.txt --time 3
9 :
	python3 -m connect4.ConnectFour ai human connect4/initial_states/case4.txt --time 3
10 :
	python3 -m connect4.ConnectFour ai human connect4/initial_states/case1.txt --time 3
11 :
	python3 -m connect4.ConnectFour ai sec_ai connect4/initial_states/case4.txt --time 3
12 :
	python3 -m connect4.ConnectFour sec_ai ai connect4/initial_states/case4.txt --time 3
clean:
	-rm *.pyc
