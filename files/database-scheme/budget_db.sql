CREATE TYPE "transaction_type" AS ENUM (
  'income',
  'outcome',
  'transfer'
);

CREATE TYPE "category_type" AS ENUM (
  'income',
  'outcome'
);

CREATE TABLE "family" (
  "id" integer PRIMARY KEY,
  "access_code" integer
);

CREATE TABLE "user" (
  "id" integer PRIMARY KEY,
  "family_id" integer,
  "email" string,
  "username" string UNIQUE,
  "password" string
);

CREATE TABLE "budget" (
  "id" integer PRIMARY KEY,
  "name" string,
  "planned_outcomes" float
);

CREATE TABLE "category" (
  "id" integer PRIMARY KEY,
  "base_category_id" integer,
  "budget_id" integer,
  "type" category_type,
  "name" string
);

CREATE TABLE "transaction" (
  "id" integer PRIMARY KEY,
  "user_id" integer,
  "account_id" integer,
  "category_id" integer,
  "type" transaction_type,
  "due_date" date,
  "due_time" time,
  "amount" float,
  "note" string DEFAULT ''
);

CREATE TABLE "account" (
  "id" integer PRIMARY KEY,
  "name" string,
  "currency" string,
  "opening_balance" float DEFAULT 0
);

ALTER TABLE "user" ADD FOREIGN KEY ("family_id") REFERENCES "family" ("id");

ALTER TABLE "category" ADD FOREIGN KEY ("base_category_id") REFERENCES "category" ("id");

ALTER TABLE "category" ADD FOREIGN KEY ("budget_id") REFERENCES "budget" ("id");

ALTER TABLE "transaction" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "transaction" ADD FOREIGN KEY ("account_id") REFERENCES "account" ("id");

ALTER TABLE "transaction" ADD FOREIGN KEY ("category_id") REFERENCES "category" ("id");
