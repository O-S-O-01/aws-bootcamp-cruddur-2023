# Week 3 — Decentralized Authentication

## Task Overview
This week focused on moving from mock authentication to a production-ready system using Amazon Cognito. I integrated the AWS Amplify SDK into the React frontend and refactored the UI to handle real user sessions. A major part of this week involved troubleshooting configuration mismatches between the AWS Console and the frontend code, as well as managing breaking changes in modern library versions.

## GENERAL TASKS COMPLETED
- [x] **Provisioned Amazon Cognito User Pool:** Created a User Pool and identified the need to disable the Client Secret for frontend compatibility.
- [x] **AWS Amplify Integration:** Installed `aws-amplify` and configured it in `App.js` using environment variables.
- [x] **Auth Logic Implementation:** Built out `checkAuth`, `signIn`, `signUp`, and `confirmSignUp` using the Amplify library.
- [x] **UI Refactoring:** Conditionally rendered components (Navigation, Sidebar) based on the `user` state.
- [x] **CLI User Management:** Used the AWS CLI to manually confirm users and set permanent passwords.

## TECHNICAL CHALLENGES AND PERSONAL SOLUTIONS

### Challenge 1: Cognito NotAuthorizedException (SECRET_HASH)
During login, I received an error stating `SECRET_HASH was not received`. This happened because the Cognito App Client was initially created with a "Client Secret."
- ***My Solution:*** I used the AWS Console to update the App Integration. I created a new App Client **without** a client secret, as React (a client-side framework) cannot securely store or send a secret hash.

### Challenge 2: Amplify v6 Breaking Changes
I encountered errors like `Auth is not exported from 'aws-amplify'` and `export 'Auth' was not found`. This was caused by `npm` installing the latest Amplify v6, while the bootcamp code relies on the v5 `Auth` class architecture.
- ***My Solution:*** I downgraded the library to a compatible version by running `npm install aws-amplify@5`. This restored the `Auth` object functionality without needing to refactor the entire frontend logic.

### Challenge 3: Scoping Issues with 'onsubmit'
In `SignupPage.js`, I hit a TypeScript/Linting error: `Cannot redeclare block-scoped variable 'onsubmit'`. This occurred because `onsubmit` is a reserved global property in the browser's window object.
- ***My Solution:*** I renamed the local function from `onsubmit` to a more specific name like `handleSubmit` or `setupSignUp` to avoid naming collisions with the global scope.

### Challenge 4: Bash Comment Interference in CLI
While running `aws cognito-idp admin-set-user-password`, my password contained a `#` character, which caused Bash to treat the rest of the command as a comment, leading to failed execution.
- ***My Solution:*** I wrapped the password string in single quotes (e.g., `'#Password123'`). This forced the shell to treat the `#` as a literal character rather than the start of a comment.

### Challenge 5: Docker Container Memory Limits (SIGTERM)
The frontend container would occasionally crash with a `SIGTERM` during `react-scripts start`, often due to high memory usage by Webpack within the restricted Docker/WSL environment.
- ***My Solution:*** Since the process eventually succeeded with a "Compiled successfully!" message, I monitored my system resources. I recognized this as a resource crunch and continued once the local server at port 3000 became stable.

### Challenge 6: X-Ray Timeout Errors
I saw `Sending segment batch failed ... Client.Timeout exceeded` in the logs.
- ***My Solution:*** I identified that the X-Ray daemon was having intermittent trouble reaching the AWS regional endpoint from my local network. Since this was for local development and didn't crash the app, I proceeded with the knowledge that this would be more stable once deployed to an AWS VPC.
