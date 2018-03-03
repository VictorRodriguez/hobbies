/*
 * =====================================================================================
 *
 *       Filename:  main.c
 *
 *    Description:  Basic struct example
 *
 *        Version:  1.0
 *        Created:  03/03/2018 11:15:21 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Victor Rodriguez (), vm.rod25@gmail.com
 *   Organization:  
 *
 * =====================================================================================
 */
#include <stdio.h>
#include <string.h>

struct Phonebook{
    char name[50];
    int phone;
    int phonebook_id;

};

void print_phonebook(struct Phonebook book){

    printf ("name : %s\n", book.name);
    printf ("phone : %d\n", book.phone);

}

int main ( int argc, char *argv[] ){

    struct Phonebook phonebook[10];

    for ( int i = 0 ; i < 10 ; i ++){
        strcpy(phonebook[i].name,"Juan Perez");
        phonebook[i].phone = (i+1)*10000000+(i+1);
    }


    for ( int i = 0 ; i < 10 ; i ++){
        print_phonebook(phonebook[i]);
    }
    return 0;
}
