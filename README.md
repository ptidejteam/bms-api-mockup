## Flask Application Setup and Run Instructions
This README provides instructions for setting up and running the Flask applications for the desigo, enteliweb, and metasys packages. Each package contains an app.py file that runs on a different port.

### Prerequisites
Python 3.x installed

### Setup Instructions
1. Clone the Repository Clone the repository containing the desigo, enteliweb, and metasys packages to your local machine.

```
git clone https://github.com/ptidejteam/bms-api-mockup
cd bms-api-mockup
```


2. Install Dependencies Navigate to the root directory of the project and install the required dependencies using the single requirements.txt file. It’s recommended to use a virtual environment.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Applications
Each application can be run separately on different ports. 
Below are the instructions for running each application.

<em> NB: You must rename `sample_env` to `.env` before running any of the applications </em>

1. Run enteliweb Application
```
cd enteliweb
source ../venv/bin/activate
python app.py
```


2. Run metasys Application
```
cd ../metasys
source ../venv/bin/activate
python app.py
```

3. Run desigo Application
```
cd ../desigo
source ../venv/bin/activate
python app.py
```

### Importing Postman Collections
1. Open the Postman application.
2. Click on the Import button located in the top-left corner of the app.
3. In the Import modal, select the File tab.
4. Click Upload Files and select the files in teh `postman_collections` folder to import them.
5. Postman will automatically import the collections and display it in the Collections tab.

<em>Note that the Python application(s) must be running before using the Postman documentation 
after the importation<em>
