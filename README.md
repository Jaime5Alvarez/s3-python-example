# S3 Python Example

A Python project demonstrating AWS S3 storage operations using Clean Architecture principles with async/await support.


## 🛠️ Installation

### Prerequisites

- Python 3.12 or higher
- LocalStack (for local S3 development)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd s3-python-example
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Start LocalStack** (for local development)
   ```bash
   docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack
   ```


## 🧪 Testing

Run the test suite:

```bash
# Using uv
uv run pytest

```