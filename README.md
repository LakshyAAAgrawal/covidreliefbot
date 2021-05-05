# CovidRelief Bot
A telegram chatbot to follow Covid resources in India

## Development Setup
1. Clone the repository
2. Execute
   ```bash
   cp src/config.json.sample src/config.json
   ```
3. Enter the configuration details in src/config.json
4. Build the Docker image
   ```bash
   docker build -t covidrelief .
   ```
5. Run the Docker image
   ```bash
   docker run -it covidrelief
   ```