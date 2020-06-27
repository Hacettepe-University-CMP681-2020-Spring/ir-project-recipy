# Recipy
A recipe retrieval system which enables users to query recipes by specifying wanted and unwanted
ingredients, tools and techniques with considering the unstructured instructions text of recipes.

## Installation
1. Download the repository and navigate to the directory that contains `requirements.txt` file.
2. Create a [Python 3.6](https://www.python.org/downloads/release/python-365/) virtualenv and activate it.
    ```bash
   python3.6 -m venv recipy_env
   ```

    ```bash
   source recipy_env/bin/activate
   ```
3. Install the requirements via [pip](https://pip.pypa.io/en/stable/) package manager.
    ```bash
   pip install -r requirements.txt
   ```
4. Start the development server.
    ```bash
   python recipy/manage.py runserver
   ```
5. If above steps were successful, navigate to http://localhost:8000/ on your browser to test the app locally. **It will use the remote database. So no database configuration required.** 

## Database Configuration (If you want to use your own database)
1. Download and install [PostgreSQL 12](https://www.postgresql.org/download/) on your machine.
2. Create an empty database on the PostgreSQL.
3. Set the database credential related settings under `recipy/recipy/settings.py` file.
    ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': '{DB_NAME}',
           'USER': '{DB_USER}',
           'PASSWORD': '{DB_USER_PASSWORD}',
           'HOST': '{DB_ADDRESS}',
           'PORT': '{DB_PORT}',
       }
   }
   ```
4. Migration files are included in the repository so only `migrate command will be sufficient to create tables on the database.
    ```bash
   python recipy/manage.py migrate
   ```
5. Insert your own recipe records into the `main_recipe` table on the database.
6. Recreate indexes and statistical thesaurus.
    1. Open the Python shell of the app.
        ```bash
       python recipy/manage.py shell
       ```
    2. Run the scripts over the Python shell of the app.
        ```python
       from main.utilities.index_creator import *
       
       build_index()
       build_statistical_thesaurus()
       ```
    3. Save the indexes as binary files with pickle over the Python shell of the app.
        ```python
       import pickle
       from main.utilities.index_creator import *
       
       with open('pickles/all_documents.txt', 'wb') as f:
           pickle.dump(ALL_DOCUMENTS, f)

       with open('pickles/index.txt', 'wb') as f:
           pickle.dump(INDEX, f)

       with open('pickles/thesaurus.txt', 'wb') as f:
           pickle.dump(STATISTICAL_THESAURUS, f)
       ```
 