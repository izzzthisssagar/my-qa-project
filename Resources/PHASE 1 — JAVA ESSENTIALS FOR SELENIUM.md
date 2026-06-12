\================================================================  
PHASE 1 — JAVA ESSENTIALS FOR SELENIUM  
Days 1–7 | 2 Hours/Day  
\================================================================

\----------------------------------------------------------------  
DAY 1 — Java Setup \+ Variables & Data Types  
\----------------------------------------------------------------  
GOAL: Get Java running on your machine and understand  
      how data is stored in programs.

\--- HOUR 1: SETUP \---

What to install:  
  1\. JDK 17+ → https://adoptium.net (Temurin build, free)  
  2\. IntelliJ IDEA Community → https://jetbrains.com/idea (free)  
  3\. After install, open IntelliJ → New Project → Java  
     → SDK: select your JDK → name it "JavaSeleniumPrep"

Verify install works:  
  Open terminal and type:  
    java \-version  
    javac \-version  
  Both should print version numbers. If not, fix PATH first.

\--- HOUR 2: VARIABLES & DATA TYPES \---

Core concept: Variables are containers that hold data.  
Java is strictly typed — you must say what type of  
data a variable holds before using it.

Primitive Data Types (memorize these 4 for Selenium):  
  int     → whole numbers       → int age \= 25;  
  double  → decimal numbers     → double price \= 9.99;  
  boolean → true or false       → boolean isLoggedIn \= true;  
  String  → text (not primitive  
            but used like one)  → String username \= "sagar";

