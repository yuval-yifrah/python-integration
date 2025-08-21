# python-integration

to run this python file, you will need to do a couple of things before.  
1. add the access key and secret key of your aws account to the environment variables  
   linux:  
   export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"  
   export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"  
   export AWS_DEFAULT_REGION="us-east-1"  
   
   this will save the variables for as long as the prompt is open. once its closed they will be deleted.  
   to add them forever do this:  
   adde them to ~/.bashrc or ~/.zshrc save and run: source ~/.bashrc or source ~/.zshrc  
   
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
   

