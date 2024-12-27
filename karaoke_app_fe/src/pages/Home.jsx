import { Image,Center, Box } from '@chakra-ui/react'
import ReactGA from "react-ga4";

export default function Home() {
    if (process.env.NODE_ENV === "production") {
      ReactGA.send({ hitType: "pageview", page: "/", title: "Home" });
    }
    return (
      <Box w='50%' >
      <Center >
        <Image  borderRadius='full' src='/img/microphone.jpg' alt='karaoke' />
      </Center>
      </Box>
    )
  }