Practice Task (type this yourself, don't copy-paste):

  public class Day1Practice {  
      public static void main(String\[\] args) {

          // User info variables  
          String name \= "Sagar";  
          int age \= 22;  
          double salary \= 25000.50;  
          boolean isStudent \= true;

          // Print them  
          System.out.println("Name: " \+ name);  
          System.out.println("Age: " \+ age);  
          System.out.println("Salary: " \+ salary);  
          System.out.println("Is Student: " \+ isStudent);  
      }  
  }

Expected Output:  
  Name: Sagar  
  Age: 22  
  Salary: 25000.5  
  Is Student: true

Key rule: Every Java program starts from main() method.  
          Without it, nothing runs.

Common Mistakes Today:  
  \- Forgetting semicolon at end of lines  
  \- Writing String with lowercase 's' (it's capital S)  
  \- Not selecting the right JDK in IntelliJ project setup

Resources:  
  \- Kunal Kushwaha Java playlist (YouTube) — Episode 1 & 2  
  \- W3Schools Java → https://w3schools.com/java (quick reference)

End of Day Checklist:  
  \[ \] IntelliJ installed and project created  
  \[ \] java \-version works in terminal  
  \[ \] Day1Practice.java runs without errors  
  \[ \] Understand what int, String, boolean, double do

\----------------------------------------------------------------  
DAY 2 — Conditions & Loops  
\----------------------------------------------------------------  
GOAL: Make your code make decisions and repeat tasks.  
      In Selenium, loops are used to handle lists of  
      elements. Conditions are used everywhere.

\--- HOUR 1: CONDITIONS \---

if / else if / else:

  int score \= 75;

  if (score \>= 80\) {  
      System.out.println("Pass with Distinction");  
  } else if (score \>= 50\) {  
      System.out.println("Pass");  
  } else {  
      System.out.println("Fail");  
  }

Comparison operators:  
  \==   equals  
  \!=   not equals  
  \>    greater than  
  \<    less than  
  \>=   greater than or equal  
  \<=   less than or equal

Logical operators:  
  &&   AND  (both must be true)  
  ||   OR   (at least one true)  
  \!    NOT  (reverses condition)

\--- HOUR 2: LOOPS \---

for loop (when you know count):

  for (int i \= 1; i \<= 5; i++) {  
      System.out.println("Day: " \+ i);  
  }

while loop (when you don't know count):

  int count \= 0;  
  while (count \< 3\) {  
      System.out.println("Attempt: " \+ count);  
      count++;  
  }

Practice Task:

  public class Day2Practice {  
      public static void main(String\[\] args) {

          // Print numbers 1-10  
          // Mark even numbers as EVEN, odd as ODD  
          for (int i \= 1; i \<= 10; i++) {  
              if (i % 2 \== 0\) {  
                  System.out.println(i \+ " \- EVEN");  
              } else {  
                  System.out.println(i \+ " \- ODD");  
              }  
          }  
      }  
  }

Expected Output:  
  1 \- ODD  
  2 \- EVEN  
  3 \- ODD  
  4 \- EVEN  
  ... and so on until 10

Common Mistakes Today:  
  \- Using \= instead of \== in conditions (= assigns, \== compares)  
  \- Infinite loop: forgetting to increment i in while loop  
  \- Off-by-one: i \<= 10 vs i \< 10 (one includes 10, other doesn't)

End of Day Checklist:  
  \[ \] if/else works correctly in your code  
  \[ \] for loop runs and prints expected output  
  \[ \] You understand what i++ does  
  \[ \] Practice task completed with correct output

\----------------------------------------------------------------  
DAY 3 — Methods & Arrays  
\----------------------------------------------------------------  
GOAL: Organize code into reusable blocks (methods).  
      Store multiple values in one place (arrays).  
      In Selenium, methods \= every action you automate.

\--- HOUR 1: METHODS \---

A method is a named block of code you can call  
multiple times. Structure:

  returnType methodName(parameters) {  
      // code  
      return value; // only if returnType is not void  
  }

Examples:

  // Method that returns nothing (void)  
  public static void greetUser(String name) {  
      System.out.println("Hello, " \+ name);  
  }

  // Method that returns a value  
  public static int addNumbers(int a, int b) {  
      return a \+ b;  
  }

  // Calling the methods  
  public static void main(String\[\] args) {  
      greetUser("Sagar");  
      int result \= addNumbers(10, 20);  
      System.out.println("Sum: " \+ result);  
  }

\--- HOUR 2: ARRAYS \---

Array \= fixed-size collection of same type elements.  
Index always starts at 0 (not 1).

  // Declare and initialize  
  String\[\] browsers \= {"Chrome", "Firefox", "Edge"};

  // Access by index  
  System.out.println(browsers\[0\]); // Chrome  
  System.out.println(browsers\[2\]); // Edge

  // Loop through array  
  for (int i \= 0; i \< browsers.length; i++) {  
      System.out.println("Browser: " \+ browsers\[i\]);  
  }

  // Enhanced for loop (cleaner)  
  for (String browser : browsers) {  
      System.out.println("Browser: " \+ browser);  
  }

Practice Task:

  public class Day3Practice {

      public static void printBrowsers(String\[\] list) {  
          for (String b : list) {  
              System.out.println("Testing on: " \+ b);  
          }  
      }

      public static int countBrowsers(String\[\] list) {  
          return list.length;  
      }

      public static void main(String\[\] args) {  
          String\[\] browsers \= {"Chrome", "Firefox", "Edge"};  
          printBrowsers(browsers);  
          System.out.println("Total: " \+ countBrowsers(browsers));  
      }  
  }

Common Mistakes Today:  
  \- Accessing index that doesn't exist → ArrayIndexOutOfBoundsException  
  \- Forgetting static keyword on methods (causes compile error in main)  
  \- Using wrong return type (saying void but trying to return a value)

End of Day Checklist:  
  \[ \] Can write a method with and without return value  
  \[ \] Can loop through an array both ways (index \+ enhanced)  
  \[ \] Practice task runs correctly  
  \[ \] Understand what .length does on arrays

\----------------------------------------------------------------  
DAY 4 — OOP — Classes & Objects  
\----------------------------------------------------------------  
GOAL: Understand how Java organizes code into objects.  
      This is the foundation of POM (Page Object Model)  
      which you'll use in Phase 3\.

\--- HOUR 1: CLASSES & OBJECTS \---

Class \= Blueprint  
Object \= Actual thing created from that blueprint

Think of it like:  
  Class  → Car design on paper  
  Object → Actual car you drive

Structure:

  // Class definition  
  public class User {

      // Fields (attributes)  
      String username;  
      String password;  
      boolean isLoggedIn;

      // Constructor (runs when object is created)  
      public User(String username, String password) {  
          this.username \= username;  
          this.password \= password;  
          this.isLoggedIn \= false;  
      }

      // Method (behaviour)  
      public void login() {  
          this.isLoggedIn \= true;  
          System.out.println(username \+ " logged in.");  
      }

      public void logout() {  
          this.isLoggedIn \= false;  
          System.out.println(username \+ " logged out.");  
      }  
  }

  // Using the class (in main)  
  public class Day4Practice {  
      public static void main(String\[\] args) {

          // Creating objects  
          User user1 \= new User("sagar", "pass123");  
          User user2 \= new User("admin", "admin@99");

          user1.login();  
          user2.login();  
          user1.logout();

          System.out.println(user2.username \+ " status: "  
                             \+ user2.isLoggedIn);  
      }  
  }

Expected Output:  
  sagar logged in.  
  admin logged in.  
  sagar logged out.  
  admin status: true

\--- HOUR 2: WHY THIS MATTERS FOR SELENIUM \---

In Selenium with POM, every web page becomes a class:

  public class LoginPage {  
      // Web elements are fields  
      // Actions (click, type) are methods  
  }

You are already writing POM-style code  
even before touching Selenium. That's the point.

Key Concepts to Know:  
  this.   → refers to current object's field  
  new     → creates a new object from a class  
  Constructor → method with same name as class, no return type

Common Mistakes Today:  
  \- Forgetting new keyword when creating objects  
  \- Constructor name different from class name  
  \- Confusing class fields with local variables

End of Day Checklist:  
  \[ \] Can write a class with fields \+ constructor \+ methods  
  \[ \] Created at least 2 objects from same class  
  \[ \] Understand why POM uses classes  
  \[ \] Practice task runs without errors

\----------------------------------------------------------------  
DAY 5 — Inheritance & Interfaces  
\----------------------------------------------------------------  
GOAL: Reuse code across classes. In Selenium frameworks,  
      BaseClass inherits into all test classes.  
      This is exactly how your framework will be structured.

\--- HOUR 1: INHERITANCE \---

Inheritance \= Child class gets all features of parent class.  
Keyword: extends

  // Parent class  
  public class Animal {  
      String name;

      public Animal(String name) {  
          this.name \= name;  
      }

      public void eat() {  
          System.out.println(name \+ " is eating.");  
      }  
  }

  // Child class  
  public class Dog extends Animal {

      public Dog(String name) {  
          super(name); // calls parent constructor  
      }

      public void bark() {  
          System.out.println(name \+ " says: Woof\!");  
      }  
  }

  // Main  
  Dog d \= new Dog("Bruno");  
  d.eat();   // inherited from Animal  
  d.bark();  // Dog's own method

super keyword: used to call parent class constructor or method.

\--- HOUR 2: INTERFACES \---

Interface \= A contract. Defines what a class MUST do,  
not how it does it.  
Keyword: implements

  public interface Testable {  
      void runTest();  
      void generateReport();  
  }

  public class LoginTest implements Testable {

      public void runTest() {  
          System.out.println("Running Login Test...");  
      }

      public void generateReport() {  
          System.out.println("Report generated.");  
      }  
  }

Selenium Framework Connection:  
  Your BaseTest class (parent) will hold:  
  \- WebDriver setup  
  \- Browser open/close methods

  All test classes will extend BaseTest:  
  public class LoginTest extends BaseTest { ... }

  This means every test class automatically gets  
  browser setup without repeating code.

Common Mistakes Today:  
  \- Forgetting super() in child constructor  
  \- Implementing interface but not writing all its methods  
  \- Calling parent method that doesn't exist

End of Day Checklist:  
  \[ \] Can write parent \+ child class with extends  
  \[ \] Understand what super() does  
  \[ \] Can write a simple interface and implement it  
  \[ \] Can explain why BaseTest class uses inheritance

\----------------------------------------------------------------  
DAY 6 — Collections (List & HashMap)  
\----------------------------------------------------------------  
GOAL: Work with dynamic data. In Selenium, you'll  
      use Lists to handle multiple web elements at once.

\--- HOUR 1: LIST \---

List \= Dynamic array, can grow/shrink.  
Most used: ArrayList

  import java.util.ArrayList;  
  import java.util.List;

  List\<String\> testCases \= new ArrayList\<\>();

  // Add items  
  testCases.add("Login Test");  
  testCases.add("Logout Test");  
  testCases.add("Register Test");

  // Access by index  
  System.out.println(testCases.get(0)); // Login Test

  // Size  
  System.out.println("Total: " \+ testCases.size());

  // Loop  
  for (String tc : testCases) {  
      System.out.println("Executing: " \+ tc);  
  }

  // Remove  
  testCases.remove("Logout Test");

  // Check if exists  
  System.out.println(testCases.contains("Login Test")); // true

Selenium Usage:  
  List\<WebElement\> links \= driver.findElements(By.tagName("a"));  
  // returns all \<a\> tags on page as a List  
  System.out.println("Total links: " \+ links.size());

\--- HOUR 2: HASHMAP \---

HashMap \= Key-Value pairs. Like a dictionary.  
Store data with a label.

  import java.util.HashMap;

  HashMap\<String, String\> userCredentials \= new HashMap\<\>();

  userCredentials.put("username", "sagar\_qa");  
  userCredentials.put("password", "test@123");  
  userCredentials.put("role", "admin");

  // Access by key  
  System.out.println(userCredentials.get("username"));

  // Loop through  
  for (String key : userCredentials.keySet()) {  
      System.out.println(key \+ " → " \+ userCredentials.get(key));  
  }

Practice Task:

  // Store 3 test cases with their expected results  
  // Print each test name and whether it should PASS or FAIL

  HashMap\<String, String\> results \= new HashMap\<\>();  
  results.put("Login with valid creds", "PASS");  
  results.put("Login with wrong password", "FAIL");  
  results.put("Login with empty fields", "FAIL");

  for (String test : results.keySet()) {  
      System.out.println(test \+ " → " \+ results.get(test));  
  }

Common Mistakes Today:  
  \- Using \[\] to access List (that's arrays, not List)  
  \- Forgetting import statements at the top  
  \- Using get() on HashMap with wrong key (returns null)

End of Day Checklist:  
  \[ \] Can create and loop through ArrayList  
  \[ \] Can create and access HashMap values  
  \[ \] Practice task runs correctly  
  \[ \] Understand how List connects to Selenium's findElements

\----------------------------------------------------------------  
DAY 7 — Exception Handling  
\----------------------------------------------------------------  
GOAL: Handle errors gracefully so your program doesn't  
      crash. In Selenium this is critical — elements  
      not found, timeouts, stale elements all throw  
      exceptions.

\--- HOUR 1: TRY-CATCH \---

Exception \= Runtime error that crashes your program.  
try-catch \= you catch the crash and handle it cleanly.

  public class Day7Practice {  
      public static void main(String\[\] args) {

          try {  
              int result \= 10 / 0; // This will crash  
              System.out.println(result);  
          } catch (ArithmeticException e) {  
              System.out.println("Error: Cannot divide by zero");  
              System.out.println("Details: " \+ e.getMessage());  
          } finally {  
              System.out.println("This always runs.");  
          }  
      }  
  }

Output:  
  Error: Cannot divide by zero  
  Details: / by zero  
  This always runs.

finally block: runs NO MATTER WHAT.  
In Selenium → driver.quit() goes here so browser  
always closes even if test fails.

\--- HOUR 2: COMMON SELENIUM EXCEPTIONS \---

Learn these NOW so they don't surprise you later:

NoSuchElementException  
  → Element not found on page  
  → Fix: Check locator, add wait

ElementNotInteractableException  
  → Element exists but can't be clicked  
  → Fix: Scroll to element or wait for it

StaleElementReferenceException  
  → Element was found but page refreshed  
  → Fix: Find element again

TimeoutException  
  → Explicit wait ran out of time  
  → Fix: Increase timeout or fix locator

WebDriverException  
  → General driver issue (browser crash, driver mismatch)  
  → Fix: Check ChromeDriver version matches Chrome

How to handle in Selenium:

  try {  
      WebElement btn \= driver.findElement(By.id("submit"));  
      btn.click();  
  } catch (NoSuchElementException e) {  
      System.out.println("Submit button not found: "  
                         \+ e.getMessage());  
  } finally {  
      driver.quit();  
  }

Practice Task:

  // Simulate a login attempt  
  // If username is empty, throw an exception and catch it

  public static void login(String username, String password) {  
      try {  
          if (username.isEmpty()) {  
              throw new IllegalArgumentException(  
                  "Username cannot be empty"  
              );  
          }  
          System.out.println("Login successful for: " \+ username);  
      } catch (IllegalArgumentException e) {  
          System.out.println("Login failed: " \+ e.getMessage());  
      } finally {  
          System.out.println("Login attempt finished.");  
      }  
  }

  public static void main(String\[\] args) {  
      login("sagar", "pass123");  
      login("", "pass123");  
  }

Common Mistakes Today:  
  \- Empty catch block (catches error but does nothing, hides bugs)  
  \- Catching Exception (too broad, catches everything)  
  \- Forgetting finally when driver.quit() is needed

End of Day Checklist:  
  \[ \] Can write try-catch-finally correctly  
  \[ \] Know at least 4 common Selenium exceptions by name  
  \[ \] Practice task runs and handles both login cases  
  \[ \] Understand why finally is critical for Selenium cleanup

\================================================================  
JAVA PHASE COMPLETE — END OF DAY 7 SUMMARY  
\================================================================

What you now know:  
  Day 1 → Variables & Data Types (storing data)  
  Day 2 → Conditions & Loops (logic \+ repetition)  
  Day 3 → Methods & Arrays (reuse \+ multiple values)  
  Day 4 → Classes & Objects (the core of POM)  
  Day 5 → Inheritance & Interfaces (BaseTest structure)  
  Day 6 → Collections (handling multiple elements)  
  Day 7 → Exception Handling (test stability)

What comes next (Day 8):  
  Mini project — Build a Simple Calculator in Java  
  that uses ALL concepts above together.  
  Then Day 9 → Selenium starts.

\================================================================  
