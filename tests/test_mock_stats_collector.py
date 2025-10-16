"""Tests for MockStatsCollector."""

import re
from datetime import datetime

import pytest

from src.mock_stats_collector import MockStatsCollector
from src.protocols import DashboardStats


@pytest.fixture
def collector() -> MockStatsCollector:
    """Create MockStatsCollector instance."""
    return MockStatsCollector()


@pytest.mark.asyncio
async def test_get_dashboard_stats_returns_correct_structure(
    collector: MockStatsCollector,
) -> None:
    """Test that get_dashboard_stats returns DashboardStats."""
    stats = await collector.get_dashboard_stats()

    assert isinstance(stats, DashboardStats)
    assert stats.total_users is not None
    assert stats.active_dialogs is not None
    assert stats.total_messages is not None
    assert stats.avg_message_length is not None
    assert stats.messages_chart_7d is not None
    assert stats.messages_chart_30d is not None


@pytest.mark.asyncio
async def test_metric_cards_have_required_fields(collector: MockStatsCollector) -> None:
    """Test that all metric cards have required fields."""
    stats = await collector.get_dashboard_stats()

    for metric_card in [
        stats.total_users,
        stats.active_dialogs,
        stats.total_messages,
        stats.avg_message_length,
    ]:
        assert metric_card.title != ""
        assert metric_card.value != ""
        assert metric_card.trend != ""
        assert metric_card.description != ""


@pytest.mark.asyncio
async def test_metric_values_are_formatted_with_commas(collector: MockStatsCollector) -> None:
    """Test that metric values are formatted with thousands separators."""
    stats = await collector.get_dashboard_stats()

    # Check that at least some values have comma separators
    # (assuming at least one metric has value >= 1000)
    all_values = [
        stats.total_users.value,
        stats.active_dialogs.value,
        stats.total_messages.value,
        stats.avg_message_length.value,
    ]

    # At least one value should contain a comma (for values >= 1000)
    has_comma = any("," in value for value in all_values)
    assert has_comma, "Expected at least one value with comma separator"


@pytest.mark.asyncio
async def test_trend_format_is_valid(collector: MockStatsCollector) -> None:
    """Test that trend values match expected format: +12.5% or -20.3%."""
    stats = await collector.get_dashboard_stats()

    # Regex pattern for trend: optional +/-, digits, optional decimal, %
    trend_pattern = re.compile(r"^[+-]\d+(\.\d+)?%$")

    for metric_card in [
        stats.total_users,
        stats.active_dialogs,
        stats.total_messages,
        stats.avg_message_length,
    ]:
        assert trend_pattern.match(metric_card.trend), f"Invalid trend format: {metric_card.trend}"


@pytest.mark.asyncio
async def test_chart_7d_has_correct_length(collector: MockStatsCollector) -> None:
    """Test that 7-day chart has exactly 7 data points."""
    stats = await collector.get_dashboard_stats()

    assert len(stats.messages_chart_7d) == 7


@pytest.mark.asyncio
async def test_chart_30d_has_correct_length(collector: MockStatsCollector) -> None:
    """Test that 30-day chart has exactly 30 data points."""
    stats = await collector.get_dashboard_stats()

    assert len(stats.messages_chart_30d) == 30


@pytest.mark.asyncio
async def test_chart_dates_are_iso8601_utc(collector: MockStatsCollector) -> None:
    """Test that chart dates are in ISO 8601 UTC format."""
    stats = await collector.get_dashboard_stats()

    # Test both charts
    for chart in [stats.messages_chart_7d, stats.messages_chart_30d]:
        for point in chart:
            # Should be able to parse as ISO 8601
            parsed_date = datetime.fromisoformat(point.date.replace("Z", "+00:00"))
            assert parsed_date is not None

            # Should end with Z (UTC indicator)
            assert point.date.endswith("Z")

            # Should match ISO format pattern
            iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
            assert iso_pattern.match(point.date), f"Invalid ISO 8601 format: {point.date}"


@pytest.mark.asyncio
async def test_chart_values_are_positive(collector: MockStatsCollector) -> None:
    """Test that all chart values are positive integers."""
    stats = await collector.get_dashboard_stats()

    for chart in [stats.messages_chart_7d, stats.messages_chart_30d]:
        for point in chart:
            assert isinstance(point.value, int)
            assert point.value > 0


@pytest.mark.asyncio
async def test_chart_values_are_in_reasonable_range(collector: MockStatsCollector) -> None:
    """Test that chart values are in a reasonable range."""
    stats = await collector.get_dashboard_stats()

    # Reasonable range: 100 to 10,000 messages per day
    min_value = 100
    max_value = 10000

    for chart in [stats.messages_chart_7d, stats.messages_chart_30d]:
        for point in chart:
            assert min_value <= point.value <= max_value, (
                f"Value {point.value} outside reasonable range [{min_value}, {max_value}]"
            )


@pytest.mark.asyncio
async def test_chart_dates_are_chronological(collector: MockStatsCollector) -> None:
    """Test that chart dates are in chronological order."""
    stats = await collector.get_dashboard_stats()

    for chart in [stats.messages_chart_7d, stats.messages_chart_30d]:
        dates = [datetime.fromisoformat(point.date.replace("Z", "+00:00")) for point in chart]

        # Check that dates are in ascending order
        for i in range(len(dates) - 1):
            assert dates[i] < dates[i + 1], "Dates are not in chronological order"


@pytest.mark.asyncio
async def test_multiple_calls_generate_different_data(collector: MockStatsCollector) -> None:
    """Test that multiple calls generate different random data."""
    stats1 = await collector.get_dashboard_stats()
    stats2 = await collector.get_dashboard_stats()

    # At least some values should be different due to randomness
    assert (
        stats1.total_users.value != stats2.total_users.value
        or stats1.active_dialogs.value != stats2.active_dialogs.value
        or stats1.total_messages.value != stats2.total_messages.value
    )


@pytest.mark.asyncio
async def test_metric_titles_are_correct(collector: MockStatsCollector) -> None:
    """Test that metric card titles match expected values."""
    stats = await collector.get_dashboard_stats()

    assert stats.total_users.title == "Total Users"
    assert stats.active_dialogs.title == "Active Dialogs"
    assert stats.total_messages.title == "Total Messages"
    assert stats.avg_message_length.title == "Avg Message Length"


@pytest.mark.asyncio
async def test_metric_descriptions_are_not_empty(collector: MockStatsCollector) -> None:
    """Test that all metric descriptions are populated."""
    stats = await collector.get_dashboard_stats()

    descriptions = [
        stats.total_users.description,
        stats.active_dialogs.description,
        stats.total_messages.description,
        stats.avg_message_length.description,
    ]

    for desc in descriptions:
        assert len(desc) > 0, "Description should not be empty"
