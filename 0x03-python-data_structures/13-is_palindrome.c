#include <stdio.h>
#include <stdlib.h>

/* Definition for singly-linked list */
typedef struct ListNode {
    int val;
    struct ListNode *next;
} listint_t;

/* Function to reverse a linked list */
listint_t* reverseList(listint_t *head) {
    listint_t *prev = NULL;
    listint_t *curr = head;
    listint_t *next = NULL;
    
    while (curr != NULL) {
        next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    
    return prev;
}

/* Function to check if a linked list is a palindrome */
int is_palindrome(listint_t **head) {
    if (*head == NULL || (*head)->next == NULL) {
        return 1; // An empty list or a single node list is considered a palindrome
    }

    listint_t *slow = *head;
    listint_t *fast = *head;
    listint_t *prev_slow = *head;
    listint_t *second_half = NULL;
    int is_pal = 1;

    while (fast != NULL && fast->next != NULL) {
        fast = fast->next->next;
        prev_slow = slow;
        slow = slow->next;
    }

    if (fast != NULL) { // Odd number of nodes, move slow pointer one step further
        slow = slow->next;
    }

    second_half = reverseList(slow);
    prev_slow->next = NULL; // Break the original list into two parts

    listint_t *p1 = *head;
    listint_t *p2 = second_half;

    while (p1 != NULL && p2 != NULL) {
        if (p1->val != p2->val) {
            is_pal = 0;
            break;
        }
        p1 = p1->next;
        p2 = p2->next;
    }

    // Reconstruct the original list
    prev_slow->next = reverseList(second_half);

    return is_pal;
}
