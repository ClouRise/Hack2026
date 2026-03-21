import { defineStore } from 'pinia'

type Theme = 'light-theme' | 'dark-theme'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: 'light-theme' as Theme,
    isInitialized: false
  }),
  
  getters: {
    getCurrentTheme: (state) => state.currentTheme,
    
    isLightTheme: (state) => state.currentTheme === 'light-theme',
    
    isDarkTheme: (state) => state.currentTheme === 'dark-theme'
  },
  
  actions: {
    toggleTheme() {
      this.currentTheme = this.currentTheme === 'light-theme' 
        ? 'dark-theme' 
        : 'light-theme'
      
      if (process.client) {
        localStorage.setItem('theme', this.currentTheme)
      }
    },
    
    setTheme(theme: Theme) {
      this.currentTheme = theme
      if (process.client) {
        localStorage.setItem('theme', theme)
      }
    },
    
    initializeTheme() {
      if (process.client) {
        const savedTheme = localStorage.getItem('theme') as Theme | null
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        
        if (savedTheme) {
          this.currentTheme = savedTheme
        } else if (prefersDark) {
          this.currentTheme = 'dark-theme'
        } else {
          this.currentTheme = 'light-theme'
        }
        
        this.isInitialized = true
      }
    }
  }
})