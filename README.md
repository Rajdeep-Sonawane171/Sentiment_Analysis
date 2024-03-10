Problem Statement :
Design scalable pipeline using spark to read customer review from s3 bucket and store it into HDFS. Schedule your pipeline to run iteratively after each hour. Create a folder in the s3 bucket where customer reviews in json format can be uploaded. The Scheduled big data pipeline will be triggered manually or automatically to read data from The S3 bucket and dump it into HDFS. Use Spark Machine learning to perform sentiment analysis using customer review stores in HDFS


Approach:Design scalable pipeline using spark to read customer review from s3 bucket and store it into HDFS
![air1](https://github.com/Rajdeep-Sonawane171/Sentiment_Analysis/assets/113442602/4c7235bf-950c-4bf6-9b63-6d142795dd79)

Use spark machine learning for creating the model.
![sentiment arch](https://github.com/Rajdeep-Sonawane171/Sentiment_Analysis/assets/113442602/796ae19b-d9a4-4f03-8e83-d4da33272e80)

For running the airflow image in docker use these commond 
```PS C:\Users\admin\Sentiment_Analysis> docker compose up```

