import ReactGA from "react-ga4";
import { Box, Button, FormControl, FormLabel, Input, Textarea, useToast , Text} from '@chakra-ui/react';
import React, { useState } from 'react';
import axios from 'axios';

const Contact = () => {
  if (process.env.NODE_ENV === "production") {
    ReactGA.send({ hitType: "pageview", page: "/contact", title: "Contact" });
  }

  const [formData, setFormData] = useState({
    firstName:'',
    lastName:'',
    email:'',
    message: '',
    genereMusicale:''
  });

  const toast = useToast(); // Per notifiche di successo/fallimento

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };
  const apiUrl = import.meta.env.VITE_API_URL;
  const handleSubmit = async (e) => {
    e.preventDefault();
    let firstName = localStorage.getItem('firstName');
    let lastName = localStorage.getItem('lastName');
    let email = localStorage.getItem('email');
    if(!firstName){
      toast({
        title: 'Errore',
        description: 'Loggati e riprova',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }else{
      formData.email=email;
      formData.lastName=lastName;
      formData.firstName=firstName;
      const url = `${apiUrl}/api/richieste/`;
      try {
        const response = await axios.post(url, formData, {
          headers: {
            Authorization: "Token b9862aacb7a0c2f9b1a346e8e1186607e61ecf81",
          },
          withCredentials: true,
        });

        if (response.status === 200) {
          toast({
            title: 'Email inviata!',
            description: 'Il tuo messaggio è stato inviato con successo.',
            status: 'success',
            duration: 5000,
            isClosable: true,
          });
          setFormData({  message: '',  genereMusicale:''});
        }
      } catch (error) {
        toast({
          title: 'Errore',
          description: 'Qualcosa è andato storto. Riprova.',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    }
  };
  return (
    <Box>
   
   <Text
            fontSize="lg"
            color="gray.700"
            mb={4}
            lineHeight="1.6"
          >Contattami via e-mail all'indirizzo di posta elettronica pasquale.daloiso@gmail.com</Text>
    <Text
          fontSize="lg"
          color="red.700"
          mb={4}
          lineHeight="1.6"
        >
  
  Se desideri altre canzoni, scrivimi il testo e il genere musicale che preferisci oppure compila il form qui sotto dopo esserti loggato.  
</Text>  

<form onSubmit={handleSubmit}>
  
        
        <FormControl id="message" isRequired mb={4}>
          <FormLabel>Genere musicale</FormLabel>
          <Input
            name="genereMusicale"
            value={formData.genereMusicale}
            onChange={handleChange}
            placeholder="Scrivi il tuo messaggio"
          />
        </FormControl>
        <FormControl id="message" isRequired mb={4}>
          <FormLabel>Testo della canzone</FormLabel>
          <Textarea  
            name="message"
            value={formData.message}
            onChange={handleChange}
            placeholder="Scrivi il testo"
            size="lg"
            height="300px"
          />
        </FormControl>

        <Button colorScheme="teal" type="submit" width="full">
          Invia Messaggio
        </Button>
      </form>
    </Box>
  )
}
export default Contact;