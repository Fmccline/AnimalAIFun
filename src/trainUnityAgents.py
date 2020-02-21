from animalai_train.trainers.trainer_controller import TrainerController
from animalai.envs import UnityEnvironment
from animalai.envs.exception import UnityEnvironmentException
from animalai.envs.arena_config import ArenaConfig
from animalai_train.trainers.meta_curriculum import MetaCurriculum
import random
import yaml
import sys
import argparse
import datetime

parser = argparse.ArgumentParser(description='My arg parser')
parser.add_argument('-a', '--arena_config', dest='arena_config', default=None, help='Path to arena config')
parser.add_argument('-f', '--model_name', dest='model_name', help='Name of model to train.')
parser.add_argument('-w', '--watch', dest='watch_ai', default=False, action='store_true', help='Boolean for whether user wants to watch the AI or not.')
parser.add_argument('-n', '--new_model', dest='new_model', default=False, action='store_true', help='Boolean for whether to create a new model or load from an existing model.')

args = parser.parse_args()

watch_ai = args.watch_ai 
if args.new_model:
    do_it = input('Are you sure you want to create a new model? (y/n)\n')
    new_model = True if do_it == 'y' or do_it == 'Y' else False
else:
    new_model = False
# ML-agents parameters for training
env_path = '../env/AnimalAI'
worker_id = random.randint(1, 100)
seed = 10
base_port = 5005
sub_id = 1
run_id = args.model_name
save_freq = 5000
curriculum_file = './configs/curriculums/y_maze/'
load_model = not new_model
train_model = not watch_ai
keep_checkpoints = 5000
lesson = 0
run_seed = 1
docker_target_name = None
model_path = './models/{run_id}'.format(run_id=run_id)
summaries_dir = './summaries'
maybe_meta_curriculum = MetaCurriculum(curriculum_file)

# My modified parameters
trainer_config_path = 'configs/trainers/curious_trainer_config.yaml'
default_arena = 'configs/arenas/baseline_arena.yaml'
number_arenas = 1 if watch_ai else 16

def load_config(trainer_config_path):
    try:
        with open(trainer_config_path) as data_file:
            trainer_config = yaml.load(data_file)
            return trainer_config
    except IOError:
        raise UnityEnvironmentException('Parameter file could not be found '
                                        'at {}.'
                                        .format(trainer_config_path))
    except UnicodeDecodeError:
        raise UnityEnvironmentException('There was an error decoding '
                                        'Trainer Config from this path : {}'
                                        .format(trainer_config_path))


def init_environment(env_path, docker_target_name, worker_id, seed):
    if env_path is not None:
        # Strip out executable extensions if passed
        env_path = (env_path.strip()
                    .replace('.app', '')
                    .replace('.exe', '')
                    .replace('.x86_64', '')
                    .replace('.x86', ''))
    docker_training = docker_target_name is not None

    return UnityEnvironment(
        n_arenas=number_arenas, # Change this to train on more arenas
        file_name=env_path,
        worker_id=worker_id,
        seed=seed,
        docker_training=docker_training,
        play=False,
        inference=watch_ai # True to watch agent play
    )


# If no configuration file is provided we use the default arena
arena = default_arena if args.arena_config is None else args.arena_config
arena_config_in = ArenaConfig(arena)

trainer_config = load_config(trainer_config_path)
env = init_environment(env_path, docker_target_name, worker_id, run_seed)

external_brains = {}
for brain_name in env.external_brain_names:
    external_brains[brain_name] = env.brains[brain_name]

# Create controller and begin training.
tc = TrainerController(model_path, summaries_dir, run_id + '-' + str(sub_id),
                       save_freq, maybe_meta_curriculum,
                       load_model, train_model,
                       keep_checkpoints, lesson, external_brains, run_seed, arena_config_in)
start = datetime.datetime.now()
tc.start_learning(env, trainer_config)
end = datetime.datetime.now()
total_time = end - start
print(f'Finished training after {round(total_time.seconds / 60 / 60, 3)} hours.')