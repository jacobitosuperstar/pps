export const compareObjectKeys = (object1: any, object2: any) => {
  const keys1 = Object.keys(object1);
  const keys2 = Object.keys(object2);

  if (keys1.length !== keys2.length) {
    return false;
  }

  for (const key of keys1) {
    // eslint-disable-next-line no-prototype-builtins
    if (!object2.hasOwnProperty(key)) {
      return false;
    }
  }

  return true;
};
