Instructions to run Scraping.py
1. provide the indeed job search url ( eg - url='https://www.indeed.com/jobs?q=Data%20Engineers&l=Redmond%2C%20WA&radius=100&vjk=dd628fd803dd06db')
2. provide regex expression based on the job title (eg - regex_data = "data eng[a-z]+")- This is to elemenate job title form the description to provide better accuracy
3. The method populateJobs in the scraping script takes page numbers (being, end). Eg - populateJobs("IndeedJobs", 0, 1,  url,regex_data)  - Here 0, 1 means scrape all the job in the range 0 to 1 page number.
4. Scraping script will generate one css per job and at the end merges it all to single csv named IndeedJobsCSV_merged.csv
5. It also saves html page source per each job in IndeedJobs folder.
6. Please place the compatible chrome driver in the same folder as the script. (We are using selenium).

Instructions to run Classification.py
1. For classification script to run, please place the provided Training_Merged.csv in the same directory. (Which is already present in the same folder in submission)
2. Testing file (csv) should contain Description as header.
3. Script will generate a file named Final_Output.csv containing predicted job title per line for the each description in testing file.
