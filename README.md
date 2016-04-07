# Wikipedia-Events-Search

Python application for quering events data from Wikipadia collection of pages about the days of the year.

The data is stored using MongoDB, indexed by day, year and category and is refreshed at 2 hours interval.



The http endpoints support queries by day, year or category(events, births, deaths, holidays_and_observances) and
allow searching by keywords too.

http://127.0.0.1:5000?day=April_7&year=2000
```
{
  "results": [
    {
      "category": "births",
      "day": "april 1",
      "title": "Joe Partington, English-Welsh footballer",
      "year": "1990"
    },
    {
      "category": "births",
      "day": "april 1",
      "title": "Julia Fischer, German discus thrower",
      "year": "1990"
    }
  ]
}
```
http://127.0.0.1:5000?keyword=bucharest&day=january_24
```
{
  "results": [
    {
      "category": "events",
      "day": "january 24",
      "title": "Bucharest is proclaimed the capital of Romania.",
      "year": "1862"
    }
  ]
}
```

##### Docker
Build and run the docker-compose environment
```
docker-compose build
docker-compose up
```
