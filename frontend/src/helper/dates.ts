import { format, parseISO } from "date-fns";
import { toZonedTime } from "date-fns-tz";

const toLocalDateTime = (
  utcDateString: string | Date,
  dateFormat = "dd/MM/yyyy hh:mm a"
): string => {
  const userTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  const date =
    typeof utcDateString === "string" ? parseISO(utcDateString) : utcDateString;

  const zonedDate = toZonedTime(date, userTimeZone);

  return format(zonedDate, dateFormat);
};

export { toLocalDateTime };
