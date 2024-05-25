# SQL technique: multiple joins and the *distinct* keyword

It is important to realize that if you have a properly designed and linked database, you can retrieve information from as many tables as you want, specify retrieval conditions based on any data in the tables, and show the results in any order that you like.

*Example:* We’ll use the order entry model. We’d like a list of all the products that have been purchased by a specific customer.

Unless you can memorize the exact spelling of every attribute in the database, along with all the PKs and FKs (I can’t), you should keep a copy of the relation scheme diagram handy when you build the query. We’ll show it again here, circling the attributes that we need for this query.

!https://web.csulb.edu/colleges/coe/cecs/dbdesign/img/multijoin-salesscheme.gif

*Other views of this diagram:* [Large image](https://web.csulb.edu/colleges/coe/cecs/dbdesign/img/multijoin-salesscheme-img.html) - [Description (text)](https://web.csulb.edu/colleges/coe/cecs/dbdesign/img/multijoin-salesscheme-dd.html)

Our query is still a simple one that could be expressed in RA using only the select, project, and join operators.

πcLastName, cFirstName, prodName σcFirstName='Alvaro' ∧ cLastName='Monge' (*customers* ⨝ *orders* ⨝ *orderlines* ⨝ *products*)

Notice the typical conjunction connector in the selection operation.

The information that we need is found in the Products table. You could think of this as “output” from the query that will be part of the SELECT clause attribute list. The retrieval condition, or “input” to the query, is based on the Customers table—these attributes will be needed for the WHERE clause..

We can’t join Customers to Products, because they don’t have any common attributes. However, we can traverse a path using the relationships. From Customers, we can use the relation with Order to find orders placed. Next, use the relationship to OrderLines to find the details of the order. Finally, from OrderLines, we use the relationship to Products to get the information about the products included. Each time we follow a relationship, we will perform a join operation on the primary key and foreign key to link related rows together. This allows us to correctly associate the Customers data with the data about the Products the customers have placed.

Another way to think about this is to simply “follow the PK-FK pairs” from table to table until you have completely linked all of the information you need. If you look carefully at the relation scheme for this query, you will realize that we could have bypassed the Orders table (since the custID is also part of the OrderLines scheme). If there were an orderID, or if we needed data from the Orders table, it would have to be included, so we’ll keep it here for illustration. In SQL, we’ll build the query using the same step-by-step procedure that you have seen before.

Look at the result set (all of the linked data). We won’t show the result here because of space limitations on the web page.

```sql
        SELECT *
        FROM customers
          NATURAL JOIN orders
          NATURAL JOIN orderlines
          NATURAL JOIN products;
```

As explained in another article, your database system might not support the NATURAL JOIN syntax that we show here. We’ll discuss this issue further when we look at join types. The multiple natural joins in our example work correctly because there are no non-pk/fk attributes in any of our tables that have the same name. In larger, more complicated databases, this might not be true and there would be serious unintended consequences in using a natural join!

Next, we need to restrict the rows in the result to only one customer.

```sql
        SELECT *
        FROM customers
          NATURAL JOIN orders
          NATURAL JOIN orderlines
          NATURAL JOIN products
        WHERE cFirstName = 'Alvaro' AND cLastName = 'Monge';
```

Finally, let's pick the columns we want. Notice that we are including the retrieval condition attributes in the SELECT clause, to be sure that this really is the right answer (there's no reason it wouldn't be, this is just for us).

```sql
        SELECT cFirstName, cLastName, prodName
        FROM customers
          NATURAL JOIN orders
          NATURAL JOIN orderlines
          NATURAL JOIN products
        WHERE cFirstName = 'Alvaro' AND cLastName = 'Monge';
```

|  |  |  |
| --- | --- | --- |
| Alvaro | Monge | Hammer, framing, 20 oz. |
| Alvaro | Monge | Hammer, framing, 20 oz. |
| Alvaro | Monge | Screwdriver, Phillips #2, 6 inch |
| Alvaro | Monge | Screwdriver, Phillips #2, 6 inch |
| Alvaro | Monge | Pliers, needle-nose, 4 inch |

## The *distinct* keyword

Oops! We only wanted a list of the individual product names that this customer has purchased, but some of them are listed more than once. What went wrong?

If the RA version of our query could have actually been executed, each row of the result table above would be distinct—remember that a relation is a *set* of tuples, and sets can’t have duplicates—and there would of course be fewer rows than you see here.

SQL doesn’t work the same way. The reason for the duplicates is that the SELECT clause simply eliminated the unwanted columns from the result set; it left all of the rows that were picked by the WHERE clause.

The real problem in SQL is that the SELECT attribute list is not a super key for the result set. Look again very carefully at the relation scheme to understand why this is true. Any time that this happens, we can eliminate the duplicate rows by including the **DISTINCT** keyword in the SELECT clause. While making this revision, we’ll also list the product names in alphabetical order.

```sql
        SELECT DISTINCT cFirstName, cLastName, prodName
        FROM customers
          NATURAL JOIN orders
          NATURAL JOIN orderlines
          NATURAL JOIN products
        WHERE cFirstName = 'Alvaro' AND cLastName = 'Monge'
        ORDER BY prodName;
```

|  |  |  |
| --- | --- | --- |
| Alvaro | Monge | Hammer, framing, 20 oz. |
| Alvaro | Monge | Pliers, needle-nose, 4 inch |
| Alvaro | Monge | Screwdriver, Phillips #2, 6 inch |

A sloppy way to be sure that you never have duplicate rows would be to always use the DISTINCT keyword. Please don’t do this—it just keeps you from understanding what is really going on in the query. If the SELECT attribute list *does* form a super key of the FROM clause (result set), the DISTINCT keyword is not needed, and should not be used. Also, requesting duplicates to be removed is a costly operation! How would you remove duplicates? The task is more difficult than you might imagine since there might be so much data that it cannot be stored in RAM and thus all resides on disk. How do you remove duplicates in that case?

# SQL technique: join types

## Inner join

All of the joins that you have seen so far have used the **natural join** syntax—for example, to produce a list of customers and dates on which they placed orders. Remember that if this syntax is available, it will automatically pick the join attributes as those with the same name in both tables (intersection of the schemes). It will also produce only one copy of those attributes in the result table.

```sql
        SELECT cFirstName, cLastName, orderDate
        FROM customers NATURAL JOIN orders;
```

- The join does not consider the pk and fk attributes you have specified. If there are any non-pk/fk attributes that have the same names in the tables to be joined, they will also be included in the intersection of the schemes, and used as join attributes in the natural join. The results will certainly not be correct! This problem might be especially difficult to detect in cases where many natural joins are performed in the same query. Fortunately, you can always specify the join attributes yourself, as we describe next.
- Another keyword that produces the same results (without the potential attribute name problem) is the **inner join**. With this syntax, you may specify the join attributes in a USING clause. (Multiple join attributes in the USING clause are separated by commas.) This also produces only one copy of the join attributes in the result table. Like the NATURAL JOIN syntax, the USING clause is not supported by all systems.
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM customers INNER JOIN orders
              USING (custID);
    ```
    
- The most widely-used (and most portable) syntax for the inner join substitutes an ON clause for the USING clause. This requires you to explicitly specify not only the join attribute names, but the join condition (normally equality). It also requires you to preface (qualify) the join attribute names with their table name, since both columns will be included in the result table. This is the only syntax that will let you use join attributes that have different names in the tables to be joined. Unfortunately, it also allows you to join tables on attributes other than the pk/fk pairs, which was a pre-1992 way to answer queries that can be written in better ways today.
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM customers INNER JOIN orders
              ON customers.custID = orders.custID;
    ```
    
- You can save a bit of typing by specifying an **alias** for each table name (such as c and o in this example), then using the alias instead of the full name when you refer to the attributes. This is the only syntax that will let you join a table to itself, as we will see when we discuss recursive relationships.
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM customers c INNER JOIN orders o
              ON c.custID = o.custID;
    ```
    
- All of the join statements above are specified as part of the 1992 SQL standard, which was not widely supported for several years after that. In earlier systems, joins were done with the 1986 standard SQL syntax. Although you shouldn’t use this unless you absolutely have to, you just might get stuck working on an older database. If so, you should recognize that the join condition is placed confusingly in the WHERE clause, along with all of the tests to pick the right rows:
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM customers c, orders o
            WHERE c.custID = o.custID;
    ```
    
    ## Outer join
    
    One important effect of all natural and inner joins is that any unmatched PK value simply drops out of the result. In our example, this means that any customer who didn’t place an order isn’t shown. Suppose that we want a list of *all* customers, along with order date(s) for those who did place orders. To include the customers who did *not* place orders, we will use an **outer join**, which may take either the USING or the ON clause syntax.
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM customers c LEFT OUTER JOIN orders o
              ON c.custID = o.custID;
    ```
    
    |  |  |  |
    | --- | --- | --- |
    | Tom | Jewett |  |
    | Alvaro | Monge | 2003-07-20 |
    | Alvaro | Monge | 2003-07-18 |
    | Alvaro | Monge | 2003-07-14 |
    | Wayne | Dick | 2003-07-14 |
- Notice that for customers who placed no orders, any attributes from the Orders table are simply filled with NULL values.
- The word “left” refers to the order of the tables in the FROM clause (customers on the left, orders on the right). The left table here is the one that might have unmatched join attributes—the one from which we want *all* rows. We could have gotten exactly the same results if the table names and outer join direction were reversed:
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM orders o RIGHT OUTER JOIN customers c
              ON o.custID = c.custID;
    ```
    
- An outer join makes sense only if one side of the relationship has a minimum cardinality of zero (as Orders does in this example). Otherwise, the outer join will produce exactly the same result as an inner join (for example, between Orders and OrderLines).
- The SQL standard also allows a FULL outer join, in which unmatched join attributes from either side are paired with null values on the other side. You will probably not have to use this with most well-designed databases.
    
    ## Evaluation order
    
    Multiple joins in a query are evaluated left-to-right in the order that you write them, unless you use parentheses to force a different evaluation order. (Some database systems require parentheses in any case.) The schemes of the joins are also cumulative in the order that they are evaluated; in RA, this means that
    
    *r1* ⨝ *r2* ⨝ *r3* = (*r1* ⨝ *r2*) ⨝ *r3*.
    
- It is especially important to remember this rule when outer joins are mixed with other joins in a query. For example, if you write:
    
    ```sql
            SELECT cFirstName, cLastName, orderDate, UPC, quantity
            FROM customers LEFT OUTER JOIN orders
              USING (custID)
              NATURAL JOIN orderlines;
    ```
    
    you will lose the customers who haven’t placed orders. They will be retained if you force the second join to be executed first:
    
    ```sql
            SELECT cFirstName, cLastName, orderDate, UPC, quantity
            FROM customers LEFT OUTER JOIN
              (orders NATURAL JOIN orderlines)
              USING (custID);
    ```
    
    ## Other join types
    
    For sake of completeness, you should also know that if you try to join two tables with no join condition, the result will be that every row from one side is paired with every row from the other side. Mathematically, this is a Cartesian product of the two tables, as you have seen before. It is almost never what you want. In pre-1992 syntax, it is easy to do this accidently, by forgetting to put the join condition in the WHERE clause:
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM customers, orders;
    ```
    
- If your system is backward-compatible (most are), you might actually try this just to prove to yourself that the result is pure nonsense. However, if you ever have an occasion to really need a Cartesian product of two tables, use the new **cross join** syntax to prove that you really mean it. Notice that this example still produces nonsense.
    
    ```sql
            SELECT cFirstName, cLastName, orderDate
            FROM customers CROSS JOIN orders;
    ```
    
- It is possible, but confusing, to specify a join condition other than equality of two attributes; this is called a **non-equi-join**. If you see such a thing in older code, it probably represents a WHERE clause or subquery in disguise.
- You may also hear the term **self join**, which is nothing but an inner or outer join between two attributes in the same table. We’ll look at these when we discuss recursive relationships.

# SQL technique: union and minus

## Set operations on tables

Some students initially think of the *join* as being a sort of union between two tables. It’s not (except for the schemes). The join pairs up data from two very different tables. In RA and SQL, union can operate only on two identical tables. Remember the Venn-diagram representation of the **union** and **minus** operations on sets. Union includes members of either or both sets (with no duplicates). Minus includes only those members of the set on the left side of the expression that are not contained in the set on the right side of the expression.

!https://web.csulb.edu/colleges/coe/cecs/dbdesign/img/setops-sets.gif

- Both sets, R and S, have to contain objects of the same type. You can’t union or minus sets of integers with sets of characters, for example. All sets, by definition, are unordered and cannot contain duplicate elements.
- SQL and RA set operations treat tables as *sets of rows*. Therefore, the tables on both sides of the union or minus operator have to have at least the same number of attributes, with corresponding attributes being of the same data type. It’s usually cleaner and more readable if you just go ahead and give them the same name using the AS keyword.
    
    ## Union
    
    For this example, we will add a Suppliers table to our sales data entry model. “A supplier is a company from which we purchase products that we will re-sell.” Each supplier suppliers zero to many products; each product is supplied by one and only one supplier. The supplier class attributes include the company name and address, plus the name and phone number of the representative from whom we make our purchases.
    
- We would like to produce a listing that shows the names and phone numbers of all people we deal with, whether they are suppliers or customers. We need rows from both tables, but they have to have the same attribute list. Looking at the relation scheme, we find corresponding first name, last name, and phone number attributes, but we still need to show what company each of the supplier representatives works for.
    
    !https://web.csulb.edu/colleges/coe/cecs/dbdesign/img/setops-union.gif
    
- We can create an extra column in the query output for the Customers table by simply giving it a name and filling it with a constant value. Here, we’ll use the value 'Customer' to distinguish these rows from supplier representatives. SQL uses the column names of the *first* part of the union query as the column names for the output, so we will give each of them aliases that are appropriate for the entire set of data.
- Build and test each component of the union query individually, then put them together. The ORDER BY clause has to come at the end.
    
    ```sql
            SELECT cLastName AS "Last Name", cFirstName AS "First Name",
              cPhone as "Phone", 'Customer' AS "Company"
            FROM customers
            UNION
            SELECT repLName, repFName, repPhone, sCompanyName
            FROM suppliers
            ORDER BY "Last Name";
    ```
    
    |  |  |  |  |
    | --- | --- | --- | --- |
    | Bradley | Jerry | 888-736-8000 | Industrial Tool Supply |
    | Dick | Wayne | 562-777-3030 | Customer |
    | Jewett | Tom | 714-555-1212 | Customer |
    | Monge | Alvaro | 562-333-4141 | Customer |
    | O'Brien | Tom | 949-567-2312 | Bosch Machine Tools |
    
    ## Minus
    
    Sometimes you have to think about both what you do want and what you don’t want in the results of a query. If there is a WHERE clause predicate that completely partitions all rows of interest (the result set) into those you want and those you don’t want, then you have a simple query with a test for inequality.
    
- The multiplicity of an association can help you determine how to build the query. Since each product has one and only one supplier, we can partition the Products table into those that are supplied by a given company and those that are not.
    
    ```sql
            SELECT prodName, sCompanyName
            FROM Products NATURAL JOIN Suppliers
            WHERE sCompanyName <> 'Industrial Tool Supply';
    ```
    
- Contrast this to finding customers who did not make purchases in 2002. Because of the optional one-to-many association between Customers and Orders, there are actually four possibilities:
    
    1. A customer made purchases in 2002 (only).
    
    2. A customer made purchases in other years, but not in 2002.
    
    3. A customer made purchases both in other years and in 2002.
    
    4. A customer made no purchases in any year.
    
- If you try to write this as a simple test for inequality,
    
    ```sql
            SELECT DISTINCT cLastName, cFirstName, cStreet, cZipCode
            FROM Customers NATURAL JOIN Orders
            WHERE TO_CHAR(orderDate, 'YYYY') <> '2002';
    ```
    
    you will correctly exclude group 1 and include group 2, but falsely include group 3 and falsely exclude group 4. Please take time to re-read this statement and convince yourself why it is true!
    
- We can show in set notation what we need to do:
    
    {*customers who did not make purchases in 2002*} = {*all customers*} − {*those who did*}
    
    There are two ways to write this in SQL.
    
- The easiest syntax in this case is to compare only the customer IDs. We’ll use the NOT IN set operator in the WHERE clause, along with a subquery to find the customer ID of those who did made purchases in 2002.
    
    ```sql
            SELECT cLastName, cFirstName, cStreet, cZipCode
            FROM Customers
            WHERE custID NOT IN
              (SELECT custID
              FROM Orders
              WHERE TO_CHAR(orderDate, 'YYYY') = '2002');
    ```
    
- We can also use the MINUS operator to subtract rows we don’t want from all rows in Customers. (Some versions of SQL use the keyword EXCEPT instead of MINUS.) Like the UNION, this requires the schemes of the two tables to match exactly in number and type of attributes.
    
    ```sql
            SELECT cLastName, cFirstName, cStreet, cZipCode
            FROM Customers
            MINUS
            SELECT cLastName, cFirstName, cStreet, cZipCode
            FROM Customers NATURAL JOIN Orders
            WHERE TO_CHAR(orderDate, 'YYYY') = '2002';
    ```
    
    ## Other set operations
    
    SQL has two additional set operators. UNION ALL works like UNION, except it keeps duplicate rows in the result. INTERSECT operates just like you would expect from set theory; again, the schemes of the two tables must match exactly.