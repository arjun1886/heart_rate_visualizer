# Heart Rate Visualizer

## Application Overview:

The user sees a web page on the browser to upload a csv file of heart rate data.

After uploading the file the user receives a line chart of heart rate data as if it’s being tracked in real time at 1 second intervals.

There is an anomaly detection field that is populated in case there are sudden spikes, drops or missing heart rates in the data.

## Architecture Overview:

The front end is designed using vanilla javascript, html, css.

Data is sent as a json through an API call to the backend, written in Python and using Flask to create WebSockets and serve API requests.

The data is deserialised and persisted to a local MySQL server (can be used later for data analysis, providing insights to the user).

It is also sent to Kafka - a message streaming platform implementing a publisher-subscriber model, in this case used as a queue to receive heart rate data 1 row at a time. This is done using a producer.

A subscriber reads this data from Kafka and creates a list of heart rate records.

This data is sent back to the front end at a rate of 1 row per second. This is done using a web socket connection between the front end and the backend. 

Web sockets are used when streaming data in real time between the client and the server where the network connection needs to be open for the duration of the data streaming period. 

## System Design:

### Front end :

Front end is fairly simple with an index.html file that contains html code to serve the web page.   The static files are contained in style.css (styling the web page is handled here) for app.js (front-end logic and client connections are handled here).

Each of these are hosted through a web server using Flask.

### Back end :

The back end is implemented using the CLEAN architecture.  The software is organised in layers of concentric circles where the inner layer has no idea about how the outer layer works, this leads to easier maintenance of code base when it gets large and separation of concerns becomes important. For eg, if you use a MySQL DB and later change to a NoSQL DB like MongoDB, most of the code remains the same and needs to be changed only at 1 layer.

The layers are as follows from innermost to outermost:  Entities, Handler, Use-Case, Repository

#### Entities :  

At the innermost layer, these are the business objects or domain models that contain the most general business rules. They are independent of any external technology or frameworks. For eg, the error object in my code does not depend on the application itself. Entity layer consists of error.py  

#### Handler : 

Contains external interfaces, in our case it enables communication between the front end and the backend by creating a controller that handles HTTP requests and web socket connections and calls the heart rate related use case methods. The controller adapts the request data to the format needed by the use case. Handler layer consists of app.py (Usually created within the handler folder but in this case is at root directory for simplicity).  

#### Use-Case : 

Contains the use cases or application services, which define the actions that can be performed within the system. They orchestrate the flow of data between entities and external layers, implementing specific business processes. In this application it has methods to handle the business logic to handle the heart rate data. This layer is represented by heart_processor.py.

#### Repository : 

The outermost layer includes the frameworks and tools like databases, queues etc. These are considered details that can change without affecting the business logic. In our case it consists of code that interacts with MySQL and Kafka. This layer is represented by my_sql.py, subscriber.py, producer.py.  

#### Anomaly detection logic : 

The logic is very simple where, if data is missing, the previous data value is used for the heart_rate, sudden spikes and dropped are configured as a delta of 30 bpm (an arbitrary choice), the anomaly field is populated accordingly to show the user.  

#### Additional Info :  

I decided to use Kafka which makes the system more complex, instead of just taking the rows of data and sending it through the web socket at 1 second intervals. The reason I did this was to show how to use stream processing technology since it would be important in the real world. I have focused more on the overall architecture and code organisation since that would be more developer dependent and more important in the context of building a large system. The anomaly detection section is something that can be leveraged through a 3rd party tech integration and hence I implemented something rudimentary.


 
