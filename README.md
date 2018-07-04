# Digital Voice Assistant with Alexa AWS Lambda and AWS Dynamodb

Step 1 – Create an AWS Account
1.  Open aws.amazon.com and click on ‘Complete Sign Up’. If you already have an account, continue to the next step.
 
a.	Follow the instructions. You may be asked to create an IAM (Identity and Access Management) role, you can ignore it for now as we will be doing this in a later step.
b.	You will need a valid Credit Card to set up your account (note the AWS Free Tier will suffice. You can find out more about the free tier here.)
c.	The sign-up process involves receiving a phone call and entering a PIN using your phone's keypad.
2. Sign into the AWS Console 
It can sometimes take a couple minutes for your new AWS account to become active. You will receive an e-mail when your account is active.
Step 2 – Create a Lambda Function
1.	AWS Lambda lets you run code without provisioning or managing servers. You pay only for the compute time you consume - there is no charge when your code is not running. With Lambda, you can run code for virtually any type of application or backend service - all with zero administration. Just upload your code and Lambda takes care of everything required to run and scale your code with high availability.
2.	IMPORTANT: Select US East (N. Virginia) region (upper right). This is the only region that currently supports Alexa skill development. If you do not select the correct region, it will not work.






3.	Search “Lambda” Under Amazon services (upper left)

 

4.	Click on Create Function. 

 










5.	Select on “Blueprints” if you want to use the preconfigured template. Or select “Author from scratch” if you want to create function from scratch. 

 

6.	If you are selecting “Blueprints” so there is readymade library you can use to create Alexa skill. Search with “Alexa” it will shows no of functions and select “alexa-skills-kit-color-expert-python”
   








7.	Enter the Name of your skill, from Role drop down select “Create custom role”. It will open new tab 

 





















8.	Accept the defaults to create a new IAM Role with a role name of ‘lambda_basic_execution’. Select "Allow" in the lower right corner and you will be returned to your Lambda function. 

 
9.	Add alexa skill kit in this function, Click on “Alexa Skills Kit”. 

 


Step 3 – Create amazon developer account, to create Your Alexa Skill in the Developer Portal
1.	Create developer account in amazon account. https://developer.amazon.com/ or sign in if it already exist. 
2.	Click on amazon alexa 

 
3.	Mouse over to Alexa Skills Kit 

 

4.	Click on “Start a Skill”

 


5.	Enter Skill name in “Skill Name”, Select a language from the drop down for which you want to create skill, (change default language according to region)
Choose a model for your skill 

 























6.	Click on Invocation, Add skill name in “Skill Invocation Name”. 
“Users say a skill's invocation name to begin an interaction with a particular custom skill.
For example, if the invocation name is "daily horoscopes", users can say”. “Give me my daily horoscope” 
After adding Invocation name Click on “Save Model”.

 


7.	Add Intent Name by click on “+ Add Intent”, There will be default 4 created Intent. 
Here we will create 2 Intent, In Intent “VisitorNameIsIntent” user will tell to alexa about his/her name. In Intent “EmpNameIsIntent” user will ask to alexa to whom he/her want to meet in office.
 
8.	The next step is to build the list of Sample Utterances. Given the flexibility and variation of spoken language in the real world, there will often be many different ways to express the same request. Providing these different phrases in your sample utterances will help improve voice recognition for the abilities you add to Alexa. It is important to include as wide a range of representative samples as you can – all the phrases that you can think of that are possible (though do not include samples that users will never speak). Alexa also attempts to generalize based on the samples you provide to interpret spoken phrases that differ in minor ways from the samples specified.


 














9.	Create Slot “Visitor” under “VisitorNameIsIntent” and slot “Emp” under “EmpNameIsIntent”.
 
10.	Create Slot Type “Employee” for both the slots.

 

11.	Add Values in SLOT

 

Step 4 – Link your Skill with Lambda Function
1.	Copy Skill Id from developer.amazon under “Endpoint -> Your Skill ID”.

 

2.	Paste Skill ID in configuration of Lambda function. 
 

3.	Copy this ARN of Lambda Function    
          
 











4.	Go to the developer.amazon and paste this ARN under “Endpoint -> Default Region”.

 

Step 5 – Configure DynamoDB
1.	Click on DynamoDB.
 









2.	Create table and add primary key name.
 
3.	It will look like as below 
 






4.	Add data in table 
 
5.	View the added data in table.

 
Step 6 – Save and Build your Skill
1.	Click on Invocation -> Click on “Save Model” -> Click on “Build Model”, Wait till you get success message that “Build Successful.”
2.	Click on Test, here you can test the Application.














