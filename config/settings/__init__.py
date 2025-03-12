import os
ENV = os.environ.get('stage', 'dev')
if ENV == 'prod':
    from .prod import *
elif ENV == 'local':
    from .local import *
else:
    from .dev import *