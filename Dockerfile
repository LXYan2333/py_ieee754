ARG BASE_IMAGE
FROM $BASE_IMAGE

RUN /opt/python/cp313-cp313/bin/pip install auditwheel cmake

COPY . /project
WORKDIR /project

CMD /opt/python/cp313-cp313/bin/python -m pip wheel . --no-deps -w /tmp/wheelhouse && \
    /opt/python/cp313-cp313/bin/python -m auditwheel repair /tmp/wheelhouse/*.whl -w /wheelhouse