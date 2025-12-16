# Use the official AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Set working directory inside container
WORKDIR /var/task

# Install Python packages manually
RUN pip3 install --no-cache-dir psycopg2-binary python-dotenv

# Copy the Lambda function code
COPY authorizer.py .

# Copy the .env file (database credentials)
COPY database.env .

# Command to run Lambda function
CMD ["authorizer.lambda_handler"]
