# Python - Everything is object
## Objects and values

If we execute these assignment statements,

`a = "banana"
b = "banana"`

we know that a and b will refer to a string with the letters "banana". But we don’t know yet whether they point to the *same* string.

There are two possible states:

!https://www.openbookproject.net/thinkcs/python/english2e/_images/mult_references1.png

In one case, a and b refer to two different things that have the same value. In the second case, they refer to the same thing. These things have names — they are called **objects**. An object is something a variable can refer to.

We can test whether two names have the same value using ==:

**`>>>** a == b
True`

We can test whether two names refer to the same object using the *is* operator:

**`>>>** a **is** b
True`

This tells us that both a and b refer to the same object, and that it is the second of the two state diagrams that describes the relationship.

Since strings are *immutable*, Python optimizes resources by making two names that refer to the same string value refer to the same object.

This is not the case with lists:

**`>>>** a = [1, 2, 3]
**>>>** b = [1, 2, 3]
**>>>** a == b
True
**>>>** a **is** b
False`

The state diagram here looks like this:

!https://www.openbookproject.net/thinkcs/python/english2e/_images/mult_references2.png

a and b have the same value but do not refer to the same object.

## 9.11. Aliasing

Since variables refer to objects, if we assign one variable to another, both variables refer to the same object:

**`>>>** a = [1, 2, 3]
**>>>** b = a
**>>>** a **is** b
True`

In this case, the state diagram looks like this:

!https://www.openbookproject.net/thinkcs/python/english2e/_images/mult_references3.png

Because the same list has two different names, a and b, we say that it is **aliased**. Changes made with one alias affect the other:

**`>>>** b[0] = 5
**>>> print** a
[5, 2, 3]`

Although this behavior can be useful, it is sometimes unexpected or undesirable. In general, it is safer to avoid aliasing when you are working with mutable objects. Of course, for immutable objects, there’s no problem. That’s why Python is free to alias strings when it sees an opportunity to economize.

## 9.12. Cloning lists

If we want to modify a list and also keep a copy of the original, we need to be able to make a copy of the list itself, not just the reference. This process is sometimes called **cloning**, to avoid the ambiguity of the word copy.

The easiest way to clone a list is to use the slice operator:

**`>>>** a = [1, 2, 3]
**>>>** b = a[:]
**>>> print** b
[1, 2, 3]`

Taking any slice of a creates a new list. In this case the slice happens to consist of the whole list.

Now we are free to make changes to b without worrying about a:

**`>>>** b[0] = 5
**>>> print** a
[1, 2, 3]`