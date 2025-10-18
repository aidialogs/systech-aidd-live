/**
 * Formatting utilities for dashboard
 */

/**
 * Format number with thousand separators (1,234)
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

/**
 * Format trend percentage (+12.5%, -5.2%, 0.0%)
 */
export function formatTrend(trend: number): string {
  const sign = trend > 0 ? "+" : "";
  return `${sign}${trend.toFixed(1)}%`;
}

/**
 * Format date in European format DD-MM-YYYY (17-10-2025)
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
}

/**
 * Format date for chart axis (short format DD-MM)
 */
export function formatDateShort(dateString: string): string {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  return `${day}-${month}`;
}
