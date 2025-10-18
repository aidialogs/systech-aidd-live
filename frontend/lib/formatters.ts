/**
 * Format a number with commas for better readability
 * @param value - The number to format
 * @returns Formatted number string
 * @example formatNumber(1234567) => "1,234,567"
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat("en-US").format(value);
}

/**
 * Format a trend percentage with sign
 * @param trend - The trend value as percentage
 * @returns Formatted trend string
 * @example formatTrend(12.5) => "+12.5%"
 * @example formatTrend(-5.3) => "-5.3%"
 * @example formatTrend(0) => "0%"
 */
export function formatTrend(trend: number): string {
  if (trend === 0) return "0%";
  const sign = trend > 0 ? "+" : "";
  return `${sign}${trend.toFixed(1)}%`;
}

/**
 * Format a date string to short format (e.g., "Oct 17")
 * @param dateString - ISO date string
 * @returns Short date format
 * @example formatDateShort("2025-10-17") => "Oct 17"
 */
export function formatDateShort(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
  }).format(date);
}

/**
 * Format a date string to full format (e.g., "October 17, 2025")
 * @param dateString - ISO date string
 * @returns Full date format
 */
export function formatDateFull(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(date);
}

/**
 * Format a number as compact (e.g., 1K, 1.2M)
 * @param value - The number to format
 * @returns Compact format string
 * @example formatCompact(1234) => "1.2K"
 * @example formatCompact(1234567) => "1.2M"
 */
export function formatCompact(value: number): string {
  return new Intl.NumberFormat("en-US", {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}
