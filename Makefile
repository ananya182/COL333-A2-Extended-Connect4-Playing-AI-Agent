all:
	python3 -m connect4.ConnectFour ai random connect4/initial_states/case1.txt --time 20

clean:
	-rm *.pyc
