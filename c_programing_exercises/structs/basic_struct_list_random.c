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
 *       Based on:
 *       https://www.geeksforgeeks.org/sorting-algorithms/#Basic
 *       https://www.geeksforgeeks.org/insertion-sort-for-singly-linked-list/
 *
 * =====================================================================================
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

struct LinkedList {
    int data;
    struct LinkedList *next;
};

typedef struct LinkedList *node; //Define node as pointer of data type struct LinkedList

/* function to insert a new_node in a list. Note that this
  function expects a pointer to head_ref as this can modify the
  head of the input linked list (similar to push())*/
void sortedInsert(struct LinkedList** head_ref, struct LinkedList* new_node)
{
    struct LinkedList* current;
    /* Special case for the head end */
    if (*head_ref == NULL || (*head_ref)->data >= new_node->data)
    {
        new_node->next = *head_ref;
        *head_ref = new_node;
    }
    else
    {
        /* Locate the node before the point of insertion */
        current = *head_ref;
        while (current->next!=NULL &&
               current->next->data < new_node->data)
        {
            current = current->next;
        }
        new_node->next = current->next;
        current->next = new_node;
    }
}
// function to sort a singly linked list using insertion sort
void insertionSort(struct LinkedList **head_ref)
{
    // Initialize sorted linked list
    struct LinkedList *sorted = NULL;
 
    // Traverse the given linked list and insert every
    // node to sorted
    struct LinkedList *current = *head_ref;
    while (current != NULL)
    {
        // Store next for next iteration
        struct LinkedList *next = current->next;
 
        // insert current in sorted linked list
        sortedInsert(&sorted, current);
 
        // Update current
        current = next;
    }
 
    // Update head_ref to point to sorted linked list
    *head_ref = sorted;
}


void print_list(node p){
    while(p != NULL){
        printf ( "%d\n",p->data );
        p = p->next;
    }
    printf("\n");
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

    srand(time(NULL));
    node head=0;
    int r;

    for (int i = 0 ; i < 10 ; i ++){
        // rand from 1 -> 10 
        r = rand() % 10 + 1;
        head = addNode(head,r);
    }
   
   printf("Random: \n");
   print_list(head);

   printf("Sorted: \n");
   insertionSort(&head);
   print_list(head);

    return 0;
}
