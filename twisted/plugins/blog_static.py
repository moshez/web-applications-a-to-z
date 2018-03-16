from twisted.application.service import ServiceMaker

serviceMaker = ServiceMaker(
    "Thing",
    "blog.twisted",
    "Thing",
    "blog",
)
