import requests
import argparse
import json

from bs4 import BeautifulSoup
from urllib.parse import urlparse

parser = argparse.ArgumentParser(
    prog="Spotify art downloader",
    description="Allows you to download album art from Spotify links",
)

parser.add_argument("url")
parser.add_argument("-r", "--resolution", type=int, choices=[640, 300, 64], default=640)

args = parser.parse_args()

def download_spotify_art(embed_url: str, resolution: int):
    embed_response = requests.get(url=embed_url)
    if not embed_response.ok:
        print(f"Failed to fetch embed page! Status code: { embed_response.status_code }\nReason: { embed_response.reason }")
        return
    
    html_parser = BeautifulSoup(embed_response.content, 'html.parser')

    page_props = html_parser.find(id="__NEXT_DATA__")
    if page_props == None:
        print(f"Failed to find pageProps!")
        return
    
    try:
        page_json = json.loads(page_props.text)
    except json.JSONDecodeError as err:
        print(f"Failed to parse pageProps! Error: { err.msg }")
        return

    try:
        cover_art = page_json['props']['pageProps']['state']['data']['entity']['coverArt']['sources']
    except KeyError as err:
        print(f"Failed to find cover_art object! Failed to find key { err }!")

    for art in cover_art:
        if art['width'] == resolution and art['height'] == resolution:
            print(f"Cover art url: { art['url'] }")
            return

    print(f"Failed to find cover art at provided resolution, attempting to find fallback source!")
    
    for art in cover_art:
        print(f"Cover art url (fallback!): { art['url'] }")
        return
    
    print(f"Failed to find art url!")

if __name__ == '__main__':
    parsed_url = urlparse(args.url)
    embed_url = f"https://open.spotify.com/embed{ parsed_url.path }"

    download_spotify_art(embed_url, args.resolution)