<div align="center">

[![](./stargazerz/Assets/banner.png)](https://github.com/Frikallo/stargazerz)

[![PyPI](https://img.shields.io/pypi/v/stargazerz.svg?color=orange)](https://pypi.org/project/stargazerz/)
[![PyPI - Downloads](https://img.shields.io/pypi/dd/stargazerz?color=orange)](https://pypi.org/project/stargazerz/) 
[![License](https://img.shields.io/github/license/frikallo/stargazerz?color=orange)](https://github.com/Frikallo/stargazerz/blob/main/LICENSE) 
[![GitHub code size](https://img.shields.io/github/languages/code-size/frikallo/stargazerz?color=orange)](https://github.com/Frikallo/stargazerz/tree/main/stargazerz)

</div>

---

###

Original Repository of stargazerz

This application uses state-of-the-art OSINT and webscraping techniques to find emails and usernames of people who have starred a GitHub repository without the need of authentication. This prjects is useful for developers looking to promote their projects or contact developers with similar interests.

This project is OpenSource, feel free to use, study and/or send pull request.

## Key Features

- **Fast**: stargazerz uses multithreading to scrape GitHub pages and find emails and usernames of stargazers.

- **Easy**: stargazerz is easy to use, just define the target repository and the number of threads and you are ready to go.

- **Powerful**: stargazerz uses state-of-the-art OSINT and webscraping techniques to find emails and usernames of stargazers.

- **Customizable**: stargazerz allows you to save the results to a file and choose which results to save.

- **Free**: stargazerz is free and open-source.

## Installation

You can install stargazerz using `pip`:

```shell
pip install stargazerz
```

## Usage
```python
import stargazerz

# Define Crawler
crawler = stargazerz.Crawler(threads=16, target="Frikallo/stargazerz")

# Run Crawler
crawler.run()

# Get Results after Crawler is done
crawler.print_results()

# Save results to file
crawler.save_results("emails", "emails.txt")
crawler.save_results("stargazers", "stargazers.txt")
crawler.save_results("all", "all.txt")
```

## Example Output
```shell
$ python3 stargazerz-example.py
[+] Target: Frikallo/stargazerz
[+] Threads: 16
[+] Starting crawler
[+] Crawler started
[+] Fetching page 1 of stargazers for Frikallo/stargazerz
[+] Fetching page 2 of stargazers for Frikallo/stargazerz
[+] Found 34 stargazers
[+] Fetching emails
Complete ✅: 100%|███████████████| 34/34 [00:18<00:00,  1.40stargazers/s]
[+] Crawler finished
[+] Time: 19.92 seconds
[-] Results
[+] Stargazers: 34
[+] Emails: 26
[+] Emails saved to emails.txt
[+] Stargazers saved to stargazers.txt
[+] All results saved to all.txt
```

