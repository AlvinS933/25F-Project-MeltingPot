DROP DATABASE IF EXISTS `MeltingPot`;
CREATE DATABASE `MeltingPot`;
USE `MeltingPot`;


   DROP TABLE IF EXISTS Administrators;
   CREATE TABLE Administrators(
       username VARCHAR (50) NOT NULL UNIQUE,
       password VARCHAR (50) NOT NULL,
       adminID INT PRIMARY KEY
   );


   DROP TABLE IF EXISTS Categories;
   CREATE TABLE Categories(
       name VARCHAR (50) NOT NULL UNIQUE,
       description TEXT,
       catID INT PRIMARY KEY
   );


   DROP TABLE IF EXISTS Ingredients;
   CREATE TABLE Ingredients(
       name VARCHAR (50) NOT NULL UNIQUE,
       description TEXT,
       ingrID INT PRIMARY KEY
   );


   DROP TABLE IF EXISTS Tags;
   CREATE TABLE Tags(
       name VARCHAR (50) NOT NULL UNIQUE,
       description TEXT,
       tagID INT PRIMARY KEY
   );


   DROP TABLE IF EXISTS DataAnalysts;
   CREATE TABLE DataAnalysts(
       username  VARCHAR(50) NOT NULL UNIQUE,
       password  VARCHAR(50) NOT NULL,
       analystID INT PRIMARY KEY
   );


   DROP TABLE IF EXISTS Users;
   CREATE TABLE Users(
       username VARCHAR (50) NOT NULL UNIQUE,
       password VARCHAR (50) NOT NULL,
       bio TEXT,
       verified TINYINT(1) NOT NULL DEFAULT 0,
       userID INT PRIMARY KEY
   );


   DROP TABLE IF EXISTS Recipes;
   CREATE TABLE Recipes(
       userID INT NOT NULL,
       catID INT NOT NULL,
       name VARCHAR(50) NOT NULL,
       description TEXT,
       steps TEXT,
       picture MEDIUMTEXT,
       difficulty INT NOT NULL,
       recipeID INT PRIMARY KEY,
       FOREIGN KEY (userID) references Users(userId),
       FOREIGN KEY (catID) references Categories(catID)
   );


   DROP TABLE IF EXISTS RecipeReports;
   CREATE TABLE RecipeReports(
       adminID INT NOT NULL,
       recipeID INT NOT NULL,
       reason VARCHAR (50),
       PRIMARY KEY (adminID, recipeID),
       FOREIGN KEY (adminID) references Administrators(adminID),
       FOREIGN KEY (recipeID) references Recipes(recipeID)
   );


   DROP TABLE IF EXISTS UserReports;
   CREATE TABLE UserReports(
       adminID INT NOT NULL,
       userID INT NOT NULL,
       reason VARCHAR (50),
       PRIMARY KEY (adminID, userID),
       FOREIGN KEY (adminID) references Administrators(adminID),
       FOREIGN KEY (userID) references Users(userID)
   );


   DROP TABLE IF EXISTS Ratings;
   CREATE TABLE Ratings(
       recipeID INT NOT NULL,
       userID INT NOT NULL,
       rating INT NOT NULL,
       PRIMARY KEY (recipeID, userID),
       FOREIGN KEY (recipeID) references Recipes(recipeID),
       FOREIGN KEY (userID) references Users(userID)
   );


   DROP TABLE IF EXISTS Collections;
   CREATE TABLE Collections(
       userID INT NOT NULL,
       title VARCHAR (50) NOT NULL,
       description TEXT,
       collectID INT PRIMARY KEY,
       FOREIGN KEY (userID) references Users(userID)
   );


   DROP TABLE IF EXISTS CollectionTags;
   CREATE TABLE CollectionTags(
       collectID INT NOT NULL,
       tagID INT NOT NULL,
       PRIMARY KEY (collectID, tagID),
       FOREIGN KEY (collectID) references Collections(collectID),
       FOREIGN KEY (tagID) references Tags(tagID)
   );


   DROP TABLE IF EXISTS Reviews;
   CREATE TABLE Reviews(
       recipeID INT NOT NULL,
       userID INT NOT NULL,
       review TEXT,
       PRIMARY KEY (recipeID, userID),
       FOREIGN KEY (recipeID) references Recipes(recipeID),
       FOREIGN KEY (userID) references Users(userID)
   );


   DROP TABLE IF EXISTS CollectionRecipes;
   CREATE TABLE CollectionRecipes(
       collectID INT,
       recipeID INT,
       PRIMARY KEY (collectID, recipeID),
       FOREIGN KEY (collectID) references Collections(collectID),
       FOREIGN KEY (recipeID) references Recipes(recipeID)
   );


   DROP TABLE IF EXISTS RecipeIngredients;
   CREATE TABLE RecipeIngredients(
       recipeID INT NOT NULL,
       ingrID INT NOT NULL,
       PRIMARY KEY (recipeID, ingrID),
       FOREIGN KEY (recipeID) references Recipes(recipeID),
       FOREIGN KEY (ingrID) references Ingredients(ingrID)
   );


   DROP TABLE IF EXISTS RecipeTags;
   CREATE TABLE RecipeTags(
       recipeID INT NOT NULL,
       tagID INT NOT NULL,
       PRIMARY KEY (recipeID, tagID),
       FOREIGN KEY (recipeID) references Recipes(recipeID),
       FOREIGN KEY (tagID) references Tags(tagID)
   );




