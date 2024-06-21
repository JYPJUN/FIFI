import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import dotenv from 'dotenv'
import { createHtmlPlugin } from 'vite-plugin-html'

dotenv.config() //추가

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    createHtmlPlugin({ //추가
      inject: {
        data: {
          kakaoMapApiKey: process.env.VITE_KAKAO_MAP_API_KEY
        }
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
