"""Tests for Mock API statistics."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import create_app
from src.api.stat_collector_mock import MockStatCollector


@pytest.fixture
def mock_collector() -> MockStatCollector:
    """Create MockStatCollector instance."""
    return MockStatCollector()


@pytest.fixture
def test_client(mock_collector: MockStatCollector) -> TestClient:
    """Create FastAPI test client with mock collector."""
    app = create_app(mock_collector)
    return TestClient(app)


class TestMockStatCollector:
    """Tests for MockStatCollector."""

    async def test_get_statistics_default_period(self, mock_collector: MockStatCollector) -> None:
        """Test getting statistics with default period."""
        stats = await mock_collector.get_statistics()

        assert stats.period == "month"
        assert stats.overview.total_messages > 0
        assert stats.overview.total_users > 0
        assert stats.overview.active_chats > 0
        assert stats.overview.avg_message_length > 0

        # Check messages by role
        assert stats.messages_by_role.user > 0
        assert stats.messages_by_role.assistant > 0
        assert stats.messages_by_role.system >= 0

        # Check time series
        assert len(stats.messages_over_time) == 30  # month = 30 days
        assert all(point.count > 0 for point in stats.messages_over_time)

        # Check top metrics
        assert stats.top_metrics.most_active_users > 0
        assert stats.top_metrics.messages_today > 0
        assert stats.top_metrics.messages_this_week > 0
        assert stats.top_metrics.messages_this_month > 0

    async def test_get_statistics_day_period(self, mock_collector: MockStatCollector) -> None:
        """Test getting statistics for day period."""
        stats = await mock_collector.get_statistics(period="day")

        assert stats.period == "day"
        assert len(stats.messages_over_time) == 24  # 24 hours

    async def test_get_statistics_week_period(self, mock_collector: MockStatCollector) -> None:
        """Test getting statistics for week period."""
        stats = await mock_collector.get_statistics(period="week")

        assert stats.period == "week"
        assert len(stats.messages_over_time) == 7  # 7 days

    async def test_get_statistics_all_period(self, mock_collector: MockStatCollector) -> None:
        """Test getting statistics for all period."""
        stats = await mock_collector.get_statistics(period="all")

        assert stats.period == "all"
        assert len(stats.messages_over_time) == 12  # 12 months


class TestAPIEndpoints:
    """Tests for API endpoints."""

    def test_health_check(self, test_client: TestClient) -> None:
        """Test health check endpoint."""
        response = test_client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_get_statistics_default(self, test_client: TestClient) -> None:
        """Test getting statistics with default parameters."""
        response = test_client.get("/api/v1/statistics")

        assert response.status_code == 200

        data = response.json()
        assert data["period"] == "month"
        assert "overview" in data
        assert "messages_by_role" in data
        assert "messages_over_time" in data
        assert "top_metrics" in data

    def test_get_statistics_with_period(self, test_client: TestClient) -> None:
        """Test getting statistics with specific period."""
        response = test_client.get("/api/v1/statistics?period=week")

        assert response.status_code == 200

        data = response.json()
        assert data["period"] == "week"
        assert len(data["messages_over_time"]) == 7

    def test_get_statistics_invalid_period(self, test_client: TestClient) -> None:
        """Test getting statistics with invalid period."""
        response = test_client.get("/api/v1/statistics?period=invalid")

        assert response.status_code == 422  # Validation error

    def test_response_structure(self, test_client: TestClient) -> None:
        """Test complete response structure."""
        response = test_client.get("/api/v1/statistics")

        assert response.status_code == 200

        data = response.json()

        # Check overview structure
        overview = data["overview"]
        assert "total_messages" in overview
        assert "total_users" in overview
        assert "active_chats" in overview
        assert "avg_message_length" in overview

        # Check messages_by_role structure
        by_role = data["messages_by_role"]
        assert "user" in by_role
        assert "assistant" in by_role
        assert "system" in by_role

        # Check messages_over_time structure
        time_series = data["messages_over_time"]
        assert isinstance(time_series, list)
        assert len(time_series) > 0
        assert "date" in time_series[0]
        assert "count" in time_series[0]

        # Check top_metrics structure
        top_metrics = data["top_metrics"]
        assert "most_active_users" in top_metrics
        assert "messages_today" in top_metrics
        assert "messages_this_week" in top_metrics
        assert "messages_this_month" in top_metrics

    def test_openapi_docs_available(self, test_client: TestClient) -> None:
        """Test that OpenAPI documentation is available."""
        response = test_client.get("/openapi.json")

        assert response.status_code == 200

        openapi = response.json()
        assert "openapi" in openapi
        assert "info" in openapi
        assert "paths" in openapi
        assert "/api/v1/statistics" in openapi["paths"]
