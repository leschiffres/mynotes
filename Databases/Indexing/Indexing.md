# An example of indexing

https://stackoverflow.com/questions/107132/what-columns-generally-make-good-indexes
https://stackoverflow.com/questions/1108/how-does-database-indexing-work

Fastest way of deploying a database on the localhost: 

```
docker pull postgres
docker run --rm -p 1283:5432 postgres:latest
```

## indexing.py

Connects with the postgres database in the localhost and creates a table with the name cards. The table consists of two columns: the number abd suit. Then a pandas dataframe is created containing a deck of cards. However to scale the things up we add for each suit (Clubs, Spades, Hearts, Diamonds) all the numbers from 1 to 50 000. Using pandas we shaffle the deck and insert the data in the cards table. The indexing is applied on both columns. Then we measure the time needed to run a query before and after indexing.
