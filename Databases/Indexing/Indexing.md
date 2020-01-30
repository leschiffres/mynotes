# An example of indexing

Like indexing in a notebook with many phone numbers, also databases use indexing to store information of a specific column so that queries become faster. In a phone book, we use letters of alphabets e.g. Alice's number will be stored in section A. Thus, everytime we want to find Alice's number we don't have to parse all of the numbers one by one, but rather go to the appropriate section. 

I saw many examples explaining how indexes work in a database and one example that captured my attention was a deck of cards. 

![Shuffled Deck](https://miro.medium.com/max/599/1*vyRa5-ANrKQO1kS07p7Kpg.jpeg)

Supposing that we have a shuffled deck of cards, how can we find a specific card (e.g. Jack of Diamonds)? How could an index be built? By number or by suit? Databases offer the option of using both and this is what I do in this code. I build a incredibly large deck inside a table of a database in the localhost, shuffle it and then use indexing to see how much is the whole process accelerated.

## Running the script 

The first step is to have a database run in a port of the localhost. By modifying accordingly the db dictionary in file `indexing.py` one can make a connection with an existing database of the system. 

If no database exists, then the fastest way of deploying a database on the localhost is docker: 

```
docker pull postgres
docker run --rm -p 1283:5432 postgres:latest
```

Then we run the python file indexing.py using the command 

```
python3 indexing.py
```

## indexing.py

- Connects with the postgres database in the localhost and creates a table with the name cards. 
- The table consists of two columns: the number abd suit. 
- Then a pandas dataframe is created containing a deck of cards. However to scale the things up we add for each suit (Clubs, Spades, Hearts, Diamonds) all the numbers from 1 to 50 000. 
- Using pandas we shuffle the deck and insert the data in the cards table. 
- We index both columns and we measure the time needed to run a query before and after indexing.

After repeating this experiment a few times, I found out that indexing is 7, 8, or even 9 times faster.


## References
https://stackoverflow.com/questions/107132/what-columns-generally-make-good-indexes
https://stackoverflow.com/questions/1108/how-does-database-indexing-work
