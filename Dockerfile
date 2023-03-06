FROM public.ecr.aws/lambda/python:3.9

COPY Lambda/User/Lambda_User_Patch.py ${LAMBDA_TASK_ROOT}

COPY custom_util.py ${LAMBDA_TASK_ROOT}

CMD [ "Lambda_User_Patch.lambda_handler" ]