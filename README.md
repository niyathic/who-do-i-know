# who-do-i-know
Last updated April 2026. Created by @niyathic (GitHub).

Go through someone's exported LinkedIn connections and output a file with just the connections whose companies are hiring for a particular role, and how many roles appeared with that company for your keywords.

-- BEFORE RUNNING THIS PROGRAM, ENSURE YOU: --

1. Set the file path of the exported LinkedIn Connections file as 
LI_CONNECTIONS_FILEPATH in the below config.
    -- How to export LinkedIn connections --
    1. Log in to LinkedIn.
    2. From your profile picture icon in the top bar, navigate to "Settings & Privacy".
    3. Navigate to "Data privacy" in the left side options.
    4. Click "Request archive", "Request new archive", or similar.
    5. A link to download the archive will be sent to the main email of the profile 
    in 24 hours. Click the link in the email.
    6. Click "Download archive".
    7. Double-click/unzip the downloaded .zip folder, then click into the new uncompressed folder.
    8. Find the "Connections.csv" file.
    9. Move it if you wish.
    10. Set the filepath as LI_CONNECTIONS_FILEPATH in the below config.
2. Create an empty .csv file and set the filepath as OUTPUT_CSV_FILEPATH in the below config 
(For some reason, in my testing the write (w) and even w+ functions were not, erm, functioning).
3. Fill in the other config items below. If you are searching for multiple roles, you will 
have to run this program for each one.
4. Install Pandas: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html
5. Install Playwright: https://playwright.dev/docs/intro

P.S. Sometimes the browser stuff is funky. I've only run into an error with waiting for 
the session key locator in two runs ever but it was fixed by just running it again, changing 
nothing! So, try that if you need... And sometimes, it just doesn't succesfully get a company's
jobs on one run but does on another. So, I am definitely seeking feedback on that or anything. 
But it gets a ton of job postings for me, so I thought I'd share. I hope it helps you!
Best of luck on your job search.
