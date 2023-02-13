FROM public.ecr.aws/lambda/python:3.8
COPY Lambda_Menu.py ${LAMBDA_TASK_ROOT}
COPY custom_util.py ${LAMBDA_TASK_ROOT}
CMD ["Lambda_Menu.lambda_handler"]