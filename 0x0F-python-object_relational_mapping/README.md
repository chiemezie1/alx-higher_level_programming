# **bject Relational Tutorial**

The SQLAlchemy Object Relational Mapper presents a method of associating user-defined Python classes with database tables, and instances of those classes (objects) with rows in their corresponding tables. It includes a system that transparently synchronizes all changes in state between objects and their related rows, called a [unit of work](https://docs.sqlalchemy.org/en/13/glossary.html#term-unit-of-work), as well as a system for expressing database queries in terms of the user defined classes and their defined relationships between each other.

The ORM is in contrast to the SQLAlchemy Expression Language, upon which the ORM is constructed. Whereas the SQL Expression Language, introduced in [SQL Expression Language Tutorial](https://docs.sqlalchemy.org/en/13/core/tutorial.html), presents a system of representing the primitive constructs of the relational database directly without opinion, the ORM presents a high level and abstracted pattern of usage, which itself is an example of applied usage of the Expression Language.

While there is overlap among the usage patterns of the ORM and the Expression Language, the similarities are more superficial than they may at first appear. One approaches the structure and content of data from the perspective of a user-defined [domain model](https://docs.sqlalchemy.org/en/13/glossary.html#term-domain-model) which is transparently persisted and refreshed from its underlying storage model. The other approaches it from the perspective of literal schema and SQL expression representations which are explicitly composed into messages consumed individually by the database.

A successful application may be constructed using the Object Relational Mapper exclusively. In advanced situations, an application constructed with the ORM may make occasional usage of the Expression Language directly in certain areas where specific database interactions are required.

The following tutorial is in doctest format, meaning each `>>>` line represents something you can type at a Python command prompt, and the following text represents the expected return value.

## **Version Check**

A quick check to verify that we are on at least **version 1.3** of SQLAlchemy:

**`>>> import** **sqlalchemy>>>** sqlalchemy.__version__ 
1.3.0`

## **Connecting**

For this tutorial we will use an in-memory-only SQLite database. To connect we use [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine):

**`>>> from** **sqlalchemy** **import** create_engine
**>>>** engine = create_engine('sqlite:///:memory:', echo=**True**)`

The `echo` flag is a shortcut to setting up SQLAlchemy logging, which is accomplished via Python’s standard `logging` module. With it enabled, we’ll see all the generated SQL produced. If you are working through this tutorial and want less output generated, set it to `False`. This tutorial will format the SQL behind a popup window so it doesn’t get in our way; just click the “SQL” links to see what’s being generated.

The return value of [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine) is an instance of [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine), and it represents the core interface to the database, adapted through a [dialect](https://docs.sqlalchemy.org/en/13/glossary.html#term-dialect) that handles the details of the database and [DBAPI](https://docs.sqlalchemy.org/en/13/glossary.html#term-DBAPI) in use. In this case the SQLite dialect will interpret instructions to the Python built-in `sqlite3` module.

**Lazy Connecting**
The [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine), when first returned by [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine), has not actually tried to connect to the database yet; that happens only the first time it is asked to perform a task against the database.

The first time a method like [`Engine.execute()`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine.execute) or [`Engine.connect()`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine.connect) is called, the [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) establishes a real [DBAPI](https://docs.sqlalchemy.org/en/13/glossary.html#term-DBAPI) connection to the database, which is then used to emit the SQL. When using the ORM, we typically don’t use the [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) directly once created; instead, it’s used behind the scenes by the ORM as we’ll see shortly.

**See also**

[Database Urls](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls) - includes examples of [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine) connecting to several kinds of databases with links to more information.

## **Declare a Mapping**

When using the ORM, the configurational process starts by describing the database tables we’ll be dealing with, and then by defining our own classes which will be mapped to those tables. In modern SQLAlchemy, these two tasks are usually performed together, using a system known as [Declarative](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/index.html), which allows us to create classes that include directives to describe the actual database table they will be mapped to.

Classes mapped using the Declarative system are defined in terms of a base class which maintains a catalog of classes and tables relative to that base - this is known as the **declarative base class**. Our application will usually have just one instance of this base in a commonly imported module. We create the base class using the [`declarative_base()`](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base) function, as follows:

**`>>> from** **sqlalchemy.ext.declarative** **import** declarative_base

**>>>** Base = declarative_base()`

Now that we have a “base”, we can define any number of mapped classes in terms of it. We will start with just a single table called `users`, which will store records for the end-users using our application. A new class called `User` will be the class to which we map this table. Within the class, we define details about the table to which we’ll be mapping, primarily the table name, and names and datatypes of columns:

**`>>> from** **sqlalchemy** **import** Column, Integer, String
**>>> class** **User**(Base):
**...**     __tablename__ = 'users'
**......**     id = Column(Integer, primary_key=**True**)
**...**     name = Column(String)
**...**     fullname = Column(String)
**...**     nickname = Column(String)
**......**     **def** __repr__(self):
**...**        **return** "<User(name='*%s*', fullname='*%s*', nickname='*%s*')>" % (
**...**                             self.name, self.fullname, self.nickname)`

**Tip**
The `User` class defines a `__repr__()` method, but note that is **optional**; we only implement it in this tutorial so that our examples show nicely formatted `User` objects.

A class using Declarative at a minimum needs a `__tablename__` attribute, and at least one [`Column`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column) which is part of a primary key [[1]](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#id2). SQLAlchemy never makes any assumptions by itself about the table to which a class refers, including that it has no built-in conventions for names, datatypes, or constraints. But this doesn’t mean boilerplate is required; instead, you’re encouraged to create your own automated conventions using helper functions and mixin classes, which is described in detail at [Mixin and Custom Base Classes](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html#declarative-mixins).

When our class is constructed, Declarative replaces all the [`Column`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column) objects with special Python accessors known as [descriptors](https://docs.sqlalchemy.org/en/13/glossary.html#term-descriptors); this is a process known as [instrumentation](https://docs.sqlalchemy.org/en/13/glossary.html#term-instrumentation). The “instrumented” mapped class will provide us with the means to refer to our table in a SQL context as well as to persist and load the values of columns from the database.

Outside of what the mapping process does to our class, the class remains otherwise mostly a normal Python class, to which we can define any number of ordinary attributes and methods needed by our application.

[[1](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#id1)]
For information on why a primary key is required, see [How do I map a table that has no primary key?](https://docs.sqlalchemy.org/en/13/faq/ormconfiguration.html#faq-mapper-primary-key).

## **Create a Schema**

With our `User` class constructed via the Declarative system, we have defined information about our table, known as [table metadata](https://docs.sqlalchemy.org/en/13/glossary.html#term-table-metadata). The object used by SQLAlchemy to represent this information for a specific table is called the [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) object, and here Declarative has made one for us. We can see this object by inspecting the `__table__` attribute:

**`>>>** User.__table__ 
Table('users', MetaData(bind=None),
            Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
            Column('name', String(), table=<users>),
            Column('fullname', String(), table=<users>),
            Column('nickname', String(), table=<users>), schema=None)`

**Classical Mappings**
The Declarative system, though highly recommended, is not required in order to use SQLAlchemy’s ORM. Outside of Declarative, any plain Python class can be mapped to any [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) using the [`mapper()`](https://docs.sqlalchemy.org/en/13/orm/mapping_api.html#sqlalchemy.orm.mapper) function directly; this less common usage is described at [Classical Mappings](https://docs.sqlalchemy.org/en/13/orm/mapping_styles.html#classical-mapping).

When we declared our class, Declarative used a Python metaclass in order to perform additional activities once the class declaration was complete; within this phase, it then created a [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) object according to our specifications, and associated it with the class by constructing a [`Mapper`](https://docs.sqlalchemy.org/en/13/orm/mapping_api.html#sqlalchemy.orm.Mapper) object. This object is a behind-the-scenes object we normally don’t need to deal with directly (though it can provide plenty of information about our mapping when we need it).

The [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) object is a member of a larger collection known as [`MetaData`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.MetaData). When using Declarative, this object is available using the `.metadata` attribute of our declarative base class.

The [`MetaData`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.MetaData) is a [registry](https://docs.sqlalchemy.org/en/13/glossary.html#term-registry) which includes the ability to emit a limited set of schema generation commands to the database. As our SQLite database does not actually have a `users` table present, we can use [`MetaData`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.MetaData) to issue CREATE TABLE statements to the database for all tables that don’t yet exist. Below, we call the [`MetaData.create_all()`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.MetaData.create_all) method, passing in our [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) as a source of database connectivity. We will see that special commands are first emitted to check for the presence of the `users` table, and following that the actual `CREATE TABLE` statement:

`>>> Base.metadata.create_all(engine)
SELECT ...
PRAGMA main.table_info("users")
()
PRAGMA temp.table_info("users")
()
CREATE TABLE users (
    id INTEGER NOT NULL, name VARCHAR,
    fullname VARCHAR,
    nickname VARCHAR,
    PRIMARY KEY (id)
)
()
COMMIT`

**Minimal Table Descriptions vs. Full Descriptions**
Users familiar with the syntax of CREATE TABLE may notice that the VARCHAR columns were generated without a length; on SQLite and PostgreSQL, this is a valid datatype, but on others, it’s not allowed. So if running this tutorial on one of those databases, and you wish to use SQLAlchemy to issue CREATE TABLE, a “length” may be provided to the [`String`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String) type as below:

`Column(String(50))`
The length field on [`String`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.String), as well as similar precision/scale fields available on [`Integer`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.Integer), [`Numeric`](https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.Numeric), etc. are not referenced by SQLAlchemy other than when creating tables.
Additionally, Firebird and Oracle require sequences to generate new primary key identifiers, and SQLAlchemy doesn’t generate or assume these without being instructed. For that, you use the [`Sequence`](https://docs.sqlalchemy.org/en/13/core/defaults.html#sqlalchemy.schema.Sequence) construct:

**`from** **sqlalchemy** **import** Sequence
Column(Integer, Sequence('user_id_seq'), primary_key=**True**)`
A full, foolproof [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) generated via our declarative mapping is therefore:

**`class** **User**(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=**True**)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    **def** __repr__(self):
        **return** "<User(name='*%s*', fullname='*%s*', nickname='*%s*')>" % (
                                self.name, self.fullname, self.nickname)`
We include this more verbose table definition separately to highlight the difference between a minimal construct geared primarily towards in-Python usage only, versus one that will be used to emit CREATE TABLE statements on a particular set of backends with more stringent requirements.

## **Create an Instance of the Mapped Class**

With mappings complete, let’s now create and inspect a `User` object:

**`>>>** ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
**>>>** ed_user.name
'ed'
**>>>** ed_user.nickname
'edsnickname'
**>>>** str(ed_user.id)
'None'`

**the `__init__()` method**
Our `User` class, as defined using the Declarative system, has been provided with a constructor (e.g. `__init__()` method) which automatically accepts keyword names that match the columns we’ve mapped. We are free to define any explicit `__init__()` method we prefer on our class, which will override the default method provided by Declarative.

Even though we didn’t specify it in the constructor, the `id` attribute still produces a value of `None` when we access it (as opposed to Python’s usual behavior of raising `AttributeError` for an undefined attribute). SQLAlchemy’s [instrumentation](https://docs.sqlalchemy.org/en/13/glossary.html#term-instrumentation) normally produces this default value for column-mapped attributes when first accessed. For those attributes where we’ve actually assigned a value, the instrumentation system is tracking those assignments for use within an eventual INSERT statement to be emitted to the database.

## **Creating a Session**

We’re now ready to start talking to the database. The ORM’s “handle” to the database is the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session). When we first set up the application, at the same level as our [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine) statement, we define a [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) class which will serve as a factory for new [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) objects:

**`>>> from** **sqlalchemy.orm** **import** sessionmaker
**>>>** Session = sessionmaker(bind=engine)`

In the case where your application does not yet have an [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) when you define your module-level objects, just set it up like this:

**`>>>** Session = sessionmaker()`

Later, when you create your engine with [`create_engine()`](https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine), connect it to the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) using [`sessionmaker.configure()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.sessionmaker.configure):

**`>>>** Session.configure(bind=engine)  *# once engine is available*`

**Session Lifecycle Patterns**
The question of when to make a [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) depends a lot on what kind of application is being built. Keep in mind, the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) is just a workspace for your objects, local to a particular database connection - if you think of an application thread as a guest at a dinner party, the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) is the guest’s plate and the objects it holds are the food (and the database…the kitchen?)! More on this topic available at [When do I construct a Session, when do I commit it, and when do I close it?](https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate).

This custom-made [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) class will create new [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) objects which are bound to our database. Other transactional characteristics may be defined when calling [`sessionmaker`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.sessionmaker) as well; these are described in a later chapter. Then, whenever you need to have a conversation with the database, you instantiate a [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session):

**`>>>** session = Session()`

The above [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) is associated with our SQLite-enabled [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine), but it hasn’t opened any connections yet. When it’s first used, it retrieves a connection from a pool of connections maintained by the [`Engine`](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine), and holds onto it until we commit all changes and/or close the session object.

## **Adding and Updating Objects**

To persist our `User` object, we [`Session.add()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.add) it to our [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session):

**`>>>** ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
**>>>** session.add(ed_user)`

At this point, we say that the instance is **pending**; no SQL has yet been issued and the object is not yet represented by a row in the database. The [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) will issue the SQL to persist `Ed Jones` as soon as is needed, using a process known as a **flush**. If we query the database for `Ed Jones`, all pending information will first be flushed, and the query is issued immediately thereafter.

For example, below we create a new [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) object which loads instances of `User`. We “filter by” the `name` attribute of `ed`, and indicate that we’d like only the first result in the full list of rows. A `User` instance is returned which is equivalent to that which we’ve added:

`>>> our_user = session.query(User).filter_by(name='ed').first() 
**BEGIN** (**implicit**)
**INSERT** **INTO** users (name, fullname, nickname) **VALUES** (?, ?, ?)
('ed', 'Ed Jones', 'edsnickname')
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name = ?
 **LIMIT** ? **OFFSET** ?
('ed', 1, 0)
>>> our_user
<User(name='ed', fullname='Ed Jones', nickname='edsnickname')>`

In fact, the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) has identified that the row returned is the **same** row as one already represented within its internal map of objects, so we actually got back the identical instance as that which we just added:

**`>>>** ed_user **is** our_user
True`

The ORM concept at work here is known as an [identity map](https://docs.sqlalchemy.org/en/13/glossary.html#term-identity-map) and ensures that all operations upon a particular row within a [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) operate upon the same set of data. Once an object with a particular primary key is present in the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session), all SQL queries on that [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) will always return the same Python object for that particular primary key; it also will raise an error if an attempt is made to place a second, already-persisted object with the same primary key within the session.

We can add more `User` objects at once using [`add_all()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.add_all):

`>>> session.add_all([
...     User(name='wendy', fullname='Wendy Williams', nickname='windy'),
...     User(name='mary', fullname='Mary Contrary', nickname='mary'),
...     User(name='fred', fullname='Fred Flintstone', nickname='freddy')])`

Also, we’ve decided Ed’s nickname isn’t that great, so lets change it:

`>>> ed_user.nickname = 'eddie'`

The [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) is paying attention. It knows, for example, that `Ed Jones` has been modified:

`>>> session.dirty
IdentitySet([<User(name='ed', fullname='Ed Jones', nickname='eddie')>])`

and that three new `User` objects are pending:

`>>> session.new  
IdentitySet([<User(name='wendy', fullname='Wendy Williams', nickname='windy')>,
<User(name='mary', fullname='Mary Contrary', nickname='mary')>,
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')>])`

We tell the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) that we’d like to issue all remaining changes to the database and commit the transaction, which has been in progress throughout. We do this via [`Session.commit()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.commit). The [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) emits the `UPDATE` statement for the nickname change on “ed”, as well as `INSERT` statements for the three new `User` objects we’ve added:

`>>> session.commit()
**UPDATE** users **SET** nickname=? **WHERE** users.id = ?
('eddie', 1)
**INSERT** **INTO** users (name, fullname, nickname) **VALUES** (?, ?, ?)
('wendy', 'Wendy Williams', 'windy')
**INSERT** **INTO** users (name, fullname, nickname) **VALUES** (?, ?, ?)
('mary', 'Mary Contrary', 'mary')
**INSERT** **INTO** users (name, fullname, nickname) **VALUES** (?, ?, ?)
('fred', 'Fred Flintstone', 'freddy')
**COMMIT**`

[`Session.commit()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.commit) flushes the remaining changes to the database, and commits the transaction. The connection resources referenced by the session are now returned to the connection pool. Subsequent operations with this session will occur in a **new** transaction, which will again re-acquire connection resources when first needed.

If we look at Ed’s `id` attribute, which earlier was `None`, it now has a value:

`>>> ed_user.id 
**BEGIN** (**implicit**)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.id = ?
(1,)
1`

After the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) inserts new rows in the database, all newly generated identifiers and database-generated defaults become available on the instance, either immediately or via load-on-first-access. In this case, the entire row was re-loaded on access because a new transaction was begun after we issued [`Session.commit()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.commit). SQLAlchemy by default refreshes data from a previous transaction the first time it’s accessed within a new transaction, so that the most recent state is available. The level of reloading is configurable as is described in [Using the Session](https://docs.sqlalchemy.org/en/13/orm/session.html).

**Session Object States**
As our `User` object moved from being outside the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session), to inside the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) without a primary key, to actually being inserted, it moved between three out of five available “object states” - **transient**, **pending**, and **persistent**. Being aware of these states and what they mean is always a good idea - be sure to read [Quickie Intro to Object States](https://docs.sqlalchemy.org/en/13/orm/session_state_management.html#session-object-states) for a quick overview.

## **Rolling Back**

Since the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session) works within a transaction, we can roll back changes made too. Let’s make two changes that we’ll revert; `ed_user`’s user name gets set to `Edwardo`:

`>>> ed_user.name = 'Edwardo'`

and we’ll add another erroneous user, `fake_user`:

`>>> fake_user = User(name='fakeuser', fullname='Invalid', nickname='12345')
>>> session.add(fake_user)`

Querying the session, we can see that they’re flushed into the current transaction:

`>>> session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
**UPDATE** users **SET** name=? **WHERE** users.id = ?
('Edwardo', 1)
**INSERT** **INTO** users (name, fullname, nickname) **VALUES** (?, ?, ?)
('fakeuser', 'Invalid', '12345')
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name **IN** (?, ?)
('Edwardo', 'fakeuser')
[<User(name='Edwardo', fullname='Ed Jones', nickname='eddie')>, <User(name='fakeuser', fullname='Invalid', nickname='12345')>]`

Rolling back, we can see that `ed_user`’s name is back to `ed`, and `fake_user` has been kicked out of the session:

`>>> session.rollback()
**ROLLBACK**>>> ed_user.name
**BEGIN** (**implicit**)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.id = ?
(1,)
u'ed'
>>> fake_user **in** session
**False**`

issuing a SELECT illustrates the changes made to the database:

`>>> session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name **IN** (?, ?)
('ed', 'fakeuser')
[<User(name='ed', fullname='Ed Jones', nickname='eddie')>]`

## **Querying**

A [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) object is created using the [`query()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.query) method on [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session). This function takes a variable number of arguments, which can be any combination of classes and class-instrumented descriptors. Below, we indicate a [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) which loads `User` instances. When evaluated in an iterative context, the list of `User` objects present is returned:

`>>> **for** instance **in** session.query(User).order_by(User.id):
...     print(instance.name, instance.fullname)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users **ORDER** **BY** users.id
()
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone`

The [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) also accepts ORM-instrumented descriptors as arguments. Any time multiple class entities or column-based entities are expressed as arguments to the [`query()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.query) function, the return result is expressed as tuples:

`>>> **for** name, fullname **in** session.query(User.name, User.fullname):
...     print(name, fullname)
**SELECT** users.name **AS** users_name,
        users.fullname **AS** users_fullname
**FROM** users
()
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone`

The tuples returned by [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) are *named* tuples, supplied by the [`KeyedTuple`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.util.KeyedTuple) class, and can be treated much like an ordinary Python object. The names are the same as the attribute’s name for an attribute, and the class name for a class:

`>>> **for** row **in** session.query(User, User.name).all():
...    print(row.User, row.name)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
()
<User(name='ed', fullname='Ed Jones', nickname='eddie')> ed
<User(name='wendy', fullname='Wendy Williams', nickname='windy')> wendy
<User(name='mary', fullname='Mary Contrary', nickname='mary')> mary
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')> fred`

You can control the names of individual column expressions using the [`ColumnElement.label()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement.label) construct, which is available from any [`ColumnElement`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.ColumnElement)-derived object, as well as any class attribute which is mapped to one (such as `User.name`):

`>>> **for** row **in** session.query(User.name.label('name_label')).all():
...    print(row.name_label)
**SELECT** users.name **AS** name_label
**FROM** users
()
ed
wendy
mary
fred`

The name given to a full entity such as `User`, assuming that multiple entities are present in the call to [`Session.query()`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session.query), can be controlled using [`aliased()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.aliased) :

`>>> **from** **sqlalchemy.orm** **import** aliased
>>> user_alias = aliased(User, name='user_alias')

>>> **for** row **in** session.query(user_alias, user_alias.name).all():
...    print(row.user_alias)
**SELECT** user_alias.id **AS** user_alias_id,
        user_alias.name **AS** user_alias_name,
        user_alias.fullname **AS** user_alias_fullname,
        user_alias.nickname **AS** user_alias_nickname
**FROM** users **AS** user_alias
()
<User(name='ed', fullname='Ed Jones', nickname='eddie')>
<User(name='wendy', fullname='Wendy Williams', nickname='windy')>
<User(name='mary', fullname='Mary Contrary', nickname='mary')>
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')>`

Basic operations with [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) include issuing LIMIT and OFFSET, most conveniently using Python array slices and typically in conjunction with ORDER BY:

`>>> **for** u **in** session.query(User).order_by(User.id)[1:3]:
...    print(u)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users **ORDER** **BY** users.id
**LIMIT** ? **OFFSET** ?
(2, 1)
<User(name='wendy', fullname='Wendy Williams', nickname='windy')>
<User(name='mary', fullname='Mary Contrary', nickname='mary')>`

and filtering results, which is accomplished either with [`filter_by()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter_by), which uses keyword arguments:

`>>> **for** name, **in** session.query(User.name).\
...             filter_by(fullname='Ed Jones'):
...    print(name)
**SELECT** users.name **AS** users_name **FROM** users
**WHERE** users.fullname = ?
('Ed Jones',)
ed`

…or [`filter()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter), which uses more flexible SQL expression language constructs. These allow you to use regular Python operators with the class-level attributes on your mapped class:

`>>> **for** name, **in** session.query(User.name).\
...             filter(User.fullname=='Ed Jones'):
...    print(name)
**SELECT** users.name **AS** users_name **FROM** users
**WHERE** users.fullname = ?
('Ed Jones',)
ed`

The [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) object is fully **generative**, meaning that most method calls return a new [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) object upon which further criteria may be added. For example, to query for users named “ed” with a full name of “Ed Jones”, you can call [`filter()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter) twice, which joins criteria using `AND`:

`>>> **for** user **in** session.query(User).\
...          filter(User.name=='ed').\
...          filter(User.fullname=='Ed Jones'):
...    print(user)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name = ? **AND** users.fullname = ?
('ed', 'Ed Jones')
<User(name='ed', fullname='Ed Jones', nickname='eddie')>`

### **Common Filter Operators**

Here’s a rundown of some of the most common operators used in [`filter()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter):

- [`ColumnOperators.__eq__()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__eq__):
    
    `query.filter(User.name == 'ed')`
    
- [`ColumnOperators.__ne__()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.__ne__):
    
    `query.filter(User.name != 'ed')`
    
- [`ColumnOperators.like()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like):
    
    `query.filter(User.name.like('*%e*d%'))`
    

> Note
> 
> 
> [`ColumnOperators.like()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.like) renders the LIKE operator, which is case insensitive on some backends, and case sensitive on others. For guaranteed case-insensitive comparisons, use [`ColumnOperators.ilike()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike).
> 
- [`ColumnOperators.ilike()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike) (case-insensitive LIKE):
    
    `query.filter(User.name.ilike('*%e*d%'))`
    

> Note
> 
> 
> most backends don’t support ILIKE directly. For those, the [`ColumnOperators.ilike()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.ilike) operator renders an expression combining LIKE with the LOWER SQL function applied to each operand.
> 
- [`ColumnOperators.in_()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.in_):
    
    `query.filter(User.name.in_(['ed', 'wendy', 'jack']))
    
    *# works with query objects too:*query.filter(User.name.in_(
        session.query(User.name).filter(User.name.like('*%e*d%'))
    ))
    
    *# use tuple_() for composite (multi-column) queries***from** **sqlalchemy** **import** tuple_
    query.filter(
        tuple_(User.name, User.nickname).\
        in_([('ed', 'edsnickname'), ('wendy', 'windy')])
    )`
    
- [`ColumnOperators.notin_()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.notin_):
    
    `query.filter(~User.name.in_(['ed', 'wendy', 'jack']))`
    
- [`ColumnOperators.is_()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.is_):
    
    `query.filter(User.name == **None**)
    
    *# alternatively, if pep8/linters are a concern*query.filter(User.name.is_(**None**))`
    
- [`ColumnOperators.isnot()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.isnot):
    
    `query.filter(User.name != **None**)
    
    *# alternatively, if pep8/linters are a concern*query.filter(User.name.isnot(**None**))`
    
- [`AND`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.and_):
    
    `*# use and_()***from** **sqlalchemy** **import** and_
    query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
    
    *# or send multiple expressions to .filter()*query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
    
    *# or chain multiple filter()/filter_by() calls*query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')`
    

> Note
> 
> 
> Make sure you use [`and_()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.and_) and **not** the Python `and` operator!
> 
- [`OR`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.or_):
    
    **`from** **sqlalchemy** **import** or_
    query.filter(or_(User.name == 'ed', User.name == 'wendy'))`
    

> Note
> 
> 
> Make sure you use [`or_()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.or_) and **not** the Python `or` operator!
> 
- [`ColumnOperators.match()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match):
    
    `query.filter(User.name.match('wendy'))`
    

> Note
> 
> 
> [`ColumnOperators.match()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators.match) uses a database-specific `MATCH` or `CONTAINS` function; its behavior will vary by backend and is not available on some backends such as SQLite.
> 

### **Returning Lists and Scalars**

A number of methods on [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) immediately issue SQL and return a value containing loaded database results. Here’s a brief tour:

- [`Query.all()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.all) returns a list:
    
    `>>> query = session.query(User).filter(User.name.like('*%e*d')).order_by(User.id)
    >>> query.all()
    **SELECT** users.id **AS** users_id,
            users.name **AS** users_name,
            users.fullname **AS** users_fullname,
            users.nickname **AS** users_nickname
    **FROM** users
    **WHERE** users.name **LIKE** ? **ORDER** **BY** users.id
    ('%ed',)
    [<User(name='ed', fullname='Ed Jones', nickname='eddie')>,
          <User(name='fred', fullname='Fred Flintstone', nickname='freddy')>]`
    
    **Warning**
    
    When the [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) object returns lists of ORM-mapped objects such as the `User` object above, the entries are **deduplicated** based on primary key, as the results are interpreted from the SQL result set. That is, if SQL query returns a row with `id=7` twice, you would only get a single `User(id=7)` object back in the result list. This does not apply to the case when individual columns are queried.
    
    **See also**
    
    [My Query does not return the same number of objects as query.count() tells me - why?](https://docs.sqlalchemy.org/en/13/faq/sessions.html#faq-query-deduplicating)
    
- [`Query.first()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.first) applies a limit of one and returns the first result as a scalar:
    
    `>>> query.first()
    **SELECT** users.id **AS** users_id,
            users.name **AS** users_name,
            users.fullname **AS** users_fullname,
            users.nickname **AS** users_nickname
    **FROM** users
    **WHERE** users.name **LIKE** ? **ORDER** **BY** users.id
     **LIMIT** ? **OFFSET** ?
    ('%ed', 1, 0)
    <User(name='ed', fullname='Ed Jones', nickname='eddie')>`
    
- [`Query.one()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one) fully fetches all rows, and if not exactly one object identity or composite row is present in the result, raises an error. With multiple rows found:
    
    `>>> user = query.one()
    Traceback (most recent call last):
    ...
    MultipleResultsFound: Multiple rows were found **for** one()`
    
    With no rows found:
    
    `>>> user = query.filter(User.id == 99).one()
    Traceback (most recent call last):
    ...
    NoResultFound: No row was found **for** one()`
    
    The [`Query.one()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one) method is great for systems that expect to handle “no items found” versus “multiple items found” differently; such as a RESTful web service, which may want to raise a “404 not found” when no results are found, but raise an application error when multiple results are found.
    
- [`Query.one_or_none()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one_or_none) is like [`Query.one()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one), except that if no results are found, it doesn’t raise an error; it just returns `None`. Like [`Query.one()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one), however, it does raise an error if multiple results are found.
- [`Query.scalar()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.scalar) invokes the [`Query.one()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.one) method, and upon success returns the first column of the row:
    
    `>>> query = session.query(User.id).filter(User.name == 'ed').\
    ...    order_by(User.id)
    >>> query.scalar()
    **SELECT** users.id **AS** users_id
    **FROM** users
    **WHERE** users.name = ? **ORDER** **BY** users.id
    ('ed',)
    1`
    

### **Using Textual SQL**

Literal strings can be used flexibly with [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query), by specifying their use with the [`text()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, which is accepted by most applicable methods. For example, [`Query.filter()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter) and [`Query.order_by()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.order_by):

`>>> **from** **sqlalchemy** **import** text
>>> **for** user **in** session.query(User).\
...             filter(text("id<224")).\
...             order_by(text("id")).all():
...     print(user.name)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** id<224 **ORDER** **BY** id
()
ed
wendy
mary
fred`

Bind parameters can be specified with string-based SQL, using a colon. To specify the values, use the [`Query.params()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.params) method:

`>>> session.query(User).filter(text("id<:value and name=:name")).\
...     params(value=224, name='fred').order_by(User.id).one()
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** id<? **and** name=? **ORDER** **BY** users.id
(224, 'fred')
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')>`

To use an entirely string-based statement, a [`text()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.text) construct representing a complete statement can be passed to [`Query.from_statement()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.from_statement). Without additional specifiers, the columns in the string SQL are matched to the model columns based on name, such as below where we use just an asterisk to represent loading all columns:

`>>> session.query(User).from_statement(
...  text("SELECT * FROM users where name=:name")).params(name='ed').all()
**SELECT** * **FROM** users **where** name=?
('ed',)
[<User(name='ed', fullname='Ed Jones', nickname='eddie')>]`

Matching columns on name works for simple cases but can become unwieldy when dealing with complex statements that contain duplicate column names or when using anonymized ORM constructs that don’t easily match to specific names. Additionally, there is typing behavior present in our mapped columns that we might find necessary when handling result rows. For these cases, the [`text()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.text) construct allows us to link its textual SQL to Core or ORM-mapped column expressions positionally; we can achieve this by passing column expressions as positional arguments to the [`TextClause.columns()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method:

`>>> stmt = text("SELECT name, id, fullname, nickname "
...             "FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id, User.fullname, User.nickname)
>>> session.query(User).from_statement(stmt).params(name='ed').all()
**SELECT** name, id, fullname, nickname **FROM** users **where** name=?
('ed',)
[<User(name='ed', fullname='Ed Jones', nickname='eddie')>]`

**New in version 1.1:** The [`TextClause.columns()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.TextClause.columns) method now accepts column expressions which will be matched positionally to a plain text SQL result set, eliminating the need for column names to match or even be unique in the SQL statement.

When selecting from a [`text()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.text) construct, the [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) may still specify what columns and entities are to be returned; instead of `query(User)` we can also ask for the columns individually, as in any other case:

`>>> stmt = text("SELECT name, id FROM users where name=:name")
>>> stmt = stmt.columns(User.name, User.id)
>>> session.query(User.id, User.name).\
...          from_statement(stmt).params(name='ed').all()
**SELECT** name, id **FROM** users **where** name=?
('ed',)
[(1, u'ed')]`

**See also**

[Using Textual SQL](https://docs.sqlalchemy.org/en/13/core/tutorial.html#sqlexpression-text) - The [`text()`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.text) construct explained from the perspective of Core-only queries.

### **Counting**

[`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) includes a convenience method for counting called [`Query.count()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.count):

`>>> session.query(User).filter(User.name.like('*%e*d')).count()
**SELECT** **count**(*) **AS** count_1
**FROM** (**SELECT** users.id **AS** users_id,
                users.name **AS** users_name,
                users.fullname **AS** users_fullname,
                users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name **LIKE** ?) **AS** anon_1
('%ed',)
2`

**Counting on `count()`**
[`Query.count()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.count) used to be a very complicated method when it would try to guess whether or not a subquery was needed around the existing query, and in some exotic cases it wouldn’t do the right thing. Now that it uses a simple subquery every time, it’s only two lines long and always returns the right answer. Use `func.count()` if a particular statement absolutely cannot tolerate the subquery being present.

The [`Query.count()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.count) method is used to determine how many rows the SQL statement would return. Looking at the generated SQL above, SQLAlchemy always places whatever it is we are querying into a subquery, then counts the rows from that. In some cases this can be reduced to a simpler `SELECT count(*) FROM table`, however modern versions of SQLAlchemy don’t try to guess when this is appropriate, as the exact SQL can be emitted using more explicit means.

For situations where the “thing to be counted” needs to be indicated specifically, we can specify the “count” function directly using the expression `func.count()`, available from the [`expression.func`](https://docs.sqlalchemy.org/en/13/core/sqlelement.html#sqlalchemy.sql.expression.func) construct. Below we use it to return the count of each distinct user name:

`>>> **from** **sqlalchemy** **import** func
>>> session.query(func.count(User.name), User.name).group_by(User.name).all()
**SELECT** **count**(users.name) **AS** count_1, users.name **AS** users_name
**FROM** users **GROUP** **BY** users.name
()
[(1, u'ed'), (1, u'fred'), (1, u'mary'), (1, u'wendy')]`

To achieve our simple `SELECT count(*) FROM table`, we can apply it as:

`>>> session.query(func.count('*')).select_from(User).scalar()
**SELECT** **count**(?) **AS** count_1
**FROM** users
('*',)
4`

The usage of [`Query.select_from()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.select_from) can be removed if we express the count in terms of the `User` primary key directly:

`>>> session.query(func.count(User.id)).scalar()
**SELECT** **count**(users.id) **AS** count_1
**FROM** users
()
4`

## **Building a Relationship**

Let’s consider how a second table, related to `User`, can be mapped and queried. Users in our system can store any number of email addresses associated with their username. This implies a basic one to many association from the `users` to a new table which stores email addresses, which we will call `addresses`. Using declarative, we define this table along with its mapped class, `Address`:

**`>>> from** **sqlalchemy** **import** ForeignKey
**>>> from** **sqlalchemy.orm** **import** relationship

**>>> class** **Address**(Base):
**...**     __tablename__ = 'addresses'
**...**     id = Column(Integer, primary_key=**True**)
**...**     email_address = Column(String, nullable=**False**)
**...**     user_id = Column(Integer, ForeignKey('users.id'))
**......**     user = relationship("User", back_populates="addresses")
**......**     **def** __repr__(self):
**...**         **return** "<Address(email_address='*%s*')>" % self.email_address

**>>>** User.addresses = relationship(
**...**     "Address", order_by=Address.id, back_populates="user")`

The above class introduces the [`ForeignKey`](https://docs.sqlalchemy.org/en/13/core/constraints.html#sqlalchemy.schema.ForeignKey) construct, which is a directive applied to [`Column`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column) that indicates that values in this column should be [constrained](https://docs.sqlalchemy.org/en/13/glossary.html#term-constrained) to be values present in the named remote column. This is a core feature of relational databases, and is the “glue” that transforms an otherwise unconnected collection of tables to have rich overlapping relationships. The [`ForeignKey`](https://docs.sqlalchemy.org/en/13/core/constraints.html#sqlalchemy.schema.ForeignKey) above expresses that values in the `addresses.user_id` column should be constrained to those values in the `users.id` column, i.e. its primary key.

A second directive, known as [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship), tells the ORM that the `Address` class itself should be linked to the `User` class, using the attribute `Address.user`. [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) uses the foreign key relationships between the two tables to determine the nature of this linkage, determining that `Address.user` will be [many to one](https://docs.sqlalchemy.org/en/13/glossary.html#term-many-to-one). An additional [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) directive is placed on the `User` mapped class under the attribute `User.addresses`. In both [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) directives, the parameter [`relationship.back_populates`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) is assigned to refer to the complementary attribute names; by doing so, each [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) can make intelligent decision about the same relationship as expressed in reverse; on one side, `Address.user` refers to a `User` instance, and on the other side, `User.addresses` refers to a list of `Address` instances.

**Note**

The [`relationship.back_populates`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) parameter is a newer version of a very common SQLAlchemy feature called [`relationship.backref`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref). The [`relationship.backref`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.backref) parameter hasn’t gone anywhere and will always remain available! The [`relationship.back_populates`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship.params.back_populates) is the same thing, except a little more verbose and easier to manipulate. For an overview of the entire topic, see the section [Linking Relationships with Backref](https://docs.sqlalchemy.org/en/13/orm/backref.html#relationships-backref).

The reverse side of a many-to-one relationship is always [one to many](https://docs.sqlalchemy.org/en/13/glossary.html#term-one-to-many). A full catalog of available [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) configurations is at [Basic Relationship Patterns](https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#relationship-patterns).

The two complementing relationships `Address.user` and `User.addresses` are referred to as a [bidirectional relationship](https://docs.sqlalchemy.org/en/13/glossary.html#term-bidirectional-relationship), and is a key feature of the SQLAlchemy ORM. The section [Linking Relationships with Backref](https://docs.sqlalchemy.org/en/13/orm/backref.html#relationships-backref) discusses the “backref” feature in detail.

Arguments to [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) which concern the remote class can be specified using strings, assuming the Declarative system is in use. Once all mappings are complete, these strings are evaluated as Python expressions in order to produce the actual argument, in the above case the `User` class. The names which are allowed during this evaluation include, among other things, the names of all classes which have been created in terms of the declared base.

See the docstring for [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) for more detail on argument style.

**Did you know ?**
• a FOREIGN KEY constraint in most (though not all) relational databases can only link to a primary key column, or a column that has a UNIQUE constraint.
• a FOREIGN KEY constraint that refers to a multiple column primary key, and itself has multiple columns, is known as a “composite foreign key”. It can also reference a subset of those columns.
• FOREIGN KEY columns can automatically update themselves, in response to a change in the referenced column or row. This is known as the CASCADE *referential action*, and is a built in function of the relational database.
• FOREIGN KEY can refer to its own table. This is referred to as a “self-referential” foreign key.
• Read more about foreign keys at [Foreign Key - Wikipedia](http://en.wikipedia.org/wiki/Foreign_key).

We’ll need to create the `addresses` table in the database, so we will issue another CREATE from our metadata, which will skip over tables which have already been created:

`>>> Base.metadata.create_all(engine)
PRAGMA...
**CREATE** **TABLE** addresses (
    id INTEGER **NOT** **NULL**,
    email_address VARCHAR **NOT** **NULL**,
    user_id INTEGER,
    **PRIMARY** **KEY** (id),
     **FOREIGN** **KEY**(user_id) **REFERENCES** users (id)
)
()
**COMMIT**`

## **Working with Related Objects**

Now when we create a `User`, a blank `addresses` collection will be present. Various collection types, such as sets and dictionaries, are possible here (see [Customizing Collection Access](https://docs.sqlalchemy.org/en/13/orm/collections.html#custom-collections) for details), but by default, the collection is a Python list.

`>>> jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
>>> jack.addresses
[]`

We are free to add `Address` objects on our `User` object. In this case we just assign a full list directly:

`>>> jack.addresses = [
...                 Address(email_address='jack@google.com'),
...                 Address(email_address='j25@yahoo.com')]`

When using a bidirectional relationship, elements added in one direction automatically become visible in the other direction. This behavior occurs based on attribute on-change events and is evaluated in Python, without using any SQL:

`>>> jack.addresses[1]
<Address(email_address='j25@yahoo.com')>

>>> jack.addresses[1].user
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>`

Let’s add and commit `Jack Bean` to the database. `jack` as well as the two `Address` members in the corresponding `addresses` collection are both added to the session at once, using a process known as **cascading**:

`>>> session.add(jack)
>>> session.commit()
**INSERT** **INTO** users (name, fullname, nickname) **VALUES** (?, ?, ?)
('jack', 'Jack Bean', 'gjffdd')
**INSERT** **INTO** addresses (email_address, user_id) **VALUES** (?, ?)
('jack@google.com', 5)
**INSERT** **INTO** addresses (email_address, user_id) **VALUES** (?, ?)
('j25@yahoo.com', 5)
**COMMIT**`

Querying for Jack, we get just Jack back. No SQL is yet issued for Jack’s addresses:

`>>> jack = session.query(User).\
... filter_by(name='jack').one()
**BEGIN** (**implicit**)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name = ?
('jack',)
>>> jack
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>`

Let’s look at the `addresses` collection. Watch the SQL:

`>>> jack.addresses
**SELECT** addresses.id **AS** addresses_id,
        addresses.email_address **AS**        addresses_email_address,
        addresses.user_id **AS** addresses_user_id
**FROM** addresses
**WHERE** ? = addresses.user_id **ORDER** **BY** addresses.id
(5,)
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]`

When we accessed the `addresses` collection, SQL was suddenly issued. This is an example of a [lazy loading](https://docs.sqlalchemy.org/en/13/glossary.html#term-lazy-loading) relationship. The `addresses` collection is now loaded and behaves just like an ordinary list. We’ll cover ways to optimize the loading of this collection in a bit.

## **Querying with Joins**

Now that we have two tables, we can show some more features of [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query), specifically how to create queries that deal with both tables at the same time. The [Wikipedia page on SQL JOIN](http://en.wikipedia.org/wiki/Join_%28SQL%29) offers a good introduction to join techniques, several of which we’ll illustrate here.

To construct a simple implicit join between `User` and `Address`, we can use [`Query.filter()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter) to equate their related columns together. Below we load the `User` and `Address` entities at once using this method:

`>>> **for** u, a **in** session.query(User, Address).\
...                     filter(User.id==Address.user_id).\
...                     filter(Address.email_address=='jack@google.com').\
...                     all():
...     print(u)
...     print(a)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname,
        addresses.id **AS** addresses_id,
        addresses.email_address **AS** addresses_email_address,
        addresses.user_id **AS** addresses_user_id
**FROM** users, addresses
**WHERE** users.id = addresses.user_id
        **AND** addresses.email_address = ?
('jack@google.com',)
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
<Address(email_address='jack@google.com')>`

The actual SQL JOIN syntax, on the other hand, is most easily achieved using the [`Query.join()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join) method:

`>>> session.query(User).join(Address).\
...         filter(Address.email_address=='jack@google.com').\
...         all()
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users **JOIN** addresses **ON** users.id = addresses.user_id
**WHERE** addresses.email_address = ?
('jack@google.com',)
[<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>]`

[`Query.join()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join) knows how to join between `User` and `Address` because there’s only one foreign key between them. If there were no foreign keys, or several, [`Query.join()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join) works better when one of the following forms are used:

`query.join(Address, User.id==Address.user_id)    *# explicit condition*query.join(User.addresses)                       *# specify relationship from left to right*query.join(Address, User.addresses)              *# same, with explicit target*`

As you would expect, the same idea is used for “outer” joins, using the [`Query.outerjoin()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.outerjoin) function:

`query.outerjoin(User.addresses)   *# LEFT OUTER JOIN*`

The reference documentation for [`Query.join()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join) contains detailed information and examples of the calling styles accepted by this method; [`Query.join()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join) is an important method at the center of usage for any SQL-fluent application.

**What does [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) select from if there’s multiple entities?**
The [`Query.join()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join) method will **typically join from the leftmost item** in the list of entities, when the ON clause is omitted, or if the ON clause is a plain SQL expression. To control the first entity in the list of JOINs, use the [`Query.select_from()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.select_from) method:

`query = session.query(User, Address).select_from(Address).join(User)`

### **Using Aliases**

When querying across multiple tables, if the same table needs to be referenced more than once, SQL typically requires that the table be *aliased* with another name, so that it can be distinguished against other occurrences of that table. This is supported using the [`aliased()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.aliased) construct. When joining to relationships using using [`aliased()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.aliased), the special attribute method [`PropComparator.of_type()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) may be used to alter the target of a relationship join to refer to a given [`aliased()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.aliased) object. Below we join to the `Address` entity twice, to locate a user who has two distinct email addresses at the same time:

`>>> **from** **sqlalchemy.orm** **import** aliased
>>> adalias1 = aliased(Address)
>>> adalias2 = aliased(Address)
>>> **for** username, email1, email2 **in** \
...     session.query(User.name, adalias1.email_address, adalias2.email_address).\
...     join(User.addresses.of_type(adalias1)).\
...     join(User.addresses.of_type(adalias2)).\
...     filter(adalias1.email_address=='jack@google.com').\
...     filter(adalias2.email_address=='j25@yahoo.com'):
...     print(username, email1, email2)
**SELECT** users.name **AS** users_name,
        addresses_1.email_address **AS** addresses_1_email_address,
        addresses_2.email_address **AS** addresses_2_email_address
**FROM** users **JOIN** addresses **AS** addresses_1
        **ON** users.id = addresses_1.user_id
**JOIN** addresses **AS** addresses_2
        **ON** users.id = addresses_2.user_id
**WHERE** addresses_1.email_address = ?
        **AND** addresses_2.email_address = ?
('jack@google.com', 'j25@yahoo.com')
jack jack**@google**.com j25**@yahoo**.com`

In addition to using the [`PropComparator.of_type()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.PropComparator.of_type) method, it is common to see the `Query.join()` method joining to a specific target by indicating it separately:

`*# equivalent to query.join(User.addresses.of_type(adalias1))*q = query.join(adalias1, User.addresses)`

### **Using Subqueries**

The [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) is suitable for generating statements which can be used as subqueries. Suppose we wanted to load `User` objects along with a count of how many `Address` records each user has. The best way to generate SQL like this is to get the count of addresses grouped by user ids, and JOIN to the parent. In this case we use a LEFT OUTER JOIN so that we get rows back for those users who don’t have any addresses, e.g.:

`SELECT users.*, adr_count.address_count FROM users LEFT OUTER JOIN
    (SELECT user_id, count(*) AS address_count
        FROM addresses GROUP BY user_id) AS adr_count
    ON users.id=adr_count.user_id`

Using the [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query), we build a statement like this from the inside out. The `statement` accessor returns a SQL expression representing the statement generated by a particular [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) - this is an instance of a [`select()`](https://docs.sqlalchemy.org/en/13/core/selectable.html#sqlalchemy.sql.expression.select) construct, which are described in [SQL Expression Language Tutorial](https://docs.sqlalchemy.org/en/13/core/tutorial.html):

**`>>> from** **sqlalchemy.sql** **import** func
**>>>** stmt = session.query(Address.user_id, func.count('*').\
**...**         label('address_count')).\
**...**         group_by(Address.user_id).subquery()`

The `func` keyword generates SQL functions, and the `subquery()` method on [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) produces a SQL expression construct representing a SELECT statement embedded within an alias (it’s actually shorthand for `query.statement.alias()`).

Once we have our statement, it behaves like a [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) construct, such as the one we created for `users` at the start of this tutorial. The columns on the statement are accessible through an attribute called `c`:

`>>> **for** u, count **in** session.query(User, stmt.c.address_count).\
...     outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
...     print(u, count)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname,
        anon_1.address_count **AS** anon_1_address_count
**FROM** users **LEFT** **OUTER** **JOIN**    (**SELECT** addresses.user_id **AS** user_id, **count**(?) **AS** address_count
    **FROM** addresses **GROUP** **BY** addresses.user_id) **AS** anon_1
    **ON** users.id = anon_1.user_id
**ORDER** **BY** users.id
('*',)
<User(name='ed', fullname='Ed Jones', nickname='eddie')> **None**<User(name='wendy', fullname='Wendy Williams', nickname='windy')> **None**<User(name='mary', fullname='Mary Contrary', nickname='mary')> **None**<User(name='fred', fullname='Fred Flintstone', nickname='freddy')> **None**<User(name='jack', fullname='Jack Bean', nickname='gjffdd')> 2`

### **Selecting Entities from Subqueries**

Above, we just selected a result that included a column from a subquery. What if we wanted our subquery to map to an entity ? For this we use `aliased()` to associate an “alias” of a mapped class to a subquery:

`>>> stmt = session.query(Address).\
...                 filter(Address.email_address != 'j25@yahoo.com').\
...                 subquery()
>>> adalias = aliased(Address, stmt)
>>> **for** user, address **in** session.query(User, adalias).\
...         join(adalias, User.addresses):
...     print(user)
...     print(address)
**SELECT** users.id **AS** users_id,
            users.name **AS** users_name,
            users.fullname **AS** users_fullname,
            users.nickname **AS** users_nickname,
            anon_1.id **AS** anon_1_id,
            anon_1.email_address **AS** anon_1_email_address,
            anon_1.user_id **AS** anon_1_user_id
**FROM** users **JOIN**    (**SELECT** addresses.id **AS** id,
            addresses.email_address **AS** email_address,
            addresses.user_id **AS** user_id
    **FROM** addresses
    **WHERE** addresses.email_address != ?) **AS** anon_1
    **ON** users.id = anon_1.user_id
('j25@yahoo.com',)
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
<Address(email_address='jack@google.com')>`

### **Using EXISTS**

The EXISTS keyword in SQL is a boolean operator which returns True if the given expression contains any rows. It may be used in many scenarios in place of joins, and is also useful for locating rows which do not have a corresponding row in a related table.

There is an explicit EXISTS construct, which looks like this:

`>>> **from** **sqlalchemy.sql** **import** exists
>>> stmt = exists().where(Address.user_id==User.id)
>>> **for** name, **in** session.query(User.name).filter(stmt):
...     print(name)
**SELECT** users.name **AS** users_name
**FROM** users
**WHERE** **EXISTS** (**SELECT** *
**FROM** addresses
**WHERE** addresses.user_id = users.id)
()
jack`

The [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) features several operators which make usage of EXISTS automatically. Above, the statement can be expressed along the `User.addresses` relationship using [`Comparator.any()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.any):

`>>> **for** name, **in** session.query(User.name).\
...         filter(User.addresses.any()):
...     print(name)
**SELECT** users.name **AS** users_name
**FROM** users
**WHERE** **EXISTS** (**SELECT** 1
**FROM** addresses
**WHERE** users.id = addresses.user_id)
()
jack`

[`Comparator.any()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.any) takes criterion as well, to limit the rows matched:

`>>> **for** name, **in** session.query(User.name).\
...     filter(User.addresses.any(Address.email_address.like('*%g*oogle%'))):
...     print(name)
**SELECT** users.name **AS** users_name
**FROM** users
**WHERE** **EXISTS** (**SELECT** 1
**FROM** addresses
**WHERE** users.id = addresses.user_id **AND** addresses.email_address **LIKE** ?)
('%google%',)
jack`

[`Comparator.has()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.has) is the same operator as [`Comparator.any()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.any) for many-to-one relationships (note the `~` operator here too, which means “NOT”):

`>>> session.query(Address).\
...         filter(~Address.user.has(User.name=='jack')).all()
**SELECT** addresses.id **AS** addresses_id,
        addresses.email_address **AS** addresses_email_address,
        addresses.user_id **AS** addresses_user_id
**FROM** addresses
**WHERE** **NOT** (**EXISTS** (**SELECT** 1
**FROM** users
**WHERE** users.id = addresses.user_id **AND** users.name = ?))
('jack',)
[]`

### **Common Relationship Operators**

Here’s all the operators which build on relationships - each one is linked to its API documentation which includes full details on usage and behavior:

- [`Comparator.__eq__()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.__eq__) (many-to-one “equals” comparison):
    
    `query.filter(Address.user == someuser)`
    
- [`Comparator.__ne__()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.__ne__) (many-to-one “not equals” comparison):
    
    `query.filter(Address.user != someuser)`
    
- IS NULL (many-to-one comparison, also uses [`Comparator.__eq__()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.__eq__)):
    
    `query.filter(Address.user == **None**)`
    
- [`Comparator.contains()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.contains) (used for one-to-many collections):
    
    `query.filter(User.addresses.contains(someaddress))`
    
- [`Comparator.any()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.any) (used for collections):
    
    `query.filter(User.addresses.any(Address.email_address == 'bar'))
    
    *# also takes keyword arguments:*query.filter(User.addresses.any(email_address='bar'))`
    
- [`Comparator.has()`](https://docs.sqlalchemy.org/en/13/orm/internals.html#sqlalchemy.orm.RelationshipProperty.Comparator.has) (used for scalar references):
    
    `query.filter(Address.user.has(name='ed'))`
    
- [`Query.with_parent()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.with_parent) (used for any relationship):
    
    `session.query(Address).with_parent(someuser, 'addresses')`
    

## **Eager Loading**

Recall earlier that we illustrated a [lazy loading](https://docs.sqlalchemy.org/en/13/glossary.html#term-lazy-loading) operation, when we accessed the `User.addresses` collection of a `User` and SQL was emitted. If you want to reduce the number of queries (dramatically, in many cases), we can apply an [eager load](https://docs.sqlalchemy.org/en/13/glossary.html#term-eager-load) to the query operation. SQLAlchemy offers three types of eager loading, two of which are automatic, and a third which involves custom criterion. All three are usually invoked via functions known as query options which give additional instructions to the [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) on how we would like various attributes to be loaded, via the [`Query.options()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.options) method.

### **Selectin Load**

In this case we’d like to indicate that `User.addresses` should load eagerly. A good choice for loading a set of objects as well as their related collections is the [`selectinload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.selectinload) option, which emits a second SELECT statement that fully loads the collections associated with the results just loaded. The name “selectin” originates from the fact that the SELECT statement uses an IN clause in order to locate related rows for multiple objects at once:

`>>> **from** **sqlalchemy.orm** **import** selectinload
>>> jack = session.query(User).\
...                 options(selectinload(User.addresses)).\
...                 filter_by(name='jack').one()
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name = ?
('jack',)
**SELECT** addresses.user_id **AS** addresses_user_id,
        addresses.id **AS** addresses_id,
        addresses.email_address **AS** addresses_email_address
**FROM** addresses
**WHERE** addresses.user_id **IN** (?)
**ORDER** **BY** addresses.id
(5,)
>>> jack
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]`

### **Joined Load**

The other automatic eager loading function is more well known and is called [`joinedload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.joinedload). This style of loading emits a JOIN, by default a LEFT OUTER JOIN, so that the lead object as well as the related object or collection is loaded in one step. We illustrate loading the same `addresses` collection in this way - note that even though the `User.addresses` collection on `jack` is actually populated right now, the query will emit the extra join regardless:

`>>> **from** **sqlalchemy.orm** **import** joinedload

>>> jack = session.query(User).\
...                        options(joinedload(User.addresses)).\
...                        filter_by(name='jack').one()
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname,
        addresses_1.id **AS** addresses_1_id,
        addresses_1.email_address **AS** addresses_1_email_address,
        addresses_1.user_id **AS** addresses_1_user_id
**FROM** users
    **LEFT** **OUTER** **JOIN** addresses **AS** addresses_1 **ON** users.id = addresses_1.user_id
**WHERE** users.name = ? **ORDER** **BY** addresses_1.id
('jack',)
>>> jack
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>

>>> jack.addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]`

Note that even though the OUTER JOIN resulted in two rows, we still only got one instance of `User` back. This is because [`Query`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query) applies a “uniquing” strategy, based on object identity, to the returned entities. This is specifically so that joined eager loading can be applied without affecting the query results.

While [`joinedload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.joinedload) has been around for a long time, [`selectinload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.selectinload) is a newer form of eager loading. [`selectinload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.selectinload) tends to be more appropriate for loading related collections while [`joinedload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.joinedload) tends to be better suited for many-to-one relationships, due to the fact that only one row is loaded for both the lead and the related object. Another form of loading, [`subqueryload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.subqueryload), also exists, which can be used in place of [`selectinload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.selectinload) when making use of composite primary keys on certain backends.

**`joinedload()` is not a replacement for `join()`**
The join created by [`joinedload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.joinedload) is anonymously aliased such that it **does not affect the query results**. An [`Query.order_by()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.order_by) or [`Query.filter()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter) call **cannot** reference these aliased tables - so-called “user space” joins are constructed using [`Query.join()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.join). The rationale for this is that [`joinedload()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.joinedload) is only applied in order to affect how related objects or collections are loaded as an optimizing detail - it can be added or removed with no impact on actual results. See the section [The Zen of Joined Eager Loading](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#zen-of-eager-loading) for a detailed description of how this is used.

### **Explicit Join + Eagerload**

A third style of eager loading is when we are constructing a JOIN explicitly in order to locate the primary rows, and would like to additionally apply the extra table to a related object or collection on the primary object. This feature is supplied via the [`contains_eager()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.contains_eager) function, and is most typically useful for pre-loading the many-to-one object on a query that needs to filter on that same object. Below we illustrate loading an `Address` row as well as the related `User` object, filtering on the `User` named “jack” and using [`contains_eager()`](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html#sqlalchemy.orm.contains_eager) to apply the “user” columns to the `Address.user` attribute:

`>>> **from** **sqlalchemy.orm** **import** contains_eager
>>> jacks_addresses = session.query(Address).\
...                             join(Address.user).\
...                             filter(User.name=='jack').\
...                             options(contains_eager(Address.user)).\
...                             all()
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname,
        addresses.id **AS** addresses_id,
        addresses.email_address **AS** addresses_email_address,
        addresses.user_id **AS** addresses_user_id
**FROM** addresses **JOIN** users **ON** users.id = addresses.user_id
**WHERE** users.name = ?
('jack',)
>>> jacks_addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]

>>> jacks_addresses[0].user
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>`

For more information on eager loading, including how to configure various forms of loading by default, see the section [Relationship Loading Techniques](https://docs.sqlalchemy.org/en/13/orm/loading_relationships.html).

## **Deleting**

Let’s try to delete `jack` and see how that goes. We’ll mark the object as deleted in the session, then we’ll issue a `count` query to see that no rows remain:

`>>> session.delete(jack)
>>> session.query(User).filter_by(name='jack').count()
**UPDATE** addresses **SET** user_id=? **WHERE** addresses.id = ?
((**None**, 1), (**None**, 2))
**DELETE** **FROM** users **WHERE** users.id = ?
(5,)
**SELECT** **count**(*) **AS** count_1
**FROM** (**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name = ?) **AS** anon_1
('jack',)
0`

So far, so good. How about Jack’s `Address` objects ?

`>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
...  ).count()
**SELECT** **count**(*) **AS** count_1
**FROM** (**SELECT** addresses.id **AS** addresses_id,
                addresses.email_address **AS** addresses_email_address,
                addresses.user_id **AS** addresses_user_id
**FROM** addresses
**WHERE** addresses.email_address **IN** (?, ?)) **AS** anon_1
('jack@google.com', 'j25@yahoo.com')
2`

Uh oh, they’re still there ! Analyzing the flush SQL, we can see that the `user_id` column of each address was set to NULL, but the rows weren’t deleted. SQLAlchemy doesn’t assume that deletes cascade, you have to tell it to do so.

### **Configuring delete/delete-orphan Cascade**

We will configure **cascade** options on the `User.addresses` relationship to change the behavior. While SQLAlchemy allows you to add new attributes and relationships to mappings at any point in time, in this case the existing relationship needs to be removed, so we need to tear down the mappings completely and start again - we’ll close the [`Session`](https://docs.sqlalchemy.org/en/13/orm/session_api.html#sqlalchemy.orm.session.Session):

**`>>>** session.close()
ROLLBACK`

and use a new [`declarative_base()`](https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html#sqlalchemy.ext.declarative.declarative_base):

**`>>>** Base = declarative_base()`

Next we’ll declare the `User` class, adding in the `addresses` relationship including the cascade configuration (we’ll leave the constructor out too):

**`>>> class** **User**(Base):
**...**     __tablename__ = 'users'
**......**     id = Column(Integer, primary_key=**True**)
**...**     name = Column(String)
**...**     fullname = Column(String)
**...**     nickname = Column(String)
**......**     addresses = relationship("Address", back_populates='user',
**...**                     cascade="all, delete, delete-orphan")
**......**     **def** __repr__(self):
**...**        **return** "<User(name='*%s*', fullname='*%s*', nickname='*%s*')>" % (
**...**                                self.name, self.fullname, self.nickname)`

Then we recreate `Address`, noting that in this case we’ve created the `Address.user` relationship via the `User` class already:

**`>>> class** **Address**(Base):
**...**     __tablename__ = 'addresses'
**...**     id = Column(Integer, primary_key=**True**)
**...**     email_address = Column(String, nullable=**False**)
**...**     user_id = Column(Integer, ForeignKey('users.id'))
**...**     user = relationship("User", back_populates="addresses")
**......**     **def** __repr__(self):
**...**         **return** "<Address(email_address='*%s*')>" % self.email_address`

Now when we load the user `jack` (below using [`Query.get()`](https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.get), which loads by primary key), removing an address from the corresponding `addresses` collection will result in that `Address` being deleted:

`*# load Jack by primary key*>>> jack = session.query(User).get(5)
**BEGIN** (**implicit**)
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.id = ?
(5,)
*# remove one Address (lazy load fires off)*>>> **del** jack.addresses[1]
**SELECT** addresses.id **AS** addresses_id,
        addresses.email_address **AS** addresses_email_address,
        addresses.user_id **AS** addresses_user_id
**FROM** addresses
**WHERE** ? = addresses.user_id
(5,)
*# only one address remains*>>> session.query(Address).filter(
...     Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
**DELETE** **FROM** addresses **WHERE** addresses.id = ?
(2,)
**SELECT** **count**(*) **AS** count_1
**FROM** (**SELECT** addresses.id **AS** addresses_id,
                addresses.email_address **AS** addresses_email_address,
                addresses.user_id **AS** addresses_user_id
**FROM** addresses
**WHERE** addresses.email_address **IN** (?, ?)) **AS** anon_1
('jack@google.com', 'j25@yahoo.com')
1`

Deleting Jack will delete both Jack and the remaining `Address` associated with the user:

`>>> session.delete(jack)

>>> session.query(User).filter_by(name='jack').count()
**DELETE** **FROM** addresses **WHERE** addresses.id = ?
(1,)
**DELETE** **FROM** users **WHERE** users.id = ?
(5,)
**SELECT** **count**(*) **AS** count_1
**FROM** (**SELECT** users.id **AS** users_id,
                users.name **AS** users_name,
                users.fullname **AS** users_fullname,
                users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name = ?) **AS** anon_1
('jack',)
0

>>> session.query(Address).filter(
...    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
... ).count()
**SELECT** **count**(*) **AS** count_1
**FROM** (**SELECT** addresses.id **AS** addresses_id,
                addresses.email_address **AS** addresses_email_address,
                addresses.user_id **AS** addresses_user_id
**FROM** addresses
**WHERE** addresses.email_address **IN** (?, ?)) **AS** anon_1
('jack@google.com', 'j25@yahoo.com')
0`

**More on Cascades**
Further detail on configuration of cascades is at [Cascades](https://docs.sqlalchemy.org/en/13/orm/cascades.html#unitofwork-cascades). The cascade functionality can also integrate smoothly with the `ON DELETE CASCADE` functionality of the relational database. See [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/13/orm/cascades.html#passive-deletes) for details.

## **Building a Many To Many Relationship**

We’re moving into the bonus round here, but lets show off a many-to-many relationship. We’ll sneak in some other features too, just to take a tour. We’ll make our application a blog application, where users can write `BlogPost` items, which have `Keyword` items associated with them.

For a plain many-to-many, we need to create an un-mapped [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) construct to serve as the association table. This looks like the following:

**`>>> from** **sqlalchemy** **import** Table, Text
**>>>** *# association table***>>>** post_keywords = Table('post_keywords', Base.metadata,
**...**     Column('post_id', ForeignKey('posts.id'), primary_key=**True**),
**...**     Column('keyword_id', ForeignKey('keywords.id'), primary_key=**True**)
**...** )`

Above, we can see declaring a [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) directly is a little different than declaring a mapped class. [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) is a constructor function, so each individual [`Column`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column) argument is separated by a comma. The [`Column`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Column) object is also given its name explicitly, rather than it being taken from an assigned attribute name.

Next we define `BlogPost` and `Keyword`, using complementary [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) constructs, each referring to the `post_keywords` table as an association table:

**`>>> class** **BlogPost**(Base):
**...**     __tablename__ = 'posts'
**......**     id = Column(Integer, primary_key=**True**)
**...**     user_id = Column(Integer, ForeignKey('users.id'))
**...**     headline = Column(String(255), nullable=**False**)
**...**     body = Column(Text)
**......**     *# many to many BlogPost<->Keyword***...**     keywords = relationship('Keyword',
**...**                             secondary=post_keywords,
**...**                             back_populates='posts')
**......**     **def** __init__(self, headline, body, author):
**...**         self.author = author
**...**         self.headline = headline
**...**         self.body = body
**......**     **def** __repr__(self):
**...**         **return** "BlogPost(*%r*, *%r*, *%r*)" % (self.headline, self.body, self.author)

**>>> class** **Keyword**(Base):
**...**     __tablename__ = 'keywords'
**......**     id = Column(Integer, primary_key=**True**)
**...**     keyword = Column(String(50), nullable=**False**, unique=**True**)
**...**     posts = relationship('BlogPost',
**...**                          secondary=post_keywords,
**...**                          back_populates='keywords')
**......**     **def** __init__(self, keyword):
**...**         self.keyword = keyword`

**Note**

The above class declarations illustrate explicit `__init__()` methods. Remember, when using Declarative, it’s optional!

Above, the many-to-many relationship is `BlogPost.keywords`. The defining feature of a many-to-many relationship is the `secondary` keyword argument which references a [`Table`](https://docs.sqlalchemy.org/en/13/core/metadata.html#sqlalchemy.schema.Table) object representing the association table. This table only contains columns which reference the two sides of the relationship; if it has *any* other columns, such as its own primary key, or foreign keys to other tables, SQLAlchemy requires a different usage pattern called the “association object”, described at [Association Object](https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-pattern).

We would also like our `BlogPost` class to have an `author` field. We will add this as another bidirectional relationship, except one issue we’ll have is that a single user might have lots of blog posts. When we access `User.posts`, we’d like to be able to filter results further so as not to load the entire collection. For this we use a setting accepted by [`relationship()`](https://docs.sqlalchemy.org/en/13/orm/relationship_api.html#sqlalchemy.orm.relationship) called `lazy='dynamic'`, which configures an alternate **loader strategy** on the attribute:

`>>> BlogPost.author = relationship(User, back_populates="posts")
>>> User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")`

Create new tables:

`>>> Base.metadata.create_all(engine)
PRAGMA...
**CREATE** **TABLE** keywords (
    id INTEGER **NOT** **NULL**,
    keyword VARCHAR(50) **NOT** **NULL**,
    **PRIMARY** **KEY** (id),
    **UNIQUE** (keyword)
)
()
**COMMITCREATE** **TABLE** posts (
    id INTEGER **NOT** **NULL**,
    user_id INTEGER,
    headline VARCHAR(255) **NOT** **NULL**,
    body TEXT,
    **PRIMARY** **KEY** (id),
    **FOREIGN** **KEY**(user_id) **REFERENCES** users (id)
)
()
**COMMITCREATE** **TABLE** post_keywords (
    post_id INTEGER **NOT** **NULL**,
    keyword_id INTEGER **NOT** **NULL**,
    **PRIMARY** **KEY** (post_id, keyword_id),
    **FOREIGN** **KEY**(post_id) **REFERENCES** posts (id),
    **FOREIGN** **KEY**(keyword_id) **REFERENCES** keywords (id)
)
()
**COMMIT**`

Usage is not too different from what we’ve been doing. Let’s give Wendy some blog posts:

`>>> wendy = session.query(User).\
...                 filter_by(name='wendy').\
...                 one()
**SELECT** users.id **AS** users_id,
        users.name **AS** users_name,
        users.fullname **AS** users_fullname,
        users.nickname **AS** users_nickname
**FROM** users
**WHERE** users.name = ?
('wendy',)
>>> post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
>>> session.add(post)`

We’re storing keywords uniquely in the database, but we know that we don’t have any yet, so we can just create them:

`>>> post.keywords.append(Keyword('wendy'))
>>> post.keywords.append(Keyword('firstpost'))`

We can now look up all blog posts with the keyword ‘firstpost’. We’ll use the `any` operator to locate “blog posts where any of its keywords has the keyword string ‘firstpost’”:

`>>> session.query(BlogPost).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
**INSERT** **INTO** keywords (keyword) **VALUES** (?)
('wendy',)
**INSERT** **INTO** keywords (keyword) **VALUES** (?)
('firstpost',)
**INSERT** **INTO** posts (user_id, headline, body) **VALUES** (?, ?, ?)
(2, "Wendy's Blog Post", 'This is a test')
**INSERT** **INTO** post_keywords (post_id, keyword_id) **VALUES** (?, ?)
(...)
**SELECT** posts.id **AS** posts_id,
        posts.user_id **AS** posts_user_id,
        posts.headline **AS** posts_headline,
        posts.body **AS** posts_body
**FROM** posts
**WHERE** **EXISTS** (**SELECT** 1
    **FROM** post_keywords, keywords
    **WHERE** posts.id = post_keywords.post_id
        **AND** keywords.id = post_keywords.keyword_id
        **AND** keywords.keyword = ?)
('firstpost',)
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]`

If we want to look up posts owned by the user `wendy`, we can tell the query to narrow down to that `User` object as a parent:

`>>> session.query(BlogPost).\
...             filter(BlogPost.author==wendy).\
...             filter(BlogPost.keywords.any(keyword='firstpost')).\
...             all()
**SELECT** posts.id **AS** posts_id,
        posts.user_id **AS** posts_user_id,
        posts.headline **AS** posts_headline,
        posts.body **AS** posts_body
**FROM** posts
**WHERE** ? = posts.user_id **AND** (**EXISTS** (**SELECT** 1
    **FROM** post_keywords, keywords
    **WHERE** posts.id = post_keywords.post_id
        **AND** keywords.id = post_keywords.keyword_id
        **AND** keywords.keyword = ?))
(2, 'firstpost')
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]`

Or we can use Wendy’s own `posts` relationship, which is a “dynamic” relationship, to query straight from there:

`>>> wendy.posts.\
...         filter(BlogPost.keywords.any(keyword='firstpost')).\
...         all()
**SELECT** posts.id **AS** posts_id,
        posts.user_id **AS** posts_user_id,
        posts.headline **AS** posts_headline,
        posts.body **AS** posts_body
**FROM** posts
**WHERE** ? = posts.user_id **AND** (**EXISTS** (**SELECT** 1
    **FROM** post_keywords, keywords
    **WHERE** posts.id = post_keywords.post_id
        **AND** keywords.id = post_keywords.keyword_id
        **AND** keywords.keyword = ?))
(2, 'firstpost')
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]`

## **Further Reference**

Query Reference: [Query API](https://docs.sqlalchemy.org/en/13/orm/query.html)

Mapper Reference: [Mapper Configuration](https://docs.sqlalchemy.org/en/13/orm/mapper_config.html)

Relationship Reference: [Relationship Configuration](https://docs.sqlalchemy.org/en/13/orm/relationships.html)

Session Reference: [Using the Session](https://docs.sqlalchemy.org/en/13/orm/session.html)