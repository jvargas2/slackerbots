import requests

def ranks():
    data = requests.get('https://bracketchallenge.ncaa.com/api/static-v1/ncaabracketchallenge/group/730609/show.json').json()
    entries = data['entries']
    ranks = "```"

    for entry in entries:
        name = entry['name']
        points = entry['total_points']
        rank = entry['rank']
        ranks += "%s: Rank %d (%d points)\n" % (name, rank, points)

    ranks += "```"
    return ranks

print(ranks())