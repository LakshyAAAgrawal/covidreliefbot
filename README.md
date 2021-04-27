# CovidRelief Bot
A telegram chatbot to follow Covid resources in India

## Development Setup
1. Clone the repository
2. Execute
   ```bash
   cp src/config.json.sample src/config.json
   ```
3. Enter the configuration details in src/config.json
4. create a virtual environment for python:
   ```
   virtualenv covidreliefbot
   ```
   Activate the virtual environment
   ```
   source covidreliefbot/bin/activate
   ```
5. Install the required modules:
   ```
   pip install -r requirements.txt
   ```
6. Run the bot
   ```
   cd tessdata
   export TESSDATA_PREFIX=$(pwd)
   cd ../src/
   python3 main.py
   ```	
