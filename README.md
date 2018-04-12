** Application Description **

I am creating an application called Movie Mood. Movie Mood allows users to register and sign in, and enter movie titles that they can then save to their account. Any user can see all the possible movie titles and director names they (and other users) have saved. Movies and Directors will have a many-to-many relationships - since there can be multiple directors for a movie, and directors can direct multiple movies. Movie Mood will also allow logged-in users to enter and save their favorite celebrity movie stars. Users can see all the favorite celebrity names they have saved but can't see other users' favorite celebrity names. Also logged-in users are able to search for a movie and receive the movie title along with the movie overview - by using data from TheMovieDB's API to gather data about the searched movie. I also used AJAX to send a request to TheMovieDB to get a movie's rating. I then displayed the rating when a user searched for a movie. 


** What a user can do **

A user has the option of signing up for an account or not. If the user chooses not to sign up for an account, they can see all the movies and directors that other users have added. However, that is all they can do. If a user chooses to make an account, they can do all of the above - plus more. Logged in users can enter and save movies they have seen (movie title, movie rating, directors of the movie, and the year the movie was filmed in). The logged-in users can also enter/save their favorite celebrity names. They can only see the celebrity names they have entered (users don't have access to seeing other users' favorite celebrity names). Logged in users can also search for a movie - which will use TheMovieDB API - to view the searched movie's overview and rating.



** Heroku Link **

https://moviemood-imunir.herokuapp.com/



** Modules **

No additional modules to install



** Routes **

/404 -> 404.html
/500 -> 500.html
/login -> login.html
/logout -> logs user out of account and redirects to index page
/register -> register.html
/ -> index.html
/all_movies -> all_movies.html
/delete/<movielst> -> deletes a Movie and redirects to index page
/movie/<info> -> single_movie.html
/update/<item> -> update.html
/all_directors -> all_directors.html
/see_favorite -> favorite.html
/search_movie -> search_movie.html



** Requirements **

    ** Ensure that your SI364final.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up). Your main file must be called SI364final.py, but of course you may include other files if you need. ** 

    ** A user should be able to load http://localhost:5000 and see the first page they ought to see on the application. **

    ** Include navigation in base.html with links (using a href tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, like this ) **

    ** Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block. **

    ** Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4). **

    **Must have data associated with a user and at least 2 routes besides logout that can only be seen by logged-in users.**

    **At least 3 model classes besides the User class.**

    **At least one one:many relationship that works properly built between 2 models.**

    **At least one many:many relationship that works properly built between 2 models.**

    **Successfully save data to each table.**

    **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).**

    **At least one query of data using an .all() method and send the results of that query to a template.**

    **At least one query of data using a .filter_by(... and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).**

    **At least one helper function that is not a get_or_create function should be defined and invoked in the application.**

    **At least two get_or_create functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).**

    **At least one error handler for a 404 error and a corresponding template.**

    **At least one error handler for any other error (pick one -- 500? 403?) and a corresponding template.**

    **Include at least 4 template .html files in addition to the error handling template files.
        At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.**

    **At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that does accord with other involved sites' Terms of Service, etc).
        Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source to the database (in some way).**

    At least one WTForm that sends data with a GET request to a new page.

    **At least one WTForm that sends data with a POST request to the same page. (NOT counting the login or registration forms provided for you in class.)**

    **At least one WTForm that sends data with a POST request to a new page. (NOT counting the login or registration forms provided for you in class.)**

    **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.**

    **Include at least one way to update items saved in the database in the application (like in HW5).**

    **Include at least one way to delete items saved in the database in the application (also like in HW5).**

    **Include at least one use of redirect.**

    **Include at least two uses of url_for. (HINT: Likely you'll need to use this several times, really.)**

    **Have at least 5 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and navigation as instructed above.)**

    (Addtionals - I completed 3)
    **(100 points) Include a use of an AJAX request in your application that accesses and displays useful (for use of your application) data.**

    **(100 points) Create, run, and commit at least one migration.**

    (100 points) Include file upload in your application and save/use the results of the file. (We did not explicitly learn this in class, but there is information available about it both online and in the Grinberg book.)

    **(100 points) Deploy the application to the internet (Heroku) — only counts if it is up when we grade / you can show proof it is up at a URL and tell us what the URL is in the README(Heroku deployment as we taught you is 100% free so this will not cost anything.)**

    (100 points) Implement user sign-in with OAuth (from any other service), and include that you need a specific-service account in the README, in the same section as the list of modules that must be installed.
