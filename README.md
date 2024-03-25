# ReTrace

ReTrace is a python script that can be used to trace redirects. This tool can be used for OSINT and to assist in tracking, and analysing malware campaigns.

Currently ReTrace can detect:

-   Header redirects  _(201, 301, 302, 303, 307, and 308 redirects)_
-   Meta Refresh redirects

For each redirect ReTrace will retrieve:

-   URL
-   Type
-   Status code
-   Redirect delay

> [!NOTE]
> Redirect delay is only for meta refresh redirects, all other redirects will report 0.0s. It also does not take into account loading times of the website you are being redirected to. It only displays the time before the page redirects you.

This data will then be displayed in a table in the CLI.

While building ReTrace I have discovered that in some cases meta redirects can behave in odd ways. I have documented my discoveries in [META_REFRESH.md](META_REFRESH.md). ReTrace is built to handle meta redirects in the same way as Chrome. 

> [!NOTE]
> If you use ReTrace in any research or anything published, credit or a shoutout would be appreciated!

## Usage

`python retrace.py -u URL -a USER_AGENT`

The user agent argument is optional and if not set will use the default of `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36`

## Usage Example

```bash
$ python retrace.py -u https://bit.ly/4crtUGS      

 ___ ___ _____ ___    _   ___ ___
| _ \ __|_   _| _ \  /_\ / __| __|
|   / _|  | | |   / / _ \ (__| _|
|_|_\___| |_| |_|_\/_/ \_\___|___|

by barleybobs

╭────────────────────────────────────┬────────┬───────────────────────┬───────╮
│ URL                                │ Type   │ Status Code           │ Delay │
├────────────────────────────────────┼────────┼───────────────────────┼───────┤
│ https://bit.ly/4crtUGS             │ Header │ 301 Moved Permanently │ 0.0s  │
│ http://google.com/                 │ Header │ 301 Moved Permanently │ 0.0s  │
│ http://www.google.com/             │ Header │ 302 Found             │ 0.0s  │
│ https://www.google.com/?gws_rd=ssl │        │ 200 OK                │       │
╰────────────────────────────────────┴────────┴───────────────────────┴───────╯
```

Each URL is displayed along with its type _(the way it is redirecting to the next URL)_, status code, and delay.

## Requirements

`requests` is required. All other libraries are standard libraries that come with python.

## Disclaimer

I take no responsibility for the actions of users of this tool or what they do with it.