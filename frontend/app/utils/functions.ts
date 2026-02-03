/** Returns a string describing the time remaining until the specified date.
 * @param date The future date to calculate the time remaining until.
 * @return A string representing the time remaining until the date in days, hours, or minutes.
 */
export function daysUntil(date: Date) {
  const diffTime = date.getTime() - Date.now();

  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  if (diffDays >= 7) return date.toLocaleString();
  if (diffDays >= 1) return `in ${diffDays} day${diffDays !== 1 ? "s" : ""}`;

  const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
  if (diffHours >= 1) return `in ${diffHours} hour${diffHours !== 1 ? "s" : ""}`;

  const diffMinutes = Math.ceil(diffTime / (1000 * 60));
  return `in ${diffMinutes} minute${diffMinutes !== 1 ? "s" : ""}`;
}
