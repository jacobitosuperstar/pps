export const trimAndCapitalize = (str: string) => {
  return str.trim().replace(/\b\w/g, (char) => char.toUpperCase());
};
