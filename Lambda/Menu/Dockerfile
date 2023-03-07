FROM public.ecr.aws/lambda/python:3.8
COPY Lambda_Menu_Get.py ${LAMBDA_TASK_ROOT}
COPY custom_util.py ${LAMBDA_TASK_ROOT}
CMD ["Lambda_Menu_Get.lambda_handler"]