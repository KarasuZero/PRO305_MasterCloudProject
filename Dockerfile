FROM public.ecr.aws/lambda/python:3.9

COPY Lambda/Store/Lambda_Store_Patch.py.py ${LAMBDA_TASK_ROOT}

COPY custom_util.py ${LAMBDA_TASK_ROOT}

CMD [ "Lambda_Store_Patch.lambda_handler" ]