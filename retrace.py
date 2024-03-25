import argparse, requests, re
from urllib.parse import urlsplit, urljoin, quote

def find_shortest_meta_refresh(location, source_code):
    # Initialize shortest delay as positive infinity
    shortest_delay = float('inf')  
    shortest_url = ""

    # Regex pattern for isolating meta refresh redirects
    pattern = r'<meta\s+http-equiv=(["\'])refresh\1\s*content=(["\'])([\d\.]+)[;,]?(?:\s*(?:url=)?(?!\2)(?:["\'])?\s*(?:http:(?!\/\/))?([^"\']+)(?:["\'])?\2)?'
    
    # Find all meta refresh tags using regex
    matches = re.findall(pattern, source_code)

    # Remove all capturing groups used to make sure quotes match
    matches = list(map(lambda x: x[2:4], matches))

    if not matches:
        return None, None
    
    # Get meta refresh with shortest delay
    # '.'.join(delay_str.split('.')[:2]) is used to handle the weird case that the delay is 1.1.1 or something with multiple decimal places. It would convert 1.1.1 to 1.1
    sorted_matches = sorted(matches, key=lambda x: (float('.'.join(x[0].split('.')[:2])), -matches.index(x)))
    shortest_delay, shortest_url = sorted_matches[0]
    shortest_delay = float('.'.join(shortest_delay.split('.')[:2]))

    # Encode URL component
    parsed_shortest_url = urlsplit(shortest_url)
    encoded_path = quote(parsed_shortest_url.path)

    if parsed_shortest_url.scheme == "" and parsed_shortest_url.netloc == "" and parsed_shortest_url.path in ["url=", ""]:
        # If captured url
        return None, None
    elif re.match(r'//(?![/])', shortest_url) is not None:
        # If redirect is "//google.com" then it should go to http://google.com
        # This is only for "//google.com", "/google.com", "///google.com", etc are all relative
        # This doesn't capture "http://" because the "//" must be at the start as re.match looks at the start of the string
        # It redirects using the protocol being used by the page that is redirecting it
        shortest_url = f"{urlsplit(location).scheme}://{parsed_shortest_url.netloc}{encoded_path}{"?" if parsed_shortest_url.query != "" else ""}{parsed_shortest_url.query}"
    elif parsed_shortest_url.scheme == "":
        # If the redirect is relative then calculate the full url
        shortest_url = urljoin(location, f"{parsed_shortest_url.netloc}{encoded_path}{"?" if parsed_shortest_url.query != "" else ""}{parsed_shortest_url.query}")
    else:
        # Otherwise get the url being redirected to
        # lstrip is used to handle https:/// or http:/// cases and remove the extra / from the scheme
        shortest_url = f"{parsed_shortest_url.scheme}://{parsed_shortest_url.netloc}{encoded_path.lstrip("/")}{"?" if parsed_shortest_url.query != "" else ""}{parsed_shortest_url.query}"

    return shortest_delay, shortest_url



# Take in CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--url", "-u", help="URL to be analysed. Should include https:// or http://.", required=True)
parser.add_argument("--agent", "-a", help="User agent to be used.")
args = parser.parse_args()

location = args.url
user_agent = args.agent
redirects = []

# While there is still a redirect to be processed keep processing
while location:
    # Send a request to the location
    try:
        response = requests.get(location, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36" if user_agent is None else user_agent}, allow_redirects=False)
    except Exception as e:
        if "Failed to resolve" in str(e):
            redirects.append({"location": location, "type": "", "status_code": "Failed to resolve", "delay": ""})
        else:
            redirects.append({"location": location, "type": "", "status_code": "Requests error", "delay": ""})
        break

    # Make all header keys lowercase
    headers = {header.lower(): i for header, i in response.headers.items()}

    # Append dictionary with location and status for each redirect
    redirect = {
        "location": location,
        "status_code": f"{response.status_code} {response.reason}",
    }
    
    if "location" in response.headers and response.status_code in [201, 301, 302, 303, 307, 308]:
        # If redirect is done through response headers (location header)
        # Add details about redirect to record
        redirect["type"] = "Header"
        redirect["delay"] = "0.0s"
        if urlsplit(response.headers["location"]).scheme == "":
            # If the redirect is relative then calculate the full url
            location = urljoin(location, response.headers["location"])
        else:
            # Otherwise get the url being redirected to
            location = response.headers["location"]

    else:
        # Search for meta refresh tags and find the one with the shortest delay
        shortest_delay, shortest_location = find_shortest_meta_refresh(location, response.text)

        if shortest_delay is not None:
            # If there is a meta refresh tag
            # Add details about redirect to record
            redirect["type"] = "Meta Refresh"
            redirect["delay"] = str(shortest_delay) + "s"
            location = shortest_location

        else:
            # Otherwise there are no more redirects
            redirect["type"] = ""
            redirect["delay"] = ""
            location = None

    redirects.append(redirect)

print()
print(r" ___ ___ _____ ___    _   ___ ___ ")
print(r"| _ \ __|_   _| _ \  /_\ / __| __|")
print(r"|   / _|  | | |   / / _ \ (__| _| ")
print(r"|_|_\___| |_| |_|_\/_/ \_\___|___|")
print("\nby barleybobs\n")
                                   

# Display table of redirects
min_lengths = {'location': 3, 'type': 4, 'status_code': 11, 'delay': 5}
lengths = {key: max(max(map(lambda x: len(str(x[key])), redirects)), min_lengths[key]) for key in redirects[0]}

print(f"╭─{"─"*lengths["location"]}─┬─{"─"*lengths["type"]}─┬─{"─"*lengths["status_code"]}─┬─{"─"*lengths["delay"]}─╮")
print(f"\x1b[1m│ URL{" "*(lengths['location'] - 3)} │ Type{" "*(lengths['type'] - 4)} │ Status Code{" "*(lengths['status_code'] - 11)} │ Delay{" "*(lengths["delay"] - 5)} │\x1b[0m")
print(f"├─{"─"*lengths["location"]}─┼─{"─"*lengths["type"]}─┼─{"─"*lengths["status_code"]}─┼─{"─"*lengths["delay"]}─┤")
for redirect in redirects:
    print(f"│ {redirect["location"]}{" "*(lengths["location"] - len(redirect["location"]))} │ {redirect["type"]}{" "*(lengths["type"] - len(redirect["type"]))} │ {redirect["status_code"]}{" "*(lengths["status_code"] - len(redirect["status_code"]))} │ {redirect["delay"]}{" "*(lengths["delay"] - len(redirect["delay"]))} │")
print(f"╰─{"─"*lengths["location"]}─┴─{"─"*lengths["type"]}─┴─{"─"*lengths["status_code"]}─┴─{"─"*lengths["delay"]}─╯")

print()