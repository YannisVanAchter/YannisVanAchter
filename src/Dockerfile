# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Avinal Kumar <avinal.xlvii@gmail.com>
#
# Distributed under the terms of MIT License
# The full license is in the file LICENSE, distributed with this software.

FROM python:3.9-alpine

# Add files to docker
COPY . /app

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run the application
CMD ["python", "main.py"]
