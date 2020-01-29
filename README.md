# bloomon
Code challenge

To run:
Clone the repository and go to project folder using your commandline tool:

.. code-block:: bash

    cd bloomon

Copy your stream data to stream.txt or leave it as it is for default stream data
Run next commands:

.. code-block:: bash

    docker build -t flowers .
    
    docker run flowers


It will output bouqutes. 

After that you can run script from inside docker container if needed:

.. code-block:: bash

    python bouquets_from_flowers.py --path PATH_TO_FILE_TO_STREAM_FROM
