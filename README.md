A serverless email summary bot runs on AWS Lambda and is triggered daily at 10 AM Brussels time by an EventBridge schedule 
AWS Documentation
AWS Documentation
.

It authenticates with Gmail via OAuth2 to fetch messages received between midnight and 10 AM Brussels time 
Google for Developers
.

Emails are classified into Personal, Marketing, or Important and summarized using OpenAI’s GPT-4 Chat Completions API 
Medium
.

The generated summary is sent back to you as an email through the Gmail API’s send endpoint 
Stack Overflow
.

The code is organized into separate Python modules for Gmail interactions, OpenAI calls, and the Lambda handler 
GitHub
.

All modules and dependencies are packaged into a single deployment.zip for upload via the Lambda console, enabling seamless serverless operation 
AWS Documentation
.
