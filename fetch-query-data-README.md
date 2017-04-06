#### 3A: fetch-query-data task
The  **fetch-the-query-data** task is to 
  1. download the spreadsheet from Google Drive, and
  2. write it as a comma-separated-value file on our local filesystem.


We can easily do this operation through the **File >> Download As** menu option
  of the Google spreadsheet if no one wants to learn how to do this programmatically.
It is nice to know how to do this programmatically, so that you can have a pipeline that
  is easy to re-run.

See [http-and-requests-README.md](./http-and-requests-README.md) for background on 
    using `requests`