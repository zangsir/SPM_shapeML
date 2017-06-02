#!/bin/bash

echo ----------------------build_tone_rec_data...
python build_tone_rec_data.py

echo ----------------------build_graph...
python build_graph.py -build

echo ----------------------threshod experiment...
python threshold_CC.py