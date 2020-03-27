# The Indian Council of Medical Research - ICMR

URL:  [The Indian Council of Medical Research - ICMR](https://icmr.nic.in/)

Publishes the latest country level SARS-CoV-2 (COVID-19) testing status data. We have archived the data so we can get time series. 


Before using this data, please note the following:
 
 1. The Indian Council of Medical Research - ICMR
 2. We only arhive, scrape and parse the data.


## DataMeet Discussions 
You can follow and participate in discussions at [DataMeet](https://groups.google.com/forum/#!topic/datameet/_HnOB5iyEx0)

## Tests At the Country
### PDF Archive

We backup the PDFss as and when it gets published. You can find them inside [icmr](https://github.com/datameet/covid19/tree/master/icmr-backup) folder.

### Parsed Data

Parsed data in the form of JSON is availabe inside [data](https://github.com/datameet/covid19/tree/master/data). We update once a day. It has historical data since 2020-03-13T10:00:00.00+05:30

There is one record for each state and report_time combination.

```
{  "id":"2021-03-25T20:00:00.00+05:30|tests",
   "key":"2021-03-25T20:00:00.00+05:30|tests",
   "value":{
         "_id":"2021-03-25T20:00:00.00+05:30|tests",
         "_rev":"1-435ca9af11c6be824876c1cff38fa49e",
         "report_time":"2021-03-25T20:00:00.00+05:30",
         "samples":25144,
         "individuals":24254,
         "confirmed_positive":581,
         "source":"icmr",
         "type":"tests"
      }
}
```

### API
Send an email to thej@datameet.org to get access to API.





## Projects Using this dataset
1. Add

## Credit
Please credit DataMeet if you use this data.
