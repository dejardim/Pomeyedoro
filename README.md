# Pomeyedoro - Eye Feedback Tracking

![banner](https://imgur.com/JK7HQOt.png)

## Description
Pomeyedoro is an eye-tracking influenced by Pomodoro timer. It leverages the power of computer vision to track eye blinks and provides feedback based on the session duration.

## Requirements
- Tested on macOS. Should work on Linux but hasn't been extensively tested.
- Conda as package manager and environment management system.

## Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/dejardim/Pomeyedoro.git
cd Pomeyedoro
```

2. Create a conda environment:

```bash
conda create -n pomeyedoro_env python=3.8
```

3. Activate the environment:

```bash
conda activate pomeyedoro_env
```

3. Install the dependicies:

```bash
pip install -r requirements.txt
```


## Running the application

1. Run the Server:

```bash
uvicorn src.server:app --port 8000
```

2. Run the Eye Tracker:

```bash
python src/eye_tracker.py
```


3. Run the Dashboard:

```bash
streamlit run dashboard.oy
```

## License
[MIT](LICENSE)
