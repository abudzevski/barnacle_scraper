from abc import ABC, abstractmethod
from network.dto import NetworkDTO
import time
import random
import requests

#add functionality to the exceptions to return the proper DTO/reevaluate exception behavior

class BaseClient(ABC): #consider changing name to BaseClient

    def open_connection(self, dst: str):
        try:
            url = self._build_url(dst)
            self.wait()
            response = requests.get(url,timeout=10)
            response.raise_for_status()

            return self._parse(response.text)
        
        except requests.exceptions.HTTPError as e: # Handles HTTP errors and deals with rate limiting
            print("HTTP error:", e)
            if e.response.status_code == 429: 
                print("Rate limit hit, backing off...")
                self._wait(3) # much longer wait
                return NetworkDTO(error=e)
            elif e.response.status_code == 403:
                print("Forbidden. Not retrying.")
                return NetworkDTO(error=e)
            elif e.response.status_code >= 500:
                print("Server error, retrying...")
                self._wait(2) # moderate wait
                return NetworkDTO(error=e)
            else: print("Other HTTP error:", e)
            return NetworkDTO(error=e)
        
        except requests.exceptions.ConnectionError as e: # Handles couldnt reach the server
            print("Connection error:", e)
            return NetworkDTO(error=e)
        
        except requests.exceptions.Timeout as e: # Handles not getting a response from he server
            print("Timeout error:", e)
            return NetworkDTO(error=e)
        
        except requests.exceptions.RequestException as e: # Handles anything else
            print("Unexpected error:", e)
            return NetworkDTO(error=e)

    @abstractmethod
    def _build_url(self, dst):
        pass

    @abstractmethod
    def _parse(self, raw_text) -> NetworkDTO:
        pass

    def _wait(self, offset: int = 0): # function responsible for determining delay between calls
        # Base range for normal success case
        #it was found that, at low values 25 pages were coverd in 60s followed by 3min45s before resuming. this patter carried for a bit before 429 became too common.
        #it seems an avg of 13s per page request keeps 429s really low.
        #piror tested valued were 9.6 - 12.8, the avg wait should be around 12.8 ~13s
        base_min = 11.6 #with 11.6 - 13.8 & jitter = 0.2 was able to get 574 pages done in 7750s before 429 with ~13.5s/page, seems to have hit a larger limmit, 6-7 hour ban
        base_max = 13.8

        # Scale up by offset, offsett acts as a multiplier to the min and max delay times.
        delay = random.uniform(base_min, base_max) * (1 + offset)
        # Add jitter (+/- 200ms)
        jitter = random.uniform(-0.25, 0.25) #was 0.2 before
        
        final_delay = max(0, delay + jitter)

        # Periodic longer delay every 20–40 requests
        """if request_count % random.randint(20, 40) == 0 and request_count > 0: 
            extra_delay = random.uniform(5, 10) 
            final_delay += extra_delay"""
        
        time.sleep(final_delay)