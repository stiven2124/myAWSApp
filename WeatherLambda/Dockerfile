FROM public.ecr.aws/lambda/python:3.14

COPY weather.py ${LAMBDA_TASK_ROOT}/

RUN pip install requests

CMD ["weather.lambda_handler"]
