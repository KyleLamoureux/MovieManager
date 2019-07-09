# Movie Manager

Will return to improve this soon. Generalize it, create a web interface to display queries, mess around with docker, scrape actual movie details off wikipedia/IMDb.

Script will scan the label 'Movies' in your gmail box once a day at 6pm which it does by just calling the script with a crontab:
`0 18 * * * cd path/to/movie_tracker && /usr/bin/python3 run.py > /tmp/movie_manager.log 2>&1`
It will convert all the new movies with that label to JSON so I can easily parse it to add it to the sheets. It will then delete all trace of running removing emails etc. And send you an email letting know that it has been ran. 

must have setup a config file which contains your gmail password and username. password being a code generated on your google account to give 'devices access'. Need a client secret from google right now to have access to your sheets.

- Not really in a shareable state ATM but works great for me cool project to practice my python and do somethings I was interested in experimenting with
