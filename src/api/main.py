"""Entry point for API server (separate from bot)."""

import logging

import uvicorn


def main() -> None:
    """Run the API server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )

    logging.info("Starting AIDD Stats API server...")

    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
