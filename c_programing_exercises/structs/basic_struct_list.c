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
//#include <malloc.h>
#include <stdlib.h>

struct LinkedList {
    int data;
    struct LinkedList *next;
};

typedef struct LinkedList *node; //Define node as pointer of data type struct LinkedList


void print_list(node p){
    while(p != NULL){
        printf ( "%d\n",p->data );
        p = p->next;
    }
}

node createNode(){
    node temp; // declare a node
    temp = (node)malloc(sizeof(struct LinkedList)); // allocate memory using malloc()
    temp->next = NULL;// make next point to NULL
    return temp;//return the new node
}


node addNode(node head, int value){
    node temp,p;// declare two nodes temp and p
    temp = createNode();//createNode will return a new node with data = value and next pointing to NULL.
    temp->data = value; // add element's value to data part of node
    if(head == NULL){
        head = temp;     //when linked list is empty
    }
    else{
        p  = head;//assign head to p
        while(p->next != NULL){
            p = p->next;//traverse the list until p is the last node.The last node always points to NULL.
        }
        p->next = temp;//Point the previous last node to the new node created.
    }
    return head;
}

int main ( int argc, char *argv[] ){

    node head=0;
    for (int i = 0 ; i < 10 ; i ++){
        head = addNode(head,i);
    }
    
   print_list(head);

    return 0;
}
