from bs4 import BeautifulSoup
import requests
archive_url = "https://www.liveatc.net/archive.php"
archive_server = "http://archive-server.liveatc.net"
def get_all():
    all_feeds = []
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    facilities = soup.find("select", {"name": "facility"}).findAll("option")
    for each in facilities:
        all_feeds.append(each['value'])
    return all_feeds

def get_airport(airport):
    all = get_all()
    results = []
    for each in all:
        if airport.lower() in each.lower():
            results.append(each)
    results = set(results)
    return results

def get_audio(airport, feed, time):
    url = "%s/%s/%s-%s.mp3" % (archive_server, airport.lower(), feed, time)
    local_filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    print("Saved: %s" % local_filename)
    return local_filename