# google_hotels_scraper

Please follow these steps to setup the project.

clone the project to your local machine.
inside the root directory of the project folder run the command python3 -m venv myenv to create a new python virtual environment
activate the virtual environment by running source myenv/bin/activate
install the required libraries by running pip install -r requirements.txt
input values for hotel name can be given inside the file called input_hotel_names.csv.
multiple hotel names can be provided as row by row in the input csv file to collect multiple hotels details in one go.
Finally, run the spider using the command scrapy crawl main
output will be saved to outputs.csv where we can see all the scraped data of hotels that we given as input.

Thank You
