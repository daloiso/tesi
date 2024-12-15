import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import commonjs from 'vite-plugin-commonjs';
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(), 
  commonjs()
],
server: {
  host: '0.0.0.0',  // Binds the dev server to all network interfaces
  port: 5173,        // Port for Vite dev server (can be adjusted if needed)
},
})
