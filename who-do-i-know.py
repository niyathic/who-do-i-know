# -- TODO -- YOUR CONFIG --
# LinkedIn login information
LI_EMAIL    = "email@domainprovider.com"     # Your email to log in to LinkedIn
LI_PASSWORD = "password!"            # Your password to log in to LinkedIn
# The job you are searching for
DESIRED_ROLE = "role name"
# The below files must exist with the correct filepaths
LI_CONNECTIONS_FILEPATH = "/Users/username/Downloads/Connections.csv"     # The file path where your downloaded LinkedIn connections file is
OUTPUT_CSV_FILEPATH = "/Users/username/folder/your_filename.csv"          # The file path where the .csv you created is

import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import re
import csv

LI_LOGIN_URL = "https://www.linkedin.com/login"

# Determine search URL keywords from desired role
role_words_list = DESIRED_ROLE.split()
print(role_words_list)
words_num = len(role_words_list)
print(words_num)
keywords = ""
i = 1
for word in role_words_list:
    print(word)
    print(i)
    keywords += word
    print(keywords)
    if(i < words_num):
        keywords += "%20"
        print(keywords)
    i += 1
    print(i)
LI_SEARCH_URL = "https://www.linkedin.com/jobs/search/?keywords=" + keywords
print(LI_SEARCH_URL)

# Open and read the LinkedIn Connections file
f_i = open(LI_CONNECTIONS_FILEPATH)
df = pd.read_csv(f_i, header=3)
print(df)
companies = df["Company"]

# For use getting the number of results for the job search in that company
def get_results_num_for_company(company, button_text, aria_label):
    print("Starting getting match_0")
    match_0 = re.search(r"\d+", button_text)
    if match_0:
        print("Got match_0: ")
        print(match_0)
        print("Getting num")
        num_results = int(match_0.group())
        print("Number of jobs at " + company + f": {num_results}")
        return(num_results)
    else:
        print("Starting getting match_1")
        match_1 = re.search(r"\d+", aria_label)
        if match_1:
            print("Got match_1: ")
            print(match_1)
            print("Getting num")
            num_results = int(match_1.group())
            print("Number of jobs at " + company + f": {num_results}")
            return(num_results)
        else:
            print("Could not parse number of results at " + company)
            return

# Create the output array and fill headers
data = []
headers = ["Connection Name","Connection URL","Company","Number of Roles"]
data.append(headers)
print(data)

'''
# File path for the CSV file
now = datetime.now()
now_str = now.strftime("%m/%d/%Y")
OUTPUT_CSV_NAME = "LI_Connected_Companies_Hiring_PMs_" + now_str
csv_filepath = OUTPUT_CSV_FILEPATH + OUTPUT_CSV_NAME + ".csv"
'''

# Log in & search for each company on LinkedIn
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Go to login
    print("Navigating to login...")
    page.goto(LI_LOGIN_URL)
    page.wait_for_timeout(10000)

    # Fill fields
    print("🔐 Logging in...")
    page.fill("input[name='session_key']", LI_EMAIL)
    page.fill("input[name='session_password']", LI_PASSWORD)

    # Click button
    page.click("button[type='submit']")

    # Wait for navigation
    page.wait_for_timeout(10000)

    # Login error checking
    if "login" in page.url or "checkpoint" in page.url:
        print("⚠️  Login may have failed or needs verification.")
        print("    Please complete login manually in the browser window, then press Enter here.")
        input("Press Enter when you're fully logged in → ")
    else:
        print(f"✅ Logged in. URL: {page.url}")

    # Go to search
    print("Navigating to job search...")
    page.goto(LI_SEARCH_URL)
    page.wait_for_timeout(10000)
    print(f"   URL: {page.url}")

    # Iterate through searching companies for positions
    i = -1
    for company in companies:
        i+=1
        try:
            print(company)
            if(type(company) == float):
                print("Company blank -- skipping")
                continue
            else:
                try:
                    # Find "Company" button at top of search
                    company_btn = page.locator("button[aria-label^='Company']").first
                    #company_btn.wait_for(state="visible", timeout=10000)
                    # Click "Company" button
                    company_btn.click()
                    company_btn.wait_for(state="visible", timeout=10000)
                    print("Filtering company")
                    # Find text input
                    company_input = page.locator("input[aria-label='Add a company']")
                    print("Adding company filter")
                    # Input this company
                    company_input.click(delay=80)
                    company_input.wait_for(state="visible", timeout=10000)
                    company_input.type(company)
                    #page.wait_for_timeout(10000)
                    company_input.fill(company)
                    print("Company filter added")
                    # Wait for dropdown options to appear
                    page.wait_for_selector("div[role='option']", state="visible", timeout=10000)
                    print("Waited for dropdown options")
                    # Click the matching company from dropdown
                    try:
                        page.locator(f"div[role='option']:has-text('{company}')").first.click(delay=80)
                        print("Clicked company from dropdown")
                    except:
                        print("Failed to find company in dropdown options")
                        continue
                    # Find "Show (x number) result(s)" button
                    showresults_btn = page.locator("button:has-text('show'):has-text('result')").first
                    print("Found show results button")
                    #showresults_btn.wait_for(timeout=20000)
                    #print("Waited for show results button")
                    # Get number of results
                    showresults_btn_innertext = showresults_btn.inner_text()
                    print("Got inner text: ")
                    print(showresults_btn_innertext)
                    showresults_btn_arialabel = showresults_btn.get_attribute("aria-label")
                    print("Got aria label: ")
                    print(showresults_btn_arialabel)
                    if "K+" in showresults_btn_innertext or "K+" in showresults_btn_arialabel:
                        print("!!!!!!! DID NOT SUCCESSFULLY filter to company before attempting to press results button. Skipping!!!!!!!")
                        continue
                    else:
                        print("Getting results num...")
                        results_num = get_results_num_for_company(company, showresults_btn_innertext, showresults_btn_arialabel)
                        print(results_num)
                        # Add connection, company, and results info to output array if there are results
                        if results_num > 0:
                            new_row = [df["First Name"][i] +" "+df["Last Name"][i], df["URL"][i], company, results_num]
                            print(new_row)
                            data.append(new_row)    
                            print(data)
                        else:
                            continue
                except PlaywrightTimeout:
                    print("⚠️  FAILED selecting company: " + company)
        except:
            # Output existing data into file in case of any error encountered in company list from connections file
            with open(OUTPUT_CSV_FILEPATH, mode='w+', newline='') as file:
                # Create a csv.writer object
                writer = csv.writer(file)
                # Write data to the CSV file
                writer.writerows(data)
                # Print a confirmation message
                print("File updated!")    
    browser.close()

# Write results to file after iterating through company list from connections file
with open(OUTPUT_CSV_FILEPATH, mode='w+', newline='') as file:
     # Create a csv.writer object
    writer = csv.writer(file)
    # Write data to the CSV file
    writer.writerows(data)
    # Print a confirmation message
    print("File updated!")
