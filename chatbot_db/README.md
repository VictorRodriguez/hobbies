# Chatbot with SQLite Database Integration

This project demonstrates a simple chatbot implemented using Lex (Flex) and Yacc (Bison) with a SQLite database connector. The chatbot can recognize greetings, farewells, and time queries, as well as query user information from a database.

## Prerequisites

- `flex` (Lex implementation)
- `bison` (Yacc implementation)
- `gcc` (GNU Compiler Collection)
- `sqlite3` (SQLite database)

## Setup

### 1. Create a Sample Database

First, create a SQLite database file (`chatbot.db`) with a table `users` that contains sample user data.

```sh
sqlite3 chatbot.db <<EOF
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
);

INSERT INTO users (name, age) VALUES ('Alice', 30);
INSERT INTO users (name, age) VALUES ('Bob', 25);
INSERT INTO users (name, age) VALUES ('Charlie', 35);
EOF
```

### 2. Lex File (`chatbot.l`)

Create a file named `chatbot.l` with the following content:

```c
%{
#include "y.tab.h"
%}

%%

hello           { return HELLO; }
hi              { return HELLO; }
hey             { return HELLO; }
goodbye         { return GOODBYE; }
bye             { return GOODBYE; }
time            { return TIME; }
what[' ']is[' ']the[' ']time  { return TIME; }
what[' ']time[' ']is[' ']it  { return TIME; }
query[' ']user[' ']name[' ']([a-zA-Z]+) { yylval.str = strdup(yytext); return QUERY_USER; }
\n              { return 0; }  /* End of input on newline */

.               { return yytext[0]; }

%%

int yywrap() {
    return 1;
}
```

### 3. Yacc File (`chatbot.y`)

Create a file named `chatbot.y` with the following content:

```c
%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>
#include <time.h>

void yyerror(const char *s);
int yylex(void);

char* yylval.str;

sqlite3 *db;

void query_user_name(const char *name);
%}

%token HELLO GOODBYE TIME QUERY_USER

%%

chatbot : greeting
        | farewell
        | query
        | user_query
        ;

greeting : HELLO { printf("Chatbot: Hello! How can I help you today?\n"); }
         ;

farewell : GOODBYE { printf("Chatbot: Goodbye! Have a great day!\n"); }
         ;

query : TIME {
            time_t now = time(NULL);
            struct tm *local = localtime(&now);
            printf("Chatbot: The current time is %02d:%02d.\n", local->tm_hour, local->tm_min);
         }
       ;

user_query : QUERY_USER {
               query_user_name(yylval.str);
               free(yylval.str);
            }
          ;

%%

int main() {
    if (sqlite3_open("chatbot.db", &db)) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return 1;
    }

    printf("Chatbot: Hi! You can greet me, ask for the time, or say goodbye.\n");
    while (yyparse() == 0) {
        // Loop until end of input
    }

    sqlite3_close(db);
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Chatbot: I didn't understand that.\n");
}

void query_user_name(const char *name) {
    sqlite3_stmt *stmt;
    const char *sql = "SELECT name, age FROM users WHERE name = ?";

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        return;
    }

    if (sqlite3_bind_text(stmt, 1, name, -1, SQLITE_STATIC) != SQLITE_OK) {
        fprintf(stderr, "Failed to bind name: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        return;
    }

    int ret_code = sqlite3_step(stmt);
    if (ret_code == SQLITE_ROW) {
        const char *retrieved_name = (const char *)sqlite3_column_text(stmt, 0);
        int age = sqlite3_column_int(stmt, 1);
        printf("Chatbot: User %s is %d years old.\n", retrieved_name, age);
    } else {
        printf("Chatbot: User not found.\n");
    }

    sqlite3_finalize(stmt);
}
```

### 4. Compile and Run the Chatbot

#### Compile the Lex File

```sh
flex chatbot.l
```

#### Compile the Yacc File

```sh
bison -d chatbot.y
```

#### Compile the Generated C Files and Link with SQLite

```sh
gcc lex.yy.c chatbot.tab.c -o chatbot -lsqlite3 -lfl
```

#### Run the Chatbot

```sh
./chatbot
```

## Example Interaction

```
Chatbot: Hi! You can greet me, ask for the time, or say goodbye.
User: hello
Chatbot: Hello! How can I help you today?
User: query user name Alice
Chatbot: User Alice is 30 years old.
User: query user name Bob
Chatbot: User Bob is 25 years old.
User: query user name Dave
Chatbot: User not found.
User: bye
Chatbot: Goodbye! Have a great day!
```

This project demonstrates how to integrate a SQLite database with a Lex/Yacc-based chatbot to handle basic conversational interactions and database queries.

