FROM ubuntu:disco
#change pip source

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y  nano net-tools iputils-ping libopencv-dev  python3.7-dev python3-pip tesseract-ocr tesseract-ocr-chi-sim
RUN mkdir /root/.pip &&  echo "[global]\nindex-url = https://pypi.douban.com/simple\ntrusted-host = pypi.douban.com" > /root/.pip/pip.conf
RUN pip3 install  'xlsxWriter==1.2.5' 'requests==2.20.1' 'opencv-contrib-python==3.4.2.17' 'pytesseract==0.3.0' 'numpy==1.17.4' 'Flask==1.1.1'
RUN pip3 install  'sympy==1.4.0' 'Flask-Session==0.3.1'
RUN pip3 install  'numpy==1.17.4' 'Pillow==6.1.0' 'h5py==2.10.0' 'web.py==0.40.dev0' 'scipy==1.3.3' 'scikit-image==0.16.2'
RUN pip3 install  'facenet-pytorch==2.2.9' 'torch==1.4.0' 'torchvision==0.5.0' 'scikit-learn==0.22.2.post1'




COPY ./*.py   /app/
COPY ./checkpoints/*   /root/.cache/torch/checkpoints/
#expose port

WORKDIR /app
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

CMD ["python3.7","server.py"]
