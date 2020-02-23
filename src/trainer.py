from unityAgentTrainer import UnityAgentTrainer
import argparse
import datetime

parser = argparse.ArgumentParser(description='Trainer for Unity ML Agents with the AnimalAI environment')
parser.add_argument('-f', '--model_name', dest='model_name', help='Name of model to train.')
parser.add_argument('-t', '--trainer_path', dest='trainer_path', default='configs/trainers/default_trainer.yaml', help='Optional path to trainer config to use.')
parser.add_argument('-c', '--curriculum', dest='curriculum', default=None, help='Optional name of curriculum to train from')
parser.add_argument('-a', '--arena_config', dest='arena_config', default=None, help='Path to arena config')
parser.add_argument('-d', '--num_agents', dest='num_agents', default=None, help='Optional name of curriculum to train from', type=int)
parser.add_argument('-w', '--watch', dest='watch_ai', default=False, action='store_true', help='Boolean for whether user wants to watch the AI or not.')
parser.add_argument('-n', '--new_model', dest='new_model', default=False, action='store_true', help='Boolean for whether to create a new model or load from an existing model.')
parser.add_argument('-N', '--new_model_now', dest='new_model_now', default=False, action='store_true', help='Boolean to bypass the check that asks if you are sure you want to create a model.')


def train_model(model_name, curriculum_type, arena_config, num_agents, watch_ai, trainer_path, new_model, new_model_now):
    if new_model_now:
        new_model = True
    elif new_model:
        new_model = True if input('Are you sure you want to create a new model?\n(y/n): ') == ('y' or 'Y') else False

    trainer = UnityAgentTrainer(model_name, trainer_path, arena_config, num_agents, new_model, watch_ai, curriculum_type)
    start = datetime.datetime.now()
    trainer.train()
    end = datetime.datetime.now()
    print(f'Finished training after {round((end-start).seconds / 60 / 60, 3)} hours.')


if __name__ == '__main__':
    args = parser.parse_args()
    new_model = args.new_model
    new_model_now = args.new_model_now
    model_name = args.model_name
    curriculum_type = args.curriculum
    arena_config = 'configs/arenas/baseline_arena.yaml' if args.arena_config is None else args.arena_config
    num_agents = args.num_agents
    watch_ai = args.watch_ai 

    train_model(model_name, curriculum_type, 
                arena_config, num_agents, 
                watch_ai, args.trainer_path, 
                args.new_model, args.new_model_now)
