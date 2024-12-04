import { Image,Center, Box } from '@chakra-ui/react'

export default function Home() {
    return (
      <Box w='50%' >
      <Center >
        <Image  borderRadius='full' src='/img/microphone.jpg' alt='karaoke' />
      </Center>
      </Box>
    )
  }