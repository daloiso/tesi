import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ChakraProvider,extendTheme,withDefaultSize,withDefaultColorScheme} from "@chakra-ui/react"

const colors = {
  yellowCustom: '#ffde59',
  buttonCustom: '#d9534f' , 
  custom: {
    blue: '#cdf3ff',
    text: '#003d4d'
  }
};

const fonts = {
  body: 'Arial',
  heading: 'Courier New',
};

const theme = extendTheme({
  
  fonts,
  colors,
  ...withDefaultSize({
    size: 'lg',
  }),
  ...withDefaultColorScheme({
    colorScheme: 'yellowCustom',
  }),
})



ReactDOM.createRoot(document.getElementById('root')).render(
  <ChakraProvider theme={theme}>
  <React.StrictMode>
    <App />
  </React.StrictMode>
  </ChakraProvider>
  ,
)

