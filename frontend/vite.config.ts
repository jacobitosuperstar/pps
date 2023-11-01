/// <reference types="vitest" />
/// <reference types="Vite/client" />

import { defineConfig, } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { configDefaults } from 'vitest/config'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(),],
  test: {
    environment: "jsdom",
    globals: true,
    exclude: [...configDefaults.exclude, './e2e/*'],
  },

})
