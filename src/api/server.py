"""API server entrypoint."""

import uvicorn
from dotenv import load_dotenv


def main() -> None:
    """Run API server with uvicorn."""
    # Load environment variables from .env file
    load_dotenv()

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
