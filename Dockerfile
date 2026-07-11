# Start from the official slim Python image
FROM python:3.13-slim

# GeoDjango needs GDAL/GEOS/PROJ. The compilers (gcc/g++/python3-dev) are only
# needed to build the Python C-extensions, so install everything, build the
# wheels, then purge the compilers in the SAME layer so they don't ship in the
# final image. All GDAL/GEOS/PROJ libraries are kept exactly as before, so
# runtime library detection is unchanged.
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal \
    GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gdal-bin libgdal-dev libproj-dev proj-data proj-bin libgeos-dev \
        libpq-dev curl \
        gcc g++ python3-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y gcc g++ python3-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app
WORKDIR /app

# Expose port for Gunicorn server
EXPOSE 8000

# Healthcheck for Azure
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
 CMD curl -f http://localhost:8000/ || exit 1

# Start Gunicorn
CMD ["gunicorn", "dropped_kerb_mapper.wsgi:application", "--bind", "0.0.0.0:8000"]
