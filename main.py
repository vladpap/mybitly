import os
import sys
import argparse
import requests
from requests.exceptions import HTTPError
from urllib.parse import urlparse
from dotenv import load_dotenv


def createArgParser ():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument ('link', nargs='?')
    return arg_parser

def shorten_link(token, link):
    body = {"long_url": link}
    response = requests.post(url="https://api-ssl.bitly.com/v4/bitlinks",
                             headers={"Authorization": f"Bearer {token}"},
                             json=body)
    response.raise_for_status()
    short_link = response.json()["link"]
    return short_link


def counted_clicks(token, link):
    parsed_link = urlparse(link)
    bit_link = "{0}{1}".format(parsed_link.netloc, parsed_link.path)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(bit_link)
    response = requests.get(url=url, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(link, token):
    parsed_link = urlparse(link)
    bit_link = "{0}{1}".format(parsed_link.netloc, parsed_link.path)
    response = requests.get(url="https://api-ssl.bitly.com/v4/bitlinks/{}".format(bit_link),
                           headers={"Authorization": f"Bearer {token}"})
    return response.ok


def main():
    load_dotenv()
    token = os.getenv("BITLY_TOKEN")
    arg_parser = createArgParser()
    input_link = arg_parser.parse_args().link
    try:
        if is_bitlink(input_link, token):
            clicks_count = counted_clicks(token, input_link)
            print(f"По вашей ссылке перешли: {clicks_count} раз(а)")
        else:
            short_link = shorten_link(token, input_link)
            print(f"Короткая ссылка: {short_link}")
    except HTTPError as http_err:
        print(f'HTTP ошибка: {http_err}')


def main2():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument ('link', nargs='?')
    print (arg_parser.parse_args().link)

if __name__ == '__main__':
    main()
    # main2()
