from jobrunner import JobRunner
from yaml import safe_load
from pprint import pprint


if __name__ == "__main__":  
    # get absolute path of this script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.yaml')
    print(f"Loading config from {config_path}")
    with open(config_path, 'r') as f:
        config = safe_load(f)
        pprint(config)

    runner = JobRunner()
    runner.configure(config)
    pprint(runner.config)
