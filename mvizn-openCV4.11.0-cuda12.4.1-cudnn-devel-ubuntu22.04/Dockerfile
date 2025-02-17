FROM nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install required system dependencies including GStreamer packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    pkg-config \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-setuptools \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libatlas-base-dev \
    libblas-dev \
    liblapack-dev \
    liblapacke-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory for sources
WORKDIR /opt

# Clone the OpenCV and opencv_contrib repositories (version 4.11.0)
RUN git clone --branch 4.11.0 --depth 1 https://github.com/opencv/opencv.git opencv-4.11.0 \
    && git clone --branch 4.11.0 --depth 1 https://github.com/opencv/opencv_contrib.git opencv_contrib-4.11.0

# Create a build directory and configure the build with CMake
WORKDIR /opt/opencv-4.11.0/build
RUN cmake -D CMAKE_BUILD_TYPE=Release \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib-4.11.0/modules \
      -D WITH_CUDA=ON \
      -D WITH_CUDNN=ON \
      -D CUDA_FAST_MATH=ON \
      -D WITH_CUBLAS=ON \
      -D BUILD_opencv_python3=ON \
      -D PYTHON_EXECUTABLE=$(which python3) \
      -D CUDA_ARCH_BIN="7.5,8.6,8.9" \
      -D CUDA_ARCH_PTX="9.0" \
      -D CPU_BASELINE="SSE4_1,SSE4_2,AVX,AVX2" \
      -D WITH_OPENMP=ON \
      -D WITH_TBB=ON \
      -D CMAKE_CXX_FLAGS_RELEASE="-march=native" \
      -D BUILD_TESTS=OFF \
      -D BUILD_PERF_TESTS=OFF \
      -D BUILD_EXAMPLES=OFF \
      ..

# Build and install OpenCV
RUN make -j$(nproc) && make install && ldconfig

# Clean up source directories to reduce image size
WORKDIR /
RUN rm -rf /opt/opencv-4.11.0 /opt/opencv_contrib-4.11.0

# Default command
CMD ["/bin/bash"]

