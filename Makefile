all:
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case1.txt --time 20
1 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case1.txt --time 20
2 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case2.txt --time 20
3 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case3.txt --time 20
4 :
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case4.txt --time 20
	
clean:
	-rm *.pyc
