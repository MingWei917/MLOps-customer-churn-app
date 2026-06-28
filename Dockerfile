# 1. Use a lightweight, official Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /workspace

# 3. Copy ONLY the requirements file first.
# (This is a Docker best-practice: it caches this layer so pip install 
# doesn't re-run every time you change your Python code!)
COPY requirements.txt .

# 4. Install the dependencies using a specific mirror
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Define the default execution command 
# (Note: Argo Workflows will usually override this in your YAML)
#CMD ["python", "main.py"]