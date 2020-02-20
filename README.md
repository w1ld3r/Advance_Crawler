# Advance Crawler

Crawler using Selenium, generating a graph to display results.

This crawler can be use as a spider.

## Getting Started

### Prerequisites

Install python3 and pip:
```
sudo apt install python3 python3-pip
```

Install chromium and chromium-driver:
```
sudo apt install chromium chromium-driver
```

### Installing

The installation has been tested in Debian bullseye/sid x86\_64 (february 2019)

#### Clone the project
```
git clone https://github.com/x1n5h3n/Advance_Crawler.git
```

#### Move in the project folder
```
cd Advance_Crawler
```

#### Install the necessary Python packages:
```
pip3 install -r requirements.txt
```

### Usage

Crawl an url using default options:
```
python3 crawler.py -u https://github.com
```

Crawl an url using a blacklist of url (ex: https://google.com):
```
python3 crawler.py -u https://github.com -b blacklist.txt
```

Crawl an url with a define depth (default 1):
```
python3 crawler.py -u https://github.com -d 10
```

Crawl an url and display result with a mode (default domain):

* **domain** mode will return unique domains found
* **link** mode will return unique links found
```
python3 crawler.py -u https://github.com -m link
python3 crawler.py -u https://github.com -m domain
```

Crawl an url using a mobile emulation (default false):
```
python3 crawler.py -u https://github.com -e true
```

Crawl an url without crawling external domains (default true):
```
python3 crawler.py -u https://github.com -a false
```

Crawl like a spider:
```
python3 crawler.py -u https://github.com -d 1337 -m link -a false
```

Print help:
```
python3 crawler.py -h
```

## Authors

* **[x1n5h3n](https://github.com/x1n5h3n)**

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.


