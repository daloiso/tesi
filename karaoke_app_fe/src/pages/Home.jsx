import { Image,Center, Box } from '@chakra-ui/react'
import ReactGA from "react-ga4";
import { keyframes } from "@emotion/react";

import { Link, Text } from '@chakra-ui/react'
export default function Home() {
    if (process.env.NODE_ENV === "production") {
      ReactGA.send({ hitType: "pageview", page: "/", title: "Home" });
    }
    const blink = keyframes`
    0% { color: green; opacity: 1; }
    50% { color: blue; opacity: 1; }
    100% { color: green; opacity: 1; }
  `;
    return (
      <Box><Text 
      fontSize="2xl" 
      fontWeight="bold" 
      color="teal.500" 
      textAlign="center"
      mb={4}
    >Impara a Cantare e Migliora la Tua Pronuncia in un Gioco!</Text>
        <Text
        fontSize="lg"
        color="gray.700"
        mb={4}
        lineHeight="1.6"
      >Scopri un modo innovativo per imparare attraverso canzoni create dall'intelligenza artificiale. 
      </Text>
      <Text
        fontSize="lg"
        color="gray.700"
        mb={4}
        lineHeight="1.6"
      >
Il nostro sistema interattivo ti aiuta a migliorare la pronuncia in modo divertente, utilizzando immagini e testi per facilitare la memorizzazione delle parole.</Text>
<Text
        fontSize="lg"
        color="gray.700"
        mb={4}
        lineHeight="1.6"
      >

Il gioco è super divertente! Devi ripetere delle parole e poi quelle stesse parole saranno usate nelle canzoni! Pronto a divertirti?
</Text>     
<Text
        fontSize="lg"
        color="red.700"
        mb={4}
        lineHeight="1.6"
      >

Novità: loggandoti avrai accesso ad una nuova traccia di musica, una salsa creata con strumenti professionali e a canzoni reali!!!
</Text>  
      <Center >
      <Link href="/dashboard">
      
      <Text
    fontSize="xl"
    fontWeight="bold"
    color="red"
   
    p={3}
    textAlign="center"
    mb={6}
   
    animation={`${blink} 1s infinite`} // Animazione di lampeggio
  >Prova subito il karaoke cliccando sull'immagine</Text>
        <Image  borderRadius='full' src='/img/microphone.jpg' alt='karaoke'  maxW="300px"    
              maxH="300px"       />
        
        </Link>
      </Center>
      </Box>
    
    )
  }