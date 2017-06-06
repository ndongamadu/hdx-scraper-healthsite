# hdx-scraper-healthsite
This application is using the HDX and the Healthsites Global Mappging Project APIs to automate the process of country data extraction from healthsites and sharing to HDX platform.
See :
- [HDX Python Library API documentation](https://github.com/OCHA-DAP/hdx-python-api)
- [Healthsites API documentation](healthsites API documentation https://github.com/healthsites/healthsites/wiki/API)

for more information.

## Download
```
git clone https://github.com/ndongamadu/hdx-scraper-healthsite.git
```
## Run it
Open a terminal and run the install script to setup. This will install a virtualenv and install all the requirements.
```
cd hdx-scraper-healthsite
python install.py
```
### HDX API key 
Get into HDX website and save your API in your home directory.
The process is well documented in the [HDX API repository](https://github.com/OCHA-DAP/hdx-python-api) : Usage -> Getting started -> Obtaining your API Key.

### Setup country to download/update
Open the ```healhsite2.py``` file. 
In ```def main()``` function, edit ```countries``` variable by adding the country name and its ISO3 code using this format : 
```
countries = {
'Country': "ISO3"
}
```

If adding many countries : 
```
countries = {
'Country1': "ISO3",
'Country2': "ISO3",
'Country3': "ISO3"}
```

### Running the script
Open a terminal and execute the following command 
```
python execute.py
```

# Data
The generated datasets are available in hdx from this link : https://data.humdata.org/organization/healthsites