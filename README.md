# YOLOv5 License Plate Detection for Parking Lot Management System
This repo is supported by: https://github.com/trungdinh22/License-Plate-Recognition.git

## About
This repo is the server for my [Parking Lot Management System app](https://github.com/trungdinh22/License-Plate-Recognition.git).

## How it works:
When the app sends an image of a vehicle's plate, the server will send back a string of the detected plate. Make sure the url in the app backend and the server's IP match for this process to work smoothly.

## Requirements:
All main packages are included in `requirements.txt`
```bash
pip install -r requirements.txt
```

## Usage:
```bash
python main.py
```