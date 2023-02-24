FROM public.ecr.aws/lambda/python:3.9

COPY Lambda/Open/Lambda_Register.py ${LAMBDA_TASK_ROOT}

COPY custom_util.py ${LAMBDA_TASK_ROOT}

CMD [ "Lambda_Register.lambda_handler" ]