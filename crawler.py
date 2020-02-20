from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
import argparse

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
DOMAIN = '{uri.scheme}://{uri.netloc}'

def parse(args):
    parser = argparse.ArgumentParser(description='Advance Crawler')
    parser.add_argument('-u', '--url', metavar='URL', type=str, required=True, help='url to crawl')
    parser.add_argument('-b', '--blacklist', metavar='BlackList', type=argparse.FileType('r'), help='balcklist file of domains', default=set())
    parser.add_argument('-d', '--depth', metavar='depth', type=int, help='depth, default is 1', default=1)
    parser.add_argument('-m', '--mode', metavar='mode', type=str, help='mode (domain|link), default is domain', default="domain")
    parser.add_argument('-e', '--mobile', metavar='mobile', type=str, help='mobile emulation (True|False), default is False', default="false")
    parser.add_argument('-a', '--external', metavar='external', type=str, help='allow external (True|False), default is True', default="true")

    if len(args) == 1:
        parser.print_help()
        sys.exit(2)
    else:
        return get_args(parser.parse_args())

def get_args(args):
    url = ""
    blacklist = set()
    depth = 1
    mode = "domain"
    mobile = False
    external = False

    try:
        if args.url:
            u = args.url
            val = URLValidator()
            try:
                val(u)
                url = u
            except ValidationError:
                print("url is invalid")
        if args.blacklist:
            blacklist = file_tolist(args.blacklist)
        if args.depth and args.depth > 0:
            depth = args.depth
        if args.mode:
            if args.mode == "domain":
                mode = args.mode
            elif args.mode == "link":
                mode = args.mode
        if args.mobile.lower() == "true":
            mobile = True
        if args.external.lower() == "true":
            external = True
    except Exception as e:
        sys.exit('Input not reconize !\n%s' % e.message)
    
    return url, blacklist, depth, mode, mobile, external

def file_tolist(file):
    blacklist = set()
    for line in file:
        for word in line.split():
            blacklist.add(word)
    return blacklist

def parse_url(url):
    parsed_uri = urlparse(url)
    return DOMAIN.format(uri=parsed_uri)

def get_chrome_options(mobile_emulation):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--ignore-certificate-errors")

    # handle mobile version crawler
    if mobile_emulation:
        device_emulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
        }
    else:
        device_emulation = {"deviceMetrics": {"width": 1920, "height": 1080}}

    return chrome_options.add_experimental_option("mobileEmulation", device_emulation)

def get_source_code(url, chrome_options):
    # get sourcecode using selenium
    try:
        with webdriver.Chrome(
            CHROME_DRIVER_PATH, options=chrome_options
        ) as driver:
            driver.get(url)
            return driver.page_source
    except:
        print("Error with get url: %s" % url)
        return ""

def get_links(source_code, domain):
    links = set()
    # find urls in source code using bs4
    soup = BeautifulSoup(source_code, 'html.parser')

    for link in soup.findAll("a", href=True):
        link = link["href"]
        if link.startswith('http') or link.startswith('/'):
            if link.startswith('/'):
                links.add(domain+link)
            else:
                links.add(link)
    return links

def get_unique_domain(f_result):
    result = {'data':[]}
    links = set()
    for domains in f_result['data']:
        source = parse_url(domains['url'])
        for domain in domains['links']:
            links.add(parse_url(domain))
        result['data'].append({'source': source, 'links': links})
    return result

def get_unique_links(f_result):
    result = {'data':[]}
    links = set()
    for sources in f_result['data']:
        source = sources['url']
        for destination in sources['links']:
            links.add(destination)
        result['data'].append({'source': source, 'links': links})
    return result

def generate_graph(result):
    matplotlib.use('TkAgg')
    g = nx.Graph()
    for domains in result['data']:
        source = domains['source']
        for domain in domains['links']:
            g.add_edge(source, domain)
    nx.draw_networkx(g, with_labels=True, edge_color="skyblue")
    plt.show()

def is_already_scanned(link, result):
    for source in result['data']:
        if link == source['url']:
            return True
    return False

def get_result(f_result, mode):
    if mode == "domain":
        # get unique domain name
        d_result = get_unique_domain(f_result)
        return d_result
    elif mode == "link":
        # get unique links
        l_result = get_unique_links(f_result)
        return l_result
    else:
        return f_result

def crawler(url, blacklist=set(), depth=1, mode='domain', mobile_emulation=False, allow_external=False):
    # initialisation of result object
    f_result = {"data": []}
    # initialisation of links list
    links = set()
    links.add(url)
    # define origine url
    origine = parse_url(url)

    chrome_options = get_chrome_options(mobile_emulation)
    for _ in range(depth):
        for url in links:
            domain = parse_url(url)
            if domain == "" or domain in blacklist:
                continue
            if not allow_external and domain != origine:
                continue
            if is_already_scanned(url, f_result):
                continue
            source_code = get_source_code(url, chrome_options)
            links = get_links(source_code, domain)
            # adding data to the result object for this page
            f_result["data"].append({"url":url, "links":links})
    return get_result(f_result, mode)

if __name__== "__main__":
    url, blacklist, depth, mode, mobile, external = parse(sys.argv)
    result = crawler(url, blacklist, depth, mode, mobile, external)
    #print(result)
    # genrate graph
    generate_graph(result)