## 4 Ws

## Overview

Application that recommends music through machine learning. Input songs you like and it will output some songs that are recommended by machine learning. This project aims to be a subsitute to spotify that has more functionality and features. We take in both songs and geography data to output accurate results. It also includes a recommendation system through chatgpt.

## Features

1. **Song Recommender:** User inputs songs and will receive three similar songs determined by machine learning.

2. **Top Tracks:** Ouput the top five tracks based on the spotify global data

3. **ChatGPT Recommender:** User inputs anything related to their music taste and chhatgpt will output similar songs back

4. **Geography Recommender:** User selects their country and will receive similar songs based on that.

5. **Quick Connection to Spotify:** User is able to login in to spotify and retrieve easy access to their playlists.

6. **Data Structures and Operations:** The project will leverage various data structures, such as an online database, to store geography information. CRUD operations (Create, Read, Update, Delete) will be implemented to manage user data. Sorting, data filtering, and query operations will be used to determine songs to recommend.
## Technical Requirements

The following technical components are necessary to implement the project effectively:

- **Online Database:** An online database will be utilized to store user code submissions and scores. CRUD operations (Create, Read, Update, Delete) will be implemented to manage user data effectively.

- **API Keys:** A API key from spotify and openai will be needed for this project

## Build Instructions

Here are the build instructions:

1. Clone the repository to your local machine using the following command:
git clone https://github.com/lwu1822/fourWsFrontend

2. Navigate to the project directory:

3. Install the required dependencies using npm or yarn. Assuming you have npm installed, run the following command:
npm install

This will download all the necessary dependencies defined in the project's package.json file.

4. Modify the API Keys:

If the application requires API keys or any configuration settings, you need to modify the appropriate files in the project to add your own API keys or configurations. Refer to the project's documentation for details on which files to modify and how to add the required information.

5. Build the project:
npm run build

This command will compile the backend code and generate optimized static files in the build directory.

6. Build a local backend server:
npm install -g serve
serve -s build

7. Access the application:
- http://localhost:5000 or the appropriate port number
