@REM 非模拟退火算法都跑10轮
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork
python main_int.py --method brickwork

python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod
python main_int.py --method ourmethod

python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place
python main_int.py --method random_place

@REM 无时间限制的模拟退火跑2轮
python main_int.py --method brickwork_annealing
python main_int.py --method brickwork_annealing

python main_int.py --method ourmethod_annealing
python main_int.py --method ourmethod_annealing

@REM 有时间限制的模拟退火跑5轮
python main_int.py --method brickwork_annealing --time_limit 1400
python main_int.py --method brickwork_annealing --time_limit 1400
python main_int.py --method brickwork_annealing --time_limit 1400
python main_int.py --method brickwork_annealing --time_limit 1400
python main_int.py --method brickwork_annealing --time_limit 1400

python main_int.py --method ourmethod_annealing --time_limit 1400
python main_int.py --method ourmethod_annealing --time_limit 1400
python main_int.py --method ourmethod_annealing --time_limit 1400
python main_int.py --method ourmethod_annealing --time_limit 1400
python main_int.py --method ourmethod_annealing --time_limit 1400

@REM 浮点数（考虑小数点后两位甚至更多）
python main_float.py --method ourmethod_annealing --time_limit 1000
python main_float.py --method ourmethod_annealing --time_limit 1000
python main_float.py --method ourmethod_annealing --time_limit 1000
python main_float.py --method ourmethod_annealing --time_limit 1000
python main_float.py --method ourmethod_annealing --time_limit 1000
