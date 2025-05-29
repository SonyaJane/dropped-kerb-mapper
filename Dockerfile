# Start from the official slim Python image
FROM python:3.13-slim

# Install OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gdal-bin libgdal-dev libproj-dev proj-data proj-bin libgeos-dev gcc g++ python3-dev musl-dev libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Get GDAL version
RUN gdal-config --version

# Set environment variables so Python packages can find GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# Copy requirements first, for faster builds when dependencies don't change
COPY requirements.txt .

# Install Python dependencies (add gdal in your requirements.txt)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your application code
COPY . /app
WORKDIR /app

# Expose port for Gunicorn server
EXPOSE 8000

# (Optional) Healthcheck for Azure
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
 CMD curl -f http://localhost:8000/ || exit 1

# Start Gunicorn
CMD ["gunicorn", "dropped_kerb_mapper.wsgi:application", "--bind", "0.0.0.0:8000"]
