import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ChakraProvider,createSystem, defaultBaseConfig, defineConfig} from "@chakra-ui/react"

const colors = {
  yellowCustom: '#ffde59',  
};

const fonts = {
  body: 'Arial',
  heading: 'Courier New',
};
/** 
const customConfig = defineConfig({
  theme: {
    fonts,
    colors,
    ...withDefaultSize({
      size: 'lg',
    }),
    ...withDefaultColorScheme({
      colorScheme: 'yellowCustom',
    }),
  },
})

*/

const customConfig = defineConfig({
  theme: {
    fonts,
    colors,
  },
})

const system = createSystem(defaultBaseConfig, customConfig)

ReactDOM.createRoot(document.getElementById('root')).render(
  <ChakraProvider value={system}>
  <React.StrictMode>
    <App />
  </React.StrictMode>
  </ChakraProvider>
  ,
)

