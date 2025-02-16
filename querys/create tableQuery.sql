CREATE TABLE Apps (
    AppId TEXT PRIMARY KEY,
    AppName TEXT NOT NULL,
    CategoryId INT NOT NULL,
    Rating FLOAT DEFAULT 0,
    RatingCount INT DEFAULT 0,
    Installs BIGINT,
    MinInstalls BIGINT,
    MaxInstalls BIGINT,
    Free BOOLEAN,
    Price FLOAT DEFAULT 0,
    Currency TEXT,
    Size TEXT,
    MinAndroid TEXT,
    DeveloperId INT NOT NULL,
    Released DATE,
    LastUpdated DATE,
    ContentRating TEXT,
    PrivacyPolicy TEXT,
    AdSupported BOOLEAN,
    InAppPurchases BOOLEAN,
    EditorsChoice BOOLEAN
);

CREATE TABLE Categories (
    CategoryId SERIAL PRIMARY KEY,
    CategoryName TEXT UNIQUE NOT NULL
);

CREATE TABLE Developers (
    DeveloperId SERIAL PRIMARY KEY,
    DeveloperName TEXT UNIQUE NOT NULL,
    DeveloperWebsite TEXT,
    DeveloperEmail TEXT
);