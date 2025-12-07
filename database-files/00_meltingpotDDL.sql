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
       FOREIGN KEY (userID) references Users(userID),
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