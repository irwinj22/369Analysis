James Irwin    
Exploratory Analysis    
02.28.2025     

*Note: reference numbers refer to code sections from the accompanying [Jupyter notebook](issues_code.ipynb), which hosts the code that is used to ground this analysis.*

To identify quality issues within the data, I decided to begin by taking a look at the first forty rows.<sup>1</sup> Quickly, I realized that only a few of the columns provided answers to my [original questions](../proposal.md), so I narrowed my focus to just search for errors and/or inconsistencies within the following columns: 
- taxi_id
- trip_start_timestamp
- trip_end_timestamp
- trip_seconds
- trip_miles
- fare

Additionally, I decided to take your advice and narrow the scope of my analysis to trips that occurred before COVID, since that event would have such a profound influence on the data. I defined "pre-COVID" as any trip that began before January 1st, 2020; this definition left 90.21% of the original observations to explore.<sup>2</sup> 

The first issue that I noticed was that the difference in time between trip_start_timestamp and trip_end_timestamp did not always align with trip_seconds. For example, while the starting timestamp may be 2014-03-20 19:45:00 and the end timestamp 2014-03-20 20:00:00, which indicates a total trip time of 15 minutes, the recorded trip_seconds would be just 660, indicating a total trip time of just 11 minutes. I found this phenomenon to be strange. 

However, as I continued to investigate, I realized that there was an even more pressing issue involving trip_seconds: many observations had a value of either 0 or NULL. This made no sense to me. How could there even be an observation in the first place if the total trip time is just 0 seconds? Moreover, I realized that the same thing was occuring within trip_miles. Many of the observations also had a value of either 0 or NULL. How could this be? 

My first thought was that maybe certain taxis did not record trip duration or length. However, of all the observations that had a 0 in either trip_seconds or trip_miles, just 0.58% had a fare value of 0 or NULL.<sup>3</sup> This means that, for the overwhelming majority of trips with a 0 in either seconds or miles, a fare was calculated. But wouldn't this fare have been calculated using a combination of time and distance? So how could this information not be reported?

Despite not understanding the issue's underlying cause, I decided to try to get a better idea of its scope. Maybe this issue just affects a couple of observations? Well, unfortunately not, as 21.93% of pre-COVID observations have a value of 0 in either trip_seconds or trip_miles.<sup>4</sup> Moreover, the distribution of 0/NULL values is not even across years, as 2013, 2014, 2015, and 2016 contain roughly 80% of the problematic observations.<sup>5</sup>

As for solutions, I have to admit that I am not sure what to do. I feel that, because the problem is so prevalent and not evenly distributed across years, it doesn't make sense to just ignore these observations. However, trip_seconds and trip_miles are integral components to some of the questions that I originally proposed, such as: 
- What is the total number of miles traveled in taxis? 
- What is the total number of time spent in taxis? 
- How long, on average, was each trip in minutes? 
- How long, on average, was each trip in miles? 

Thus, I am asking for your help in trying to address this issue. What would you recommend that I do? 


