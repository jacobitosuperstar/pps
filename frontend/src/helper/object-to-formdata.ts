export const objectToFormData = (obj: Record<string, any>): FormData => {
  const formData = new FormData();

  for (const key in obj) {
    // Verifica si la propiedad pertenece directamente al objeto (ignora las propiedades heredadas)
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const value = obj[key];

      // Si el valor es un archivo (File), lo agregamos directamente
      if (value instanceof File) {
        formData.append(key, value);
      } else {
        // Si no es un archivo, convertimos el valor a cadena y lo agregamos
        formData.append(key, String(value));
      }
    }
  }

  return formData;
};
