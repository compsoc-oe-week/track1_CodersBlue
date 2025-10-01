FROM openeuler/openeuler:latest

SHELL ["/bin/bash", "-c"]
RUN /usr/bin/dnf update -y
RUN /usr/bin/dnf install -y python3 nodejs npm curl go sqlite htop
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
RUN . "$HOME/.cargo/env"
RUN /usr/bin/dnf group install -y "Development Tools"

WORKDIR /work

# Add a script to check environment variables
RUN echo '#!/bin/bash' > /usr/local/bin/check-env.sh && \
    echo 'echo "=== Environment Variables Check ==="' >> /usr/local/bin/check-env.sh && \
    echo 'echo "CODER_BASE_URL: ${CODER_BASE_URL:-NOT SET}"' >> /usr/local/bin/check-env.sh && \
    echo 'echo "CODER_MODEL_NAME: ${CODER_MODEL_NAME:-NOT SET}"' >> /usr/local/bin/check-env.sh && \
    echo 'echo "OPENAI_API_KEY: ${OPENAI_API_KEY:-NOT SET}"' >> /usr/local/bin/check-env.sh && \
    echo 'echo "=================================="' >> /usr/local/bin/check-env.sh && \
    chmod +x /usr/local/bin/check-env.sh

# Run the check when container starts
RUN echo 'check-env.sh' >> ~/.bashrc

ENTRYPOINT /bin/sh