INSERT INTO Administrators(username, password, adminID)
   VALUES('Robert', 'Bobby23', 1),
         ('Pauly', 'Jersey32', 2),
         ('Carly', 'shows43', 3);


INSERT INTO Categories(name, description, catID)
   VALUES('Breakfast', 'Meals to wake up', 1),
         ('Lunch', 'Food for noon', 2),
         ('Dinner', 'End of the day feast', 3);


INSERT INTO Ingredients(name, description, ingrID)
   VALUES('Onions', 'Fresh, Whole Onions', 1),
         ('Potatoes', 'Organic Gold Potatoes', 2),
         ('Tomatoes', 'Organic Farm Baby Tomatoes', 3);


INSERT INTO Tags(name, description, tagID)
   VALUES('Gluten Free', '0 Gluten Ingredients', 1),
         ('Vegan', 'No Animal Products', 2),
         ('Vegetarian', 'No Meat', 3);


INSERT INTO DataAnalysts(username, password, analystID)
   VALUES('Jim Halpert', 'Scranton', 1),
         ('The Lorax', 'Trees', 2),
         ('Jim Hooper', 'Sheriff', 3);


INSERT INTO Users(username, password, bio, userID)
   VALUES('Pamela Halpert', 'Reception', 'Italian desserts', 1),
         ('John Brown', 'Jimmy87', 'Chicago Deep Dish', 2),
         ('Bobby Altman', 'Scammer', 'MexiCali Fusion', 3);


INSERT INTO Recipes(userID, catID, name, description, steps, picture, difficulty, recipeID)
   VALUES (1, 1, 'Bacon Egg and Cheese', 'Yummy breakfast with bacon egg and cheese sandwich', 'Put Bacon Egg and Cheese on Bread', NULL, 3., 1),
          (2, 2, 'Chicken Noodle Soup', 'Classic chicken noodle soup', 'Put Chicken and Noodles in Broth', NULL, 2, 2),
          (3, 3, 'Pizza', 'Homemade healthy pizza', 'Put Tomato Sauce and Cheese on Dough and Bake it', NULL, 4, 3);


INSERT INTO RecipeReports(adminID, recipeID, reason)
   VALUES (1, 1, 'Calories are incorrect.'),
          (2, 2, 'Copied Recipe'),
          (3, 3, 'Fake Recipe/Inappropriate');


INSERT INTO UserReports(adminID, userID, reason)
   VALUES (1, 1, 'Spamming Comments'),
          (2, 2, 'Spam Reporting'),
          (3, 3, 'Creating bot accounts');


INSERT INTO Ratings(recipeID, userID, rating)
   VALUES (1, 1, 4),
          (2, 2, 3),
          (3,3, 2);


INSERT INTO Collections(userID, title, description, collectID)
   VALUES (1, 'Quick Bites', 'Easy fast and simple recipes', 1),
          (2, 'Free Time', 'Meals that require a lot of time', 2),
          (3, 'Family Fun', 'Recipes for a family to cook', 3);


INSERT INTO CollectionTags(collectID, tagID)
   VALUES (1, 1),
          (2, 2),
          (3, 3);


INSERT INTO Reviews(recipeID, userID, review)
   VALUES (1, 1, 'Yummy!'),
          (2, 2, 'Better than expected.'),
          (3, 3, 'Not my favorite');


INSERT INTO CollectionRecipes(collectID, recipeID)
   VALUES (1, 1),
          (2, 2),
          (3, 3);


INSERT INTO RecipeIngredients(recipeID, ingrID)
   VALUES (1, 1),
          (2, 2),
          (3, 3);


INSERT INTO RecipeTags(recipeID, tagID)
   VALUES (1, 1),
          (2, 2),
          (3, 3);

INSERT INTO users (userID, username) VALUES
    (1, 'Pamela Halpert'),
    (2, 'John Brown'),
    (3, 'Bobby Altman');

INSERT INTO admins (adminID, username) VALUES
    (1, 'Robert'),
    (2, 'Pauly'),
    (3, 'Carly');

INSERT INTO analysts (analystID, username) VALUES
    (1, 'Jim Halpert'),
    (2, 'The Lorax'),
    (3, 'Jim Hooper');
