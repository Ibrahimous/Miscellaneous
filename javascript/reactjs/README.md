
# TODO

Reprendre ici : https://nextjs.org/learn/dashboard-app/creating-layouts-and-pages
et là : https://reactflow.dev/examples/overview
et là : https://chatgpt.com/c/7070a5db-b45b-4747-ae66-b7020059b7e9

FROM the following:
1. Send a React Flow workflow JSON to a golang route
2. Save it in MongoDB/Get it from MongoDB
3. Read it and adapt it to goflow engine

To save a workflow from React Flow to MongoDB and then read it in Golang, you'll follow these steps:

1. **Save the React Flow Workflow to MongoDB:**
   - Convert the React Flow workflow data to a format suitable for storage (typically JSON).
   - Use a backend service (e.g., Node.js/Express) to handle the API request to save the data to MongoDB.

2. **Read the Workflow from MongoDB in Golang:**
   - Create a Go service that connects to MongoDB and fetches the saved workflow data.

Here's a step-by-step guide:

### Step 1: Saving the React Flow Workflow to MongoDB

**Frontend (React Flow) Side:**

1. **Capture the workflow data in React Flow:**
   ```jsx
   // Assuming you have your React Flow data in a variable called `reactFlowData`
   const saveWorkflow = async () => {
       const response = await fetch('/api/save-workflow', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
           },
           body: JSON.stringify(reactFlowData),
       });
       if (response.ok) {
           console.log('Workflow saved successfully!');
       } else {
           console.error('Failed to save workflow.');
       }
   };
   ```

**Backend (Node.js/Express) Side:**

1. **Set up an Express server to handle saving the workflow:**

   ```javascript
   const express = require('express');
   const mongoose = require('mongoose');

   const app = express();
   app.use(express.json());

   mongoose.connect('mongodb://localhost:27017/workflows', {
       useNewUrlParser: true,
       useUnifiedTopology: true,
   });

   const workflowSchema = new mongoose.Schema({
       data: Object,
   });

   const Workflow = mongoose.model('Workflow', workflowSchema);

   app.post('/api/save-workflow', async (req, res) => {
       try {
           const workflow = new Workflow({ data: req.body });
           await workflow.save();
           res.status(200).send('Workflow saved successfully');
       } catch (error) {
           res.status(500).send('Failed to save workflow');
       }
   });

   app.listen(3000, () => {
       console.log('Server is running on port 3000');
   });
   ```

### Step 2: Reading the Workflow from MongoDB in Golang

1. **Set up a Go application to connect to MongoDB:**

   ```go
   package main

   import (
       "context"
       "fmt"
       "log"
       "go.mongodb.org/mongo-driver/bson"
       "go.mongodb.org/mongo-driver/mongo"
       "go.mongodb.org/mongo-driver/mongo/options"
   )

   func main() {
       clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
       client, err := mongo.Connect(context.TODO(), clientOptions)
       if err != nil {
           log.Fatal(err)
       }
       defer func() {
           if err = client.Disconnect(context.TODO()); err != nil {
               log.Fatal(err)
           }
       }()

       collection := client.Database("workflows").Collection("workflows")

       var result bson.M
       err = collection.FindOne(context.TODO(), bson.D{}).Decode(&result)
       if err != nil {
           log.Fatal(err)
       }

       fmt.Println(result)
   }
   ```

This code connects to the MongoDB instance, fetches a single document from the `workflows` collection, and prints it out.

### Summary

1. **React Flow Frontend**:
   - Send the workflow data to a backend API.
2. **Node.js/Express Backend**:
   - Save the workflow data in MongoDB.
3. **Golang Application**:
   - Connect to MongoDB and read the workflow data.

You may need to adjust the database schema, error handling, and connection strings according to your specific requirements and environment.