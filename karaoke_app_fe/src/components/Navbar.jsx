import { CiLogout } from "react-icons/ci";
import { 
  Flex, 
  Heading, 
  Text, 
  Button, 
  Spacer, 
  HStack, 
  useToast,
} from "@chakra-ui/react"

export default function Navbar() {
  const toast = useToast()

  return (
    <Flex as="nav" p="10px" mb="60px" alignItems="center">
      <Heading as="h1" fontSize="1.5em">
      <Text 
      fontSize="2xl" 
      fontWeight="bold" 
      color="teal.500" 
      textAlign="center"
      mb={4}
    >Karaoke didattico
    </Text></Heading>
      <Spacer />

      <HStack spacing="20px" display={"none"}> 
       
        <Text>il ponte</Text>
        <Button 
          onClick={() => toast({
            title: 'Logged out.',
            description: "Uscito dal divertimento",
            duration: 10000,
            isClosable: true,
            position: 'top',
            status: 'success',
            
          })}
        >Logout</Button>
      </HStack>
    </Flex>
  )
}
