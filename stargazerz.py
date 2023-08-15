import requests
import re
import threading
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

class Crawler:
    def __init__(self, threads: int, target: str) -> None:
        self.threads = threads
        self.target = target.split('/')  # Split "Frikallo/MISST" into ["Frikallo", "MISST"]
        self.stargazers = []
        self.emails = []
        self.user_email = {}

    def get_all_stargazers(self, username, repository, page=1):
        print(f"Fetching page {page} of stargazers for {username}/{repository}.")
        url = f'https://github.com/{username}/{repository}/stargazers?page={page}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            stargazers = soup.find_all('img', {'class': 'avatar avatar-user'})

            for stargazer in stargazers:
                self.stargazers.append(stargazer['alt'][1:])
                self.user_email[stargazer['alt'][1:]] = "Not retrieved :("

            if len(stargazers) > 0:
                self.get_all_stargazers(username, repository, page + 1)
        elif response.status_code == 429:
            time.sleep(1)
            self.get_all_stargazers(username, repository, page)
        
    def _get_repo(self, username, index=0):
        url = f'https://github.com/{username}?tab=repositories'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            repo_list = soup.find_all('h3', {'class': 'wb-break-all'})

            if repo_list:
                try:
                    latest_repo = repo_list[index].text.strip().split("\n")[0]
                except IndexError:
                    #print("No more repositories found for the user.")
                    return None
                return latest_repo
            else:
                #print("No repositories found for the user.")
                return None
        elif response.status_code == 429:
            time.sleep(1)
            return self._get_repo(username, index)
        else:
            #print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
        
    def _get_latest_commit_info(self, username, repository):
        url = f'https://github.com/{username}/{repository}/commits'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            commit_info = soup.find_all('a', href=True)
            commit_url = None
            
            for a in commit_info:
                if f"/{username}/{repository}/commit/" in a['href']:
                    commit_url = a['href']

            if commit_url:
                latest_commit_url = f'https://github.com{commit_url}'
                return latest_commit_url
            else:
                #print(f"No commits found for {username}/{repository}.")
                return None
        elif response.status_code == 429:
            time.sleep(1)
            return self._get_latest_commit_info(username, repository)
        else:
            #print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
        
    def _find_first_match_between_tags(self, text):
        pattern = r'<(.*?)>'
        match = re.search(pattern, text)
        
        if match:
            return match.group(1)
        else:
            return None
        
    def _get_latest_commit_patch_email(self, user, attempts=0):
        user = user.strip()
        latest_repo = self._get_repo(user, attempts)

        if not latest_repo:
            #print(f"The user {user} does not have any public repositories.")
            return

        latest_commit_patch_url = self._get_latest_commit_info(user, latest_repo)

        if not latest_commit_patch_url:
            return None
        latest_commit_patch_url += ".patch"

        response = requests.get(latest_commit_patch_url)
        email = self._find_first_match_between_tags(response.text)

        return email
    
    def fetch_emails(self, stargazers):
        for stargazer in stargazers:
            for i in range(4): # Try 4 times before giving up
                email = self._get_latest_commit_patch_email(stargazer, i)
                
                if email is not None:
                    if "noreply" not in email:
                        self.pbar.set_description(f"Fetching {stargazer} attempt {i + 1} of 4 ✅")
                        break
                    else:
                        self.pbar.set_description(f"Fetching {stargazer} attempt {i + 1} of 4 ❌")
                else:
                    self.pbar.set_description(f"Fetching {stargazer} attempt {i + 1} of 4 ❌")

            if email is not None:
                if "noreply" not in email:
                    self.emails.append(email)
                    self.user_email[stargazer] = email
            self.pbar.update(1)

    def run(self):
        self.get_all_stargazers(self.target[0], self.target[1])
        self.pbar = tqdm(total=len(self.stargazers), desc="Fetching emails", unit="stargazers", leave=False)
        chunk_size = len(self.stargazers) // self.threads
        stargazer_chunks = [self.stargazers[i:i + chunk_size] for i in range(0, len(self.stargazers), chunk_size)]

        threads = []
        for chunk in stargazer_chunks:
            thread = threading.Thread(target=self.fetch_emails, args=(chunk,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.pbar.close()

    def _clean(self, items):
        items = [item.strip() for item in items]
        items = list(set(items))
        return items
    
    def results(self):
        cleaned_stargazers = self._clean(self.stargazers)
        cleaned_emails = self._clean(self.emails)
        print(f"{len(cleaned_stargazers)} stargazers.\n{len(cleaned_emails)} emails.")
    
    def save_results(self,  mode: str, file: str):
        if mode == "emails":
            cleaned_emails = self._clean(self.emails)
            
            with open(file, "w") as f:
                for email in cleaned_emails:
                    f.write(email + "\n")
        elif mode == "stargazers":
            cleaned_stargazers = self._clean(self.stargazers)
            
            with open(file, "w") as f:
                for stargazer in cleaned_stargazers:
                    f.write(stargazer + "\n")
        elif mode == "all":
            with open(file, "w") as f:
                for username, email in self.user_email.items():
                    f.write(f"{username} {email}\n")
        else:
            print("Mode not supported. Use 'emails' or 'stargazers'.")
            return
        
if __name__ == "__main__":
    crawler = Crawler(threads=16, target="Frikallo/MISST")
    crawler.run()
    crawler.results()
    crawler.save_results("emails", "emails.txt")
    crawler.save_results("stargazers", "stargazers.txt")
    crawler.save_results("all", "all.txt")