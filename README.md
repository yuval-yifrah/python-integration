# python-integration

this tool is here to help you manage resources in your aws account with a new awesome cli tool i created just for you!  
this tool is here to help you create new ec2/s3/route53  
manage the ec2:  
create, stop/start/terminate/list  
manage s3:  
create upload and list  
manage route53:  
create zone-name, create/upsert/delete records and list them  

this tool manages everything you created by a tag "CreatedBy" so you can see and list only the things you created from this tool!

This tool works only with your AWS user credentials (access key + secret key).
No IAM roles or profiles are required, but all actions are limited to the permissions of your user.
Make sure your AWS user has enough permissions for the resources you want to manage.

first you need:  
to run this python file, you will need to do a couple of things before.  
1. add the access key and secret key of your aws account to the environment variables  
   linux:  
   export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"  
   export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"  
   export AWS_DEFAULT_REGION="us-east-1"  
   
   this will save the variables for as long as the prompt is open. once its closed they will be deleted.  
   to add them forever do this:  
   add them to ~/.bashrc or ~/.zshrc save and run: source ~/.bashrc or source ~/.zshrc  
   
   cmd:  
   set AWS_ACCESS_KEY_ID "YOUR_ACCESS_KEY_ID"  
   set AWS_SECRET_ACCESS_KEY "YOUR_SECRET_ACCESS_KEY"  
   set AWS_DEFAULT_REGION="us-east-1"  

   this will save the variables for as long as the prompt is open. once its closed they will be deleted.  
   to add them forever do this:  
   open settings > environment variables > user variables > add them one by one and save  

   if you run this from pycharm, add them through the terminal:  
      export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"  
      export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"  
      export AWS_DEFAULT_REGION="us-east-1"  
   
2. install on your ec2 git,python3,boto3,click:  
      sudo yum install -y python3 python3-pip  
      pip3 install boto3 --user  
      sudo python3 -m pip install click
3. examples for how to run this awesome tool:
   in your gitbash run:  
   python3 integrative_project.py ec2 create amazon-linux t3.micro yuvalyhome yuvalySG subnet1
   python3 integrative_project.py route53 manage delete yuvaly.com www.yuvaly.com A 1.2.43.4
   python3 integrative_project.py s3 create private yuvalyprivate
   
   use --help after every word to see what you need to do next!

4. to delete your creations, you need to connect to the aws website and delete manually everything except the ec2 - which you can terminate from this tool   
   
   

