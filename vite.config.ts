import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // Относительные пути: сборка работает на GitHub Pages в любой папке репозитория
  base: './',
  plugins: [react()],
})
