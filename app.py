from flask import Flask, jsonify, request

from apscheduler.schedulers.background import BackgroundScheduler

from commands import AddTaskCommand, ModifyTaskCommand, RemoveTaskCommand, CommandExecutor
from conditions import Interpreter


app = Flask(__name__)


scheduler = BackgroundScheduler()

scheduler.start()

command_executor = CommandExecutor()


@app.route('/')
def index():
    return jsonify({
        'success': True,
        'message': "This is application for managing tasks"
    })


@app.route('/add-task', methods=['POST'])
def add_task():

    try:

        data = request.get_json()

        for filed in ['receiver', 'city', 'messenger', 'units', 'interval']:
            if filed not in data:
                raise Exception(f"Invalid request data. Field \"{filed}\" is required.")
        
        receiver = data['receiver']
        city = data['city']
        messenger = data['messenger']
        units = data['units']
        interval = data['interval']

        if not isinstance(interval, int):
            raise TypeError(f"Invalid request data. Field \"interval\" must be integer.")
        
        if interval <= 0:
            raise ValueError(f"Invalid request data. Field \"interval\" must be positive integer.")
        
        if 'condition' in data and not isinstance(data['condition'], dict):
            raise TypeError(f"Invalid request data. Field \"condition\" must be dictionary.")

        if 'condition' in data and not len(data['condition']) == 1:
            raise ValueError(f"Invalid request data. Field \"condition\" must contain only one root operator.")

        if 'condition' not in data or Interpreter(data['condition']):

            command = AddTaskCommand(scheduler, receiver, city, messenger, units, interval)

            command_executor.set_command(command)

            result = command_executor.execute_command()

            return jsonify(result), 201
        
        return jsonify({'success': True, 'message': "Task not added"})

    except Exception as exception:
        return jsonify({
            'success': False,
            'error': {
                'type': type(exception).__name__,
                'message': str(exception)
            }
        })


@app.route('/modify-task/<task_id>', methods=['PUT'])
def modify_task(task_id):

    try:

        data = request.get_json()

        for filed in ['interval']:
            if filed not in data:
                raise Exception(f"Invalid request data. Field \"{filed}\" is required.")
        
        interval = data['interval']

        if not isinstance(interval, int):
            raise TypeError(f"Invalid request data. Field \"interval\" must be integer.")
        
        if interval <= 0:
            raise ValueError(f"Invalid request data. Field \"interval\" must be positive integer.")
        
        command = ModifyTaskCommand(scheduler, task_id, interval)

        command_executor.set_command(command)

        result = command_executor.execute_command()

        return jsonify(result)

    except Exception as exception:
        return jsonify({
            'success': False,
            'error': {
                'type': type(exception).__name__,
                'message': str(exception)
            }
        })


@app.route('/remove-task/<task_id>', methods=['DELETE'])
def remove_task(task_id):

    try:

        command = RemoveTaskCommand(scheduler, task_id)

        command_executor.set_command(command)

        result = command_executor.execute_command()

        return jsonify(result)

    except Exception as exception:
        return jsonify({
            'success': False,
            'error': {
                'type': type(exception).__name__,
                'message': str(exception)
            }
        })


if __name__ == '__main__':
    app.run()
