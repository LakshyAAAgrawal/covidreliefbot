# CovidRelief Bot
A telegram chatbot to follow Covid resources in India. Can be added to covid resource groups or used with DM.

Features:
1. /find_leads - Verified leads for resources at given location. Either select a message with a request as a reply or just write the request, "/find_leads oxygen in delhi". Oxygen and Beds supported at the moment.
2. /tweets - Find twitter feed of leads for resource at location - "/tweets oxygen in delhi"
3. Extract information from images - Name of resource, contact number and location.

Can be used by visiting [https://t.me/covidreliefbot](https://t.me/covidreliefbot)

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
