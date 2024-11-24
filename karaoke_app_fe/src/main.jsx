import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ChakraProvider, defaultSystem } from "@chakra-ui/react"

ReactDOM.createRoot(document.getElementById('root')).render(
  <ChakraProvider value={defaultSystem}>
  <React.StrictMode>
    <App />
  </React.StrictMode>
  </ChakraProvider>
  ,
)

