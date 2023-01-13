#!/bin/zsh

source ~/.zshrc
python -m flask --app app --debug run --host=0.0.0.0 --port=5001
