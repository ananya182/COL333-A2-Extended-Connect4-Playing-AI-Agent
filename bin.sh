#!/bin/sh
python3 -m connect4.ConnectFour ai ai connect4/initial_states/case1.txt --time 5 &
python3 -m connect4.ConnectFour ai sec_ai connect4/initial_states/case1.txt --time 5 &
python3 -m connect4.ConnectFour sec_ai ai connect4/initial_states/case1.txt --time 5 &

python3 -m connect4.ConnectFour ai ai connect4/initial_states/case2.txt --time 5 &
python3 -m connect4.ConnectFour ai sec_ai connect4/initial_states/case2.txt --time 5 &
python3 -m connect4.ConnectFour sec_ai ai connect4/initial_states/case2.txt --time 5 &

python3 -m connect4.ConnectFour ai ai connect4/initial_states/case3.txt --time 5 &
python3 -m connect4.ConnectFour ai sec_ai connect4/initial_states/case3.txt --time 5 &
python3 -m connect4.ConnectFour sec_ai ai connect4/initial_states/case3.txt --time 5 &

python3 -m connect4.ConnectFour ai ai connect4/initial_states/case4.txt --time 5 &
python3 -m connect4.ConnectFour ai sec_ai connect4/initial_states/case4.txt --time 5 &
python3 -m connect4.ConnectFour sec_ai ai connect4/initial_states/case4.txt --time 5 &