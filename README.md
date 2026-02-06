## Start locally
```bash
## Create virtual Environment
python -m venv .venv
## Activate virtual Environment
source .venv/bin/activate
## Install dependencies
pip install -r ./requirements.txt
## Start app
python -m uvicorn deface.api.deface:app --reload
```

-----

## Uvicorn server
Start uvicorn server:
```bash
python -m uvicorn deface.api.deface:app --reload
```

http://localhost:8000/docs

-----

## Docker 

Build image:
```bash
docker build -t deface-backend .
```

Run container:
```bash
docker run -d \
 --name deface-backend \
 -p 8000:8000 \
 deface-backend
```

Watch logs:
```bash
docker logs --follow deface-backend
```

Work/Test in container:
```bash
docker run -it --rm \
 -v $(pwd)/data/upload:/app/data/upload   -v $(pwd)/data/result:/app/data/result \
 --entrypoint /bin/bash \
 deface-backend
```



