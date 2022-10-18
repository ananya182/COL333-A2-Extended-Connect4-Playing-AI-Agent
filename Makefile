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
	python3 -m connect4.ConnectFour ai ai connect4/initial_states/case4.txt --time 3
6 :
	python3 -m connect4.ConnectFour ai human connect4/initial_states/case4.txt --time 5
clean:
	-rm *.pyc
