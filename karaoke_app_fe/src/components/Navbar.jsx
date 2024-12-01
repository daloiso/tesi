import { CiLogout } from "react-icons/ci";
import { 
  Flex, 
  Heading, 
  Text, 
  Button, 
  Spacer, 
  HStack, 
  
} from "@chakra-ui/react"
import {  toaster } from "./ui/toaster"

export default function Navbar() {


  return (
    <Flex as="nav" p="10px" mb="60px" alignItems="center">
      <Heading as="h1" fontSize="1.5em">Karaoke didattico</Heading>
      <Spacer />

      <HStack spacing="20px" display={"none"}> 
       
        <Text>il ponte</Text>
        <Button 
          colorScheme="purple"
          onClick={() => toaster.create({
            title: "Logged out.",
            description: "Arrivederci",
            placement: 'top',
          })}
        >Logout</Button>
      </HStack>
    </Flex>
  )
}
