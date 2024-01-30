# Python - More Classes and Objects
### **Object-Oriented Programming (OOP):**

Object-Oriented Programming is a programming paradigm that uses objects – instances of classes – to design and organize code. The key concepts include:

- **Class:** A blueprint for creating objects, defining attributes and behaviors.
- **Object:** An instance of a class, representing a specific entity.
- **Encapsulation:** Bundling data and methods that operate on the data within a single unit (class).
- **Inheritance:** A mechanism for creating a new class by deriving properties and behaviors from an existing class.
- **Polymorphism:** The ability of a class to take on multiple forms, allowing objects of different classes to be treated as objects of a common base class.

### **"First-Class Everything":**

In Python, everything is an object, and objects can be assigned to variables, passed as arguments, and returned from functions. Functions are also first-class citizens, allowing them to be treated like any other variable.

### **Class and Object:**

- **Class:** A blueprint for creating objects. It defines attributes and methods.
- **Object:** An instance of a class. It represents a specific occurrence of the class.

### **Attribute:**

An attribute is a characteristic or property that describes an object. In Python classes, attributes are defined within the class and represent data associated with instances of the class.

### **Public, Protected, and Private Attributes:**

- **Public Attributes:** Accessible from outside the class.
- **Protected Attributes (Convention):** Accessible within the class and its subclasses.
- **Private Attributes (Convention):** Accessible only within the class.

### **Self:**

**`self`** is a convention in Python used as the first parameter in instance methods, referring to the instance of the class. It allows access to the instance's attributes and methods.

### **Method:**

A method is a function defined within a class that operates on instances of the class.

### **Special `__init__` Method:**

**`__init__`** is a special method in Python classes used for initializing object attributes when an instance is created.

### **Data Abstraction, Data Encapsulation, and Information Hiding:**

- **Data Abstraction:** Representing essential features without including the background details.
- **Data Encapsulation:** Bundling the data and the methods that operate on the data within a single unit (class).
- **Information Hiding:** Restricting access to some of an object's components.

### **Property:**

A property is a special attribute with getter, setter, and deleter methods, allowing controlled access to an attribute.

### **Difference Between Attribute and Property:**

- An attribute is a data item that describes an object.
- A property is a special attribute that controls access to another attribute.

### **Getters and Setters:**

In Python, getters and setters are achieved using the **`@property`** decorator and setter method.

### **Special `__str__` and `__repr__` Methods:**

- **`__str__`**: Called by **`str()`** and **`print()`** to display a user-friendly string representation.
- **`__repr__`**: Called by **`repr()`** to generate an unambiguous string representation.

### **Class Attribute:**

A class attribute is shared by all instances of a class. It is defined within the class but outside any methods.

### **Object Attribute vs. Class Attribute:**

- An object attribute is specific to an instance.
- A class attribute is shared among all instances of the class.

### **Class Method and Static Method:**

- **Class Method:** A method bound to the class rather than an instance. Defined using the **`@classmethod`** decorator.
- **Static Method:** A method that belongs to a class but does not access or modify class or instance state. Defined using the **`@staticmethod`** decorator.

### **Dynamically Creating Attributes:**

New attributes can be dynamically created for instances and classes using assignment.

### **`__dict__` Attribute:**

- **`__dict__`** of a class contains a dictionary storing the class's namespace.
- **`__dict__`** of an instance contains a dictionary storing the instance's attributes.

### **Attribute Access in Python:**

Python uses a chain of attribute access: instance attributes, class attributes, and attributes inherited from parent classes.

### **Using `getattr` Function:**

**`getattr(object, name)`** is a built-in function that returns the value of a named attribute of an object. It allows dynamic attribute access.