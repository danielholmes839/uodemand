export function formatDate(date: Date): string {
  const offset = date.getTimezoneOffset();
  date = new Date(date.getTime() - offset * 60 * 1000);
  return date.toISOString().split("T")[0];
}

export function formatTime(date: Date): string {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let meridiem = hours >= 12 ? "pm" : "am";

  hours %= 12;

  if (hours === 0) {
    hours = 12;
  }

  let string = minutes < 10 ? "0" + minutes : minutes;

  return `${hours}:${string}${meridiem}`;
}
