
import { 
  Flex, 
  Heading, 
  Text, 
  Button, 
  Spacer, 
  HStack, 
  useToast,
} from "@chakra-ui/react"
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import * as jwt_decode from 'jwt-decode';


export default function Navbar() {
  const toast = useToast()
  const handleLoginSuccess = (response) => {
    console.log("Google Login Success:", response);
    // Qui puoi inviare il token a backend per autenticazione o usarlo direttamente
    const token = response.credential;
    const decodedToken = jwt_decode.jwtDecode(token);
    console.log(decodedToken);
    const name = decodedToken.name;  // Nome completo
    const firstName = decodedToken.given_name;  // Nome
    const lastName = decodedToken.family_name;  // Cognome
    const email = decodedToken.email;  // Email

    console.log(`Nome: ${firstName}`);
    console.log(`Cognome: ${lastName}`);
    console.log(`Email: ${email}`);


  };

  const handleLoginFailure = (error) => {
    console.error("Google Login Failed:", error);
    alert('login failure');
  };

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

      <HStack spacing="20px" > 
       
        <GoogleOAuthProvider clientId="173949360126-78n5ve6cd91s7k3bdpv6g0latcm6hkg9.apps.googleusercontent.com">
      <div>
        
        <GoogleLogin
          onSuccess={handleLoginSuccess}
          onError={handleLoginFailure}
        />
      </div>
    </GoogleOAuthProvider>
      </HStack>
    </Flex>
  )
}
