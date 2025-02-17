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
    DeveloperId TEXT NOT NULL,
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
    DeveloperId TEXT PRIMARY KEY UNIQUE NOT NULL,
    DeveloperWebsite TEXT,
    DeveloperEmail TEXT
);

ALTER TABLE Apps 
ADD CONSTRAINT CategoryId FOREIGN KEY (CategoryId) REFERENCES Categories(CategoryId);

ALTER TABLE Apps 
ADD CONSTRAINT DeveloperId FOREIGN KEY (DeveloperId) REFERENCES Developers(DeveloperId);

CREATE INDEX idx_CategoryId ON Apps(CategoryId);
CREATE INDEX idx_FreeApps ON Apps(Free);
CREATE INDEX idx_free_social_category ON Apps(CategoryId, Free, AppId, AppName);
