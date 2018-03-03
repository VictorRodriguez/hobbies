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

    struct Phonebook phonebook;

    strcpy(phonebook.name,"Juan Perez");
    phonebook.phone = 12345678;

    print_phonebook(phonebook);
    return 0;
